from typing import Optional
from app.domain.entities.categoria import Categoria
from app.infrastructure.repository_impl.categoria_repo import CategoriaRepository

class GetCategoriaUseCase:
    def __init__(self, categoria_repo: CategoriaRepository):
        self.categoria_repo = categoria_repo
    
    def execute(self, categoria_id: int) -> Optional[Categoria]:
        if categoria_id <= 0:
            raise ValueError("El ID de la categoría debe ser mayor a 0")
        
        return self.categoria_repo.get_by_id(categoria_id)

