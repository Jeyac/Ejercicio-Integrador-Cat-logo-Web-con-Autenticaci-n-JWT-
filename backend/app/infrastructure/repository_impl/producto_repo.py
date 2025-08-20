from typing import List, Optional
from sqlalchemy import func
from decimal import Decimal
from app.domain.entities.producto import Producto
from app.infrastructure.db.models.producto_model import ProductoModel
from app.infrastructure.db.base import db

class ProductoRepository:
    
    def create(self, producto: Producto) -> Producto:
        producto_model = ProductoModel(
            nombre=producto.nombre,
            precio=producto.precio,
            categoria_id=producto.categoria_id,
            presentacion_id=producto.presentacion_id,
            activo=producto.activo
        )
        db.session.add(producto_model)
        db.session.commit()
        
        return self._model_to_entity(producto_model)
    
    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        producto_model = ProductoModel.query.get(producto_id)
        if producto_model:
            return self._model_to_entity(producto_model)
        return None
    
    def get_by_nombre(self, nombre: str) -> Optional[Producto]:
        producto_model = ProductoModel.query.filter(
            func.lower(ProductoModel.nombre) == func.lower(nombre)
        ).first()
        if producto_model:
            return self._model_to_entity(producto_model)
        return None
    
    def get_all(self, page: int = 1, per_page: int = 10, search: str = None, 
               categoria_id: int = None, presentacion_id: int = None) -> tuple[List[Producto], int]:
        query = ProductoModel.query
        
        if search:
            query = query.filter(
                func.lower(ProductoModel.nombre).contains(func.lower(search))
            )
        
        if categoria_id:
            query = query.filter(ProductoModel.categoria_id == categoria_id)
        
        if presentacion_id:
            query = query.filter(ProductoModel.presentacion_id == presentacion_id)
        
        paginated = query.order_by(ProductoModel.nombre).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        productos = [self._model_to_entity(model) for model in paginated.items]
        return productos, paginated.total
    
    def update(self, producto_id: int, producto: Producto) -> Optional[Producto]:
        producto_model = ProductoModel.query.get(producto_id)
        if not producto_model:
            return None
        
        producto_model.nombre = producto.nombre
        producto_model.precio = producto.precio
        producto_model.categoria_id = producto.categoria_id
        producto_model.presentacion_id = producto.presentacion_id
        producto_model.activo = producto.activo
        db.session.commit()
        
        return self._model_to_entity(producto_model)
    
    def delete(self, producto_id: int) -> bool:
        producto_model = ProductoModel.query.get(producto_id)
        if not producto_model:
            return False
        
        db.session.delete(producto_model)
        db.session.commit()
        return True
    
    def exists_by_nombre(self, nombre: str, exclude_id: int = None) -> bool:
        query = ProductoModel.query.filter(
            func.lower(ProductoModel.nombre) == func.lower(nombre)
        )
        if exclude_id:
            query = query.filter(ProductoModel.id != exclude_id)
        return query.first() is not None
    
    def _model_to_entity(self, model: ProductoModel) -> Producto:
        return Producto(
            id=model.id,
            nombre=model.nombre,
            precio=Decimal(str(model.precio)),
            categoria_id=model.categoria_id,
            presentacion_id=model.presentacion_id,
            activo=model.activo,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

