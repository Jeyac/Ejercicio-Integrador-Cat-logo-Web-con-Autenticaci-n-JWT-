from typing import List, Tuple
from app.domain.entities.categoria import Categoria
from app.infrastructure.repository_impl.categoria_repo import CategoriaRepository

class ListCategoriasUseCase:
    def __init__(self, categoria_repo: CategoriaRepository):
        self.categoria_repo = categoria_repo
    
    def execute(self, page: int = 1, per_page: int = 10, search: str = None) -> Tuple[List[Categoria], int]:
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
            
        return self.categoria_repo.get_all(page=page, per_page=per_page, search=search)

