from typing import Optional
from app.domain.entities.producto import Producto
from app.infrastructure.repository_impl.producto_repo import ProductoRepository

class GetProductoUseCase:
    def __init__(self, producto_repo: ProductoRepository):
        self.producto_repo = producto_repo
    
    def execute(self, producto_id: int) -> Optional[Producto]:
        if producto_id <= 0:
            raise ValueError("El ID del producto debe ser mayor a 0")
        
        return self.producto_repo.get_by_id(producto_id)

