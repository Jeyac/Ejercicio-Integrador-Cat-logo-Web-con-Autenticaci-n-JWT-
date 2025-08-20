from werkzeug.security import check_password_hash
from app.infrastructure.repository_impl.usuario_repo import UsuarioRepository
from app.infrastructure.auth.jwt_service import JWTService
from typing import Dict, Any, Optional

class LoginUserUseCase:
    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo
    
    def execute(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        # Buscar el usuario por email
        usuario = self.usuario_repo.get_by_email(email)
        if not usuario:
            return None
        
        # Verificar que el usuario esté activo
        if not usuario.activo:
            raise ValueError("La cuenta de usuario está desactivada")
        
        # Verificar la contraseña
        if not check_password_hash(usuario.password_hash, password):
            return None
        
        # Generar tokens JWT
        tokens = JWTService.create_tokens(usuario.id, usuario.email)
        
        return {
            "user": {
                "id": usuario.id,
                "email": usuario.email,
                "nombre": usuario.nombre
            },
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"]
        }

