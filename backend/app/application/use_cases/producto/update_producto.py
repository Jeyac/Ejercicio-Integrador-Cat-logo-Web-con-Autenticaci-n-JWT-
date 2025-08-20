from typing import Optional
from decimal import Decimal
from app.domain.entities.producto import Producto
from app.infrastructure.repository_impl.producto_repo import ProductoRepository
from app.infrastructure.repository_impl.categoria_repo import CategoriaRepository
from app.infrastructure.repository_impl.presentacion_repo import PresentacionRepository

class UpdateProductoUseCase:
    def __init__(self, producto_repo: ProductoRepository, categoria_repo: CategoriaRepository, 
                 presentacion_repo: PresentacionRepository):
        self.producto_repo = producto_repo
        self.categoria_repo = categoria_repo
        self.presentacion_repo = presentacion_repo
    
    def execute(self, producto_id: int, nombre: str, precio: float, categoria_id: int, 
                presentacion_id: int, activo: bool = True) -> Optional[Producto]:
        if producto_id <= 0:
            raise ValueError("El ID del producto debe ser mayor a 0")
        
        # Verificar que el producto existe
        producto_existente = self.producto_repo.get_by_id(producto_id)
        if not producto_existente:
            return None
        
        # Validar que la categoría existe
        categoria = self.categoria_repo.get_by_id(categoria_id)
        if not categoria:
            raise ValueError(f"No existe una categoría con ID {categoria_id}")
        
        # Validar que la presentación existe
        presentacion = self.presentacion_repo.get_by_id(presentacion_id)
        if not presentacion:
            raise ValueError(f"No existe una presentación con ID {presentacion_id}")
        
        # Validar datos del producto
        producto_actualizado = Producto(
            id=producto_id,
            nombre=nombre,
            precio=Decimal(str(precio)),
            categoria_id=categoria_id,
            presentacion_id=presentacion_id,
            activo=activo
        )
        producto_actualizado.validate()
        
        # Verificar que no exista otro producto con el mismo nombre
        if self.producto_repo.exists_by_nombre(nombre, exclude_id=producto_id):
            raise ValueError(f"Ya existe otro producto con el nombre '{nombre}'")
        
        # Actualizar el producto
        return self.producto_repo.update(producto_id, producto_actualizado)

