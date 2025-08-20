from typing import List, Tuple, Optional
from app.domain.entities.producto import Producto
from app.infrastructure.repository_impl.producto_repo import ProductoRepository

class ListProductosUseCase:
    def __init__(self, producto_repo: ProductoRepository):
        self.producto_repo = producto_repo
    
    def execute(self, page: int = 1, per_page: int = 10, search: str = None, 
                categoria_id: Optional[int] = None, presentacion_id: Optional[int] = None) -> Tuple[List[Producto], int]:
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
            
        return self.producto_repo.get_all(
            page=page, 
            per_page=per_page, 
            search=search,
            categoria_id=categoria_id,
            presentacion_id=presentacion_id
        )

