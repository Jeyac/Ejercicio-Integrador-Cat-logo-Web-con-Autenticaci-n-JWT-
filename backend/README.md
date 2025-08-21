# Backend Flask - Catálogo de Productos

Backend de la aplicación de catálogo de productos construido con **Flask**, siguiendo los principios de **Clean Architecture** y utilizando **PostgreSQL** como base de datos.

## Arquitectura

El backend está estructurado siguiendo los principios de **Clean Architecture**:

```
backend/
├── app/
│   ├── domain/              # Capa de dominio
│   │   └── entities/        # Entidades de negocio
│   ├── application/         # Capa de aplicación
│   │   └── use_cases/       # Casos de uso
│   ├── infrastructure/      # Capa de infraestructura
│   │   ├── db/             # Base de datos y modelos
│   │   ├── repository_impl/ # Implementaciones de repositorios
│   │   └── auth/           # Servicios de autenticación
│   └── interface/          # Capa de interfaz
│       ├── blueprints/     # Controladores Flask
│       └── http/          # DTOs y validación
├── migrations/             # Migraciones de base de datos
├── config.py              # Configuración de la aplicación
├── requirements.txt       # Dependencias Python
└── wsgi.py               # Punto de entrada
```

## 🚀 Características

### Autenticación JWT
- **Registro** y **login** de usuarios
- **Tokens de acceso** (1 hora) y **refresh** (30 días)
- **Rutas protegidas** con middleware JWT
- **Manejo automático** de tokens expirados

### Gestión de Entidades
- **Categorías**: Clasificación de productos
- **Presentaciones**: Formatos de presentación
- **Productos**: Gestión completa con precios y estado
- **Usuarios**: Sistema de autenticación

### Funcionalidades Avanzadas
- **Búsqueda** case-insensitive por nombre
- **Paginación** configurable
- **Filtros** por categoría y presentación
- **Validación** de datos con Marshmallow
- **Relaciones** entre entidades

## Requisitos Previos

- **Python 3.13+**
- **PostgreSQL 12+**
- **pip** (gestor de paquetes Python)

## Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Jeyac/Ejercicio-Integrador-Cat-logo-Web-con-Autenticaci-n-JWT-.git
cd Ejercicio-Integrador-Cat-logo-Web-con-Autenticaci-n-JWT-/backend
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crear archivo `.env` en el directorio `backend/`:

#### Generar Claves Secretas
Antes de crear el archivo `.env`, genera claves seguras:

```bash
# Opción 1: Usando Python
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"

# Opción 2: Usando OpenSSL
echo "SECRET_KEY=$(openssl rand -base64 32)"
echo "JWT_SECRET_KEY=$(openssl rand -base64 32)"
```

```env
# Configuración de la base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=catalogo_db
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_password_postgres

# Claves secretas (generar claves seguras)
# Ejemplos de claves generadas (cambiar por las tuyas):
SECRET_KEY=mi_clave_secreta_super_segura_2024_xyz123
JWT_SECRET_KEY=mi_jwt_secret_key_super_segura_2024_abc456

# Configuración de Flask
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

### 5. Configurar Base de Datos

#### Crear Base de Datos PostgreSQL
```sql
CREATE DATABASE catalogo_db;
CREATE USER tu_usuario_postgres WITH PASSWORD 'tu_password_postgres';
GRANT ALL PRIVILEGES ON DATABASE catalogo_db TO tu_usuario_postgres;
```

#### Inicializar Migraciones
```bash
# Inicializar Alembic
flask db init

# Crear migración inicial
flask db migrate -m "Initial migration"

# Aplicar migraciones
flask db upgrade
```

### 6. Ejecutar la Aplicación
```bash
python wsgi.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `DB_HOST` | Host de PostgreSQL | `localhost` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DB_NAME` | Nombre de la base de datos | `catalogo_db` |
| `DB_USER` | Usuario de PostgreSQL | `tu_usuario_postgres` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `tu_password_postgres` |
| `SECRET_KEY` | Clave secreta de Flask | Requerida (generar con herramientas de seguridad) |
| `JWT_SECRET_KEY` | Clave secreta para JWT | Requerida (generar con herramientas de seguridad) |
| `FLASK_DEBUG` | Modo debug | `False` |

### Configuración de CORS
El backend está configurado para permitir peticiones desde:
- `http://localhost:8080` (Frontend en desarrollo)
- `http://127.0.0.1:8080`
- `http://localhost:3000`
- `http://127.0.0.1:3000`

**Para acceso desde red local, agregar tu IP a `CORS_ORIGINS` en `config.py`:**
```python
CORS_ORIGINS = [
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://TU_IP_LOCAL:8080',  # Agregar tu IP aquí
    'http://TU_IP_LOCAL:3000'   # Agregar tu IP aquí
]
```

## API Endpoints

