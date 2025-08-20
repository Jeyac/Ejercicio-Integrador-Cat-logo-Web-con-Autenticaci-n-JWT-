import os
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

# Cargar variables de entorno desde .env
load_dotenv()

from config import Config
from app.infrastructure.db.base import db

jwt = JWTManager()
migrate = Migrate()

def create_database_if_not_exists():
    try:
        try:
            import psycopg2
            psycopg_driver = psycopg2
        except ImportError:
            try:
                import psycopg
                psycopg_driver = psycopg
            except ImportError:
                raise ImportError("Se requiere psycopg2 o psycopg para PostgreSQL")

        conn = psycopg_driver.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            dbname='postgres',
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s", (Config.DB_NAME,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {Config.DB_NAME}")
            print(f"✅ Base de datos '{Config.DB_NAME}' creada exitosamente")
        else:
            print(f"✅ Base de datos '{Config.DB_NAME}' ya existe")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"⚠️  Error al verificar/crear base de datos: {e}")
        print("⚠️  Asegúrate de que PostgreSQL esté ejecutándose y las credenciales sean correctas")

def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    
    create_database_if_not_exists()
    
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    from app.interface.blueprints.auth_bp import auth_bp
    from app.interface.blueprints.categoria_bp import categoria_bp
    from app.interface.blueprints.presentacion_bp import presentacion_bp
    from app.interface.blueprints.producto_bp import producto_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(categoria_bp, url_prefix='/api/categorias')
    app.register_blueprint(presentacion_bp, url_prefix='/api/presentaciones')
    app.register_blueprint(producto_bp, url_prefix='/api/productos')
    
    # Endpoint de salud para verificar que la API esté funcionando
    @app.route('/api/health')
    def health_check():
        return {
            'status': 'success',
            'message': 'API del Catálogo de Productos funcionando correctamente',
            'timestamp': '2025-08-20',
            'version': '1.0.0',
            'cors_origins': app.config['CORS_ORIGINS']
        }
    
    # Endpoint raíz de la API
    @app.route('/api')
    def api_root():
        return {
            'message': 'API del Catálogo de Productos',
            'endpoints': {
                'health': '/api/health',
                'auth': '/api/auth',
                'categorias': '/api/categorias',
                'presentaciones': '/api/presentaciones',
                'productos': '/api/productos'
            },
            'status': 'online'
        }
    
    # Endpoint en la raíz del servidor (puerto 5000)
    @app.route('/')
    def root():
        return {
            'message': '🚀 Servidor del Catálogo de Productos funcionando correctamente',
            'api_url': '/api',
            'health_check': '/api/health',
            'frontend_url': 'http://192.168.0.105:8080',
            'status': 'online',
            'timestamp': '2025-08-20',
            'version': '1.0.0'
        }
    
    return app
