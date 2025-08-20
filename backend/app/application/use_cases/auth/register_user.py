from werkzeug.security import generate_password_hash
from app.domain.entities.usuario import Usuario
from app.infrastructure.repository_impl.usuario_repo import UsuarioRepository
from app.infrastructure.auth.jwt_service import JWTService
from typing import Dict, Any

class RegisterUserUseCase:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo
    
    def execute(self, email: str, password: str, nombre: str) -> Dict[str, Any]:
        # Validar que el email no esté en uso
        if self.usuario_repo.exists_by_email(email):
            raise ValueError("Ya existe un usuario registrado con este email")
        
        # Validar longitud de la contraseña
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        
        # Crear el usuario
        usuario = Usuario(
            id=None,
            email=email,
            password_hash=generate_password_hash(password),
            nombre=nombre,
            activo=True
        )
        usuario.validate()
        
        # Guardar el usuario
        usuario_creado = self.usuario_repo.create(usuario)
        
        # Generar tokens JWT
        tokens = JWTService.create_tokens(usuario_creado.id, usuario_creado.email)
        
        return {
            "user": {
                "id": usuario_creado.id,
                "email": usuario_creado.email,
                "nombre": usuario_creado.nombre
            },
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"]
        }