### Autenticación
```
POST /api/auth/register     # Registro de usuario
POST /api/auth/login        # Login de usuario
POST /api/auth/refresh      # Refresh de token
GET  /api/auth/me          # Información del usuario
```

### Health Check
```
GET  /api/health           # Estado de la API
GET  /                     # Información del servidor
```

### Categorías
```
GET    /api/categorias      # Listar categorías (paginado, búsqueda)
POST   /api/categorias      # Crear categoría
PUT    /api/categorias/:id  # Actualizar categoría
DELETE /api/categorias/:id  # Eliminar categoría
```

### Presentaciones
```
GET    /api/presentaciones      # Listar presentaciones
POST   /api/presentaciones      # Crear presentación
PUT    /api/presentaciones/:id  # Actualizar presentación
DELETE /api/presentaciones/:id  # Eliminar presentación
```

### Productos
```
GET    /api/productos       # Listar productos (con filtros)
POST   /api/productos       # Crear producto
PUT    /api/productos/:id   # Actualizar producto
DELETE /api/productos/:id   # Eliminar producto
```

### Parámetros de Query
- **Paginación**: `?page=1&size=10`
- **Búsqueda**: `?q=texto`
- **Filtros**: `?categoria_id=1&presentacion_id=1`

## Modelo de Datos

### Categorías
```sql
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Presentaciones
```sql
CREATE TABLE presentaciones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Productos
```sql
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) UNIQUE NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    categoria_id INTEGER REFERENCES categorias(id),
    presentacion_id INTEGER REFERENCES presentaciones(id),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Usuarios
```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Scripts de Desarrollo

### Ejecutar en Modo Desarrollo
```bash
python wsgi.py
```

### Ejecutar Tests
```bash
pytest
```

### Crear Migración
```bash
flask db migrate -m "Descripción del cambio"
```

### Aplicar Migraciones
```bash
flask db upgrade
```

### Revertir Migración
```bash
flask db downgrade
```

## Solución de Problemas

### Error de Conexión a Base de Datos
1. Verificar que PostgreSQL esté ejecutándose
2. Confirmar credenciales en `.env`
3. Verificar que la base de datos existe
4. Comprobar permisos del usuario

### Error de CORS
1. Verificar configuración en `config.py`
2. Confirmar que el frontend esté en el puerto correcto
3. Revisar headers de las peticiones
4. **Para acceso desde red local**: Agregar tu IP a `CORS_ORIGINS`

### Error de Conexión desde Otros Dispositivos
1. **Obtener tu IP real**: 
   - Windows: `ipconfig | findstr "IPv4"`
   - Linux/Mac: `ifconfig` o `ip addr`
2. **Actualizar CORS**: Agregar `http://TU_IP:8080` a `CORS_ORIGINS` en `config.py`
3. **Reiniciar backend**: `python wsgi.py`
4. **Verificar firewall**: Permitir conexiones en puerto 5000

### Error de JWT
1. Verificar que las claves secretas estén configuradas
2. Confirmar que los tokens no hayan expirado
3. Revisar la configuración de CORS

### Error de Migraciones
1. Verificar que Alembic esté inicializado
2. Comprobar que la base de datos esté creada
3. Revisar permisos del usuario de base de datos

## Tecnologías Utilizadas

- **Flask 3.0** - Framework web
- **SQLAlchemy 2.0** - ORM
- **PostgreSQL** - Base de datos
- **Alembic** - Migraciones
- **JWT** - Autenticación
- **Marshmallow** - Validación
- **Flask-CORS** - Manejo de CORS
- **psycopg[binary]** - Driver PostgreSQL

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Seguridad

### Variables de Entorno
- **Nunca compartas** tus archivos `.env` con credenciales reales
- **Usa ejemplos genéricos** para credenciales de base de datos
- **Genera claves seguras** para `SECRET_KEY` y `JWT_SECRET_KEY`
- **Cambia las credenciales** por defecto de PostgreSQL

### Cómo Generar Claves Seguras
```bash
# Opción 1: Usando Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Opción 2: Usando OpenSSL
openssl rand -base64 32

# Opción 3: Usando Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### Ejemplo de Configuración Segura
```env
# CORRECTO - Usar valores genéricos para credenciales de BD
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_password_postgres

# CORRECTO - Usar ejemplos de claves generadas
SECRET_KEY=mi_clave_secreta_super_segura_2024_xyz123
JWT_SECRET_KEY=mi_jwt_secret_key_super_segura_2024_abc456

## Autor

**Jeraldyn** - [GitHub](https://github.com/Jeyac)

## Repositorio

**URL del Repositorio**: https://github.com/Jeyac/Ejercicio-Integrador-Cat-logo-Web-con-Autenticaci-n-JWT-.git

---

⭐ Si este proyecto te ha sido útil, ¡dale una estrella!
