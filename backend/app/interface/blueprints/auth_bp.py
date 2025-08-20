from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.application.use_cases.auth.register_user import RegisterUserUseCase
from app.application.use_cases.auth.login_user import LoginUserUseCase
from app.application.use_cases.auth.refresh_token import RefreshTokenUseCase
from app.infrastructure.repository_impl.usuario_repo import UsuarioRepository
from app.interface.http.dtos import RegisterUserDTO, LoginUserDTO, validate_json

auth_bp = Blueprint('auth', __name__)

# Instanciar repositorios y casos de uso
usuario_repo = UsuarioRepository()
register_use_case = RegisterUserUseCase(usuario_repo)
login_use_case = LoginUserUseCase(usuario_repo)
refresh_use_case = RefreshTokenUseCase()

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        # Validar datos de entrada
        data = validate_json(RegisterUserDTO, request.get_json())
        
        # Ejecutar caso de uso
        result = register_use_case.execute(
            email=data['email'],
            password=data['password'],
            nombre=data['nombre']
        )
        
        return jsonify({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'data': result
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # Validar datos de entrada
        data = validate_json(LoginUserDTO, request.get_json())
        
        # Ejecutar caso de uso
        result = login_use_case.execute(
            email=data['email'],
            password=data['password']
        )
        
        if not result:
            return jsonify({
                'success': False,
                'message': 'Credenciales inválidas'
            }), 401
        

        print(f"🔍 Login exitoso - Tokens generados: {result}")
        return jsonify({
            'success': True,
            'message': 'Inicio de sesión exitoso',
            'data': result
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        print(f"❌ Error en login: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error interno del servidor: {str(e)}'
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        # Log para debugging
        auth_header = request.headers.get('Authorization')
        print(f"🔍 Refresh endpoint - Authorization header: {auth_header}")
        
        # Ejecutar caso de uso
        result = refresh_use_case.execute()
        
        print(f"🔍 Refresh exitoso - Nuevo token generado: {result}")
        
        return jsonify({
            'success': True,
            'message': 'Token renovado exitosamente',
            'data': result
        }), 200
        
    except Exception as e:
        print(f"🔍 Refresh error: {e}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    try:
        from app.infrastructure.auth.jwt_service import JWTService
        user_id = JWTService.get_current_user_id()
        user_email = JWTService.get_current_user_email()
        
        return jsonify({
            'success': True,
            'data': {
                'id': user_id,
                'email': user_email
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500
