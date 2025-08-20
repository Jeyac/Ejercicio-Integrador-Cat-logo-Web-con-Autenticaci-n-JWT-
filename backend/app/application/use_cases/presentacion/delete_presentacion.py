from app.infrastructure.repository_impl.presentacion_repo import PresentacionRepository

class DeletePresentacionUseCase:
    def __init__(self, presentacion_repo: PresentacionRepository):
        self.presentacion_repo = presentacion_repo
    
    def execute(self, presentacion_id: int) -> bool:
        if presentacion_id <= 0:
            raise ValueError("El ID de la presentación debe ser mayor a 0")
        
        # Verificar que la presentación existe
        presentacion_existente = self.presentacion_repo.get_by_id(presentacion_id)
        if not presentacion_existente:
            return False
        
        # Intentar eliminar (el repositorio verificará si tiene productos asociados)
        return self.presentacion_repo.delete(presentacion_id)

