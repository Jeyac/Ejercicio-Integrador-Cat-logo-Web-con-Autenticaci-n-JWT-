from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from typing import Dict

class JWTService:
    
    @staticmethod
    def create_tokens(user_id: int, email: str) -> Dict[str, str]:
        """Crear tokens de acceso y refresh para un usuario"""
        additional_claims = {"email": email}
        
        access_token = create_access_token(
            identity=str(user_id),  # Convertir a string
            additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(
            identity=str(user_id),  # Convertir a string
            additional_claims=additional_claims
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    @staticmethod
    def get_current_user_id() -> int:
        """Obtener el ID del usuario actual desde el token JWT"""
        user_id = get_jwt_identity()
        return int(user_id) if user_id else None
    
    @staticmethod
    def get_current_user_email() -> str:
        """Obtener el email del usuario actual desde el token JWT"""
        jwt_data = get_jwt()
        return jwt_data.get("email")
