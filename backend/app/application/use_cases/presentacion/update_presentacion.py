from typing import Optional
from app.domain.entities.presentacion import Presentacion
from app.infrastructure.repository_impl.presentacion_repo import PresentacionRepository

class UpdatePresentacionUseCase:
    def __init__(self, presentacion_repo: PresentacionRepository):
        self.presentacion_repo = presentacion_repo
    
    def execute(self, presentacion_id: int, nombre: str, descripcion: str = None) -> Optional[Presentacion]:
        if presentacion_id <= 0:
            raise ValueError("El ID de la presentación debe ser mayor a 0")
        
        # Verificar que la presentación existe
        presentacion_existente = self.presentacion_repo.get_by_id(presentacion_id)
        if not presentacion_existente:
            return None
        
        # Validar datos
        presentacion_actualizada = Presentacion(
            id=presentacion_id,
            nombre=nombre,
            descripcion=descripcion
        )
        presentacion_actualizada.validate()
        
        # Verificar que no exista otra presentación con el mismo nombre
        if self.presentacion_repo.exists_by_nombre(nombre, exclude_id=presentacion_id):
            raise ValueError(f"Ya existe otra presentación con el nombre '{nombre}'")
        
        # Actualizar la presentación
        return self.presentacion_repo.update(presentacion_id, presentacion_actualizada)

