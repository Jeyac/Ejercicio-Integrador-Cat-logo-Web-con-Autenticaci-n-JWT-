from typing import Optional
from sqlalchemy import func
from app.domain.entities.usuario import Usuario
from app.infrastructure.db.models.usuario_model import UsuarioModel
from app.infrastructure.db.base import db

class UsuarioRepository:
    
    def create(self, usuario: Usuario) -> Usuario:
        usuario_model = UsuarioModel(
            email=usuario.email,
            password_hash=usuario.password_hash,
            nombre=usuario.nombre,
            activo=usuario.activo
        )
        db.session.add(usuario_model)
        db.session.commit()
        
        return self._model_to_entity(usuario_model)
    
    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        usuario_model = UsuarioModel.query.get(usuario_id)
        if usuario_model:
            return self._model_to_entity(usuario_model)
        return None
    
    def get_by_email(self, email: str) -> Optional[Usuario]:
        usuario_model = UsuarioModel.query.filter(
            func.lower(UsuarioModel.email) == func.lower(email)
        ).first()
        if usuario_model:
            return self._model_to_entity(usuario_model)
        return None
    
    def exists_by_email(self, email: str, exclude_id: int = None) -> bool:
        query = UsuarioModel.query.filter(
            func.lower(UsuarioModel.email) == func.lower(email)
        )
        if exclude_id:
            query = query.filter(UsuarioModel.id != exclude_id)
        return query.first() is not None
    
    def update(self, usuario_id: int, usuario: Usuario) -> Optional[Usuario]:
        usuario_model = UsuarioModel.query.get(usuario_id)
        if not usuario_model:
            return None
        
        usuario_model.email = usuario.email
        usuario_model.nombre = usuario.nombre
        usuario_model.activo = usuario.activo
        if usuario.password_hash:
            usuario_model.password_hash = usuario.password_hash
        db.session.commit()
        
        return self._model_to_entity(usuario_model)
    
    def _model_to_entity(self, model: UsuarioModel) -> Usuario:
        return Usuario(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            nombre=model.nombre,
            activo=model.activo,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

