from typing import List, Optional
from sqlalchemy import func
from app.domain.entities.categoria import Categoria
from app.infrastructure.db.models.categoria_model import CategoriaModel
from app.infrastructure.db.base import db

class CategoriaRepository:
    
    def create(self, categoria: Categoria) -> Categoria:
        categoria_model = CategoriaModel(
            nombre=categoria.nombre,
            descripcion=categoria.descripcion
        )
        db.session.add(categoria_model)
        db.session.commit()
        
        return self._model_to_entity(categoria_model)
    
    def get_by_id(self, categoria_id: int) -> Optional[Categoria]:
        categoria_model = CategoriaModel.query.get(categoria_id)
        if categoria_model:
            return self._model_to_entity(categoria_model)
        return None
    
    def get_by_nombre(self, nombre: str) -> Optional[Categoria]:
        categoria_model = CategoriaModel.query.filter(
            func.lower(CategoriaModel.nombre) == func.lower(nombre)
        ).first()
        if categoria_model:
            return self._model_to_entity(categoria_model)
        return None
    
    def get_all(self, page: int = 1, per_page: int = 10, search: str = None) -> tuple[List[Categoria], int]:
        query = CategoriaModel.query
        
        if search:
            query = query.filter(
                func.lower(CategoriaModel.nombre).contains(func.lower(search))
            )
        
        paginated = query.order_by(CategoriaModel.nombre).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        categorias = [self._model_to_entity(model) for model in paginated.items]
        return categorias, paginated.total
    
    def update(self, categoria_id: int, categoria: Categoria) -> Optional[Categoria]:
        categoria_model = CategoriaModel.query.get(categoria_id)
        if not categoria_model:
            return None
        
        categoria_model.nombre = categoria.nombre
        categoria_model.descripcion = categoria.descripcion
        db.session.commit()
        
        return self._model_to_entity(categoria_model)
    
    def delete(self, categoria_id: int) -> bool:
        categoria_model = CategoriaModel.query.get(categoria_id)
        if not categoria_model:
            return False
        
        # Verificar si tiene productos asociados
        if categoria_model.productos.count() > 0:
            raise ValueError("No se puede eliminar la categoría porque tiene productos asociados")
        
        db.session.delete(categoria_model)
        db.session.commit()
        return True
    
    def exists_by_nombre(self, nombre: str, exclude_id: int = None) -> bool:
        query = CategoriaModel.query.filter(
            func.lower(CategoriaModel.nombre) == func.lower(nombre)
        )
        if exclude_id:
            query = query.filter(CategoriaModel.id != exclude_id)
        return query.first() is not None
    
    def _model_to_entity(self, model: CategoriaModel) -> Categoria:
        return Categoria(
            id=model.id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

