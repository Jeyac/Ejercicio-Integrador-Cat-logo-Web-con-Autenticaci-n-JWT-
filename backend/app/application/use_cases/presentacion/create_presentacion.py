from app.domain.entities.presentacion import Presentacion
from app.infrastructure.repository_impl.presentacion_repo import PresentacionRepository

class CreatePresentacionUseCase:
    def __init__(self, presentacion_repo: PresentacionRepository):
        self.presentacion_repo = presentacion_repo
    
    def execute(self, nombre: str, descripcion: str = None) -> Presentacion:
        # Validar datos
        presentacion = Presentacion(
            id=None,
            nombre=nombre,
            descripcion=descripcion
        )
        presentacion.validate()
        
        # Verificar que no exista una presentación con el mismo nombre
        if self.presentacion_repo.exists_by_nombre(nombre):
            raise ValueError(f"Ya existe una presentación con el nombre '{nombre}'")
        
        # Crear la presentación
        return self.presentacion_repo.create(presentacion)

