from typing import Optional
from app.domain.entities.presentacion import Presentacion
from app.infrastructure.repository_impl.presentacion_repo import PresentacionRepository

class GetPresentacionUseCase:
    def __init__(self, presentacion_repo: PresentacionRepository):
        self.presentacion_repo = presentacion_repo
    
    def execute(self, presentacion_id: int) -> Optional[Presentacion]:
        if presentacion_id <= 0:
            raise ValueError("El ID de la presentación debe ser mayor a 0")
        
        return self.presentacion_repo.get_by_id(presentacion_id)

