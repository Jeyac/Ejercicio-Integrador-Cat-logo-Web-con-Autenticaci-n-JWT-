from flask_jwt_extended import get_jwt_identity, get_jwt, create_access_token
from typing import Dict

class RefreshTokenUseCase:
    def __init__(self):
        pass
    
    def execute(self) -> Dict[str, str]:
        # Obtener el ID del usuario desde el refresh token
        current_user_id = get_jwt_identity()
        jwt_data = get_jwt()
        
        # Crear un nuevo access token
        new_access_token = create_access_token(
            identity=str(current_user_id),  # Convertir a string
            additional_claims={"email": jwt_data.get("email")}
        )
        
        return {
            "access_token": new_access_token
        }
