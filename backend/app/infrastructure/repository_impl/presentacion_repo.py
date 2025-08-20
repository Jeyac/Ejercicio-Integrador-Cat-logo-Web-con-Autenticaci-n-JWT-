from typing import List, Optional
from sqlalchemy import func
from app.domain.entities.presentacion import Presentacion
from app.infrastructure.db.models.presentacion_model import PresentacionModel
from app.infrastructure.db.base import db

class PresentacionRepository:
    
    def create(self, presentacion: Presentacion) -> Presentacion:
        presentacion_model = PresentacionModel(
            nombre=presentacion.nombre,
            descripcion=presentacion.descripcion
        )
        db.session.add(presentacion_model)
        db.session.commit()
        
        return self._model_to_entity(presentacion_model)
    
    def get_by_id(self, presentacion_id: int) -> Optional[Presentacion]:
        presentacion_model = PresentacionModel.query.get(presentacion_id)
        if presentacion_model:
            return self._model_to_entity(presentacion_model)
        return None
    
    def get_by_nombre(self, nombre: str) -> Optional[Presentacion]:
        presentacion_model = PresentacionModel.query.filter(
            func.lower(PresentacionModel.nombre) == func.lower(nombre)
        ).first()
        if presentacion_model:
            return self._model_to_entity(presentacion_model)
        return None
    
    def get_all(self, page: int = 1, per_page: int = 10, search: str = None) -> tuple[List[Presentacion], int]:
        query = PresentacionModel.query
        
        if search:
            query = query.filter(
                func.lower(PresentacionModel.nombre).contains(func.lower(search))
            )
        
        paginated = query.order_by(PresentacionModel.nombre).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        presentaciones = [self._model_to_entity(model) for model in paginated.items]
        return presentaciones, paginated.total
    
    def update(self, presentacion_id: int, presentacion: Presentacion) -> Optional[Presentacion]:
        presentacion_model = PresentacionModel.query.get(presentacion_id)
        if not presentacion_model:
            return None
        
        presentacion_model.nombre = presentacion.nombre
        presentacion_model.descripcion = presentacion.descripcion
        db.session.commit()
        
        return self._model_to_entity(presentacion_model)
    
    def delete(self, presentacion_id: int) -> bool:
        presentacion_model = PresentacionModel.query.get(presentacion_id)
        if not presentacion_model:
            return False
        
        # Verificar si tiene productos asociados
        if presentacion_model.productos.count() > 0:
            raise ValueError("No se puede eliminar la presentación porque tiene productos asociados")
        
        db.session.delete(presentacion_model)
        db.session.commit()
        return True
    
    def exists_by_nombre(self, nombre: str, exclude_id: int = None) -> bool:
        query = PresentacionModel.query.filter(
            func.lower(PresentacionModel.nombre) == func.lower(nombre)
        )
        if exclude_id:
            query = query.filter(PresentacionModel.id != exclude_id)
        return query.first() is not None
    
    def _model_to_entity(self, model: PresentacionModel) -> Presentacion:
        return Presentacion(
            id=model.id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

