from typing import List, Tuple
from app.domain.entities.presentacion import Presentacion
from app.infrastructure.repository_impl.presentacion_repo import PresentacionRepository

class ListPresentacionesUseCase:
    def __init__(self, presentacion_repo: PresentacionRepository):
        self.presentacion_repo = presentacion_repo
    
    def execute(self, page: int = 1, per_page: int = 10, search: str = None) -> Tuple[List[Presentacion], int]:
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
            
        return self.presentacion_repo.get_all(page=page, per_page=per_page, search=search)

