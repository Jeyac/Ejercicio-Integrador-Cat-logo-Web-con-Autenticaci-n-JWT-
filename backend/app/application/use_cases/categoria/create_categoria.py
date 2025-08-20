from app.domain.entities.categoria import Categoria
from app.infrastructure.repository_impl.categoria_repo import CategoriaRepository

class CreateCategoriaUseCase:
    def __init__(self, categoria_repo: CategoriaRepository):
        self.categoria_repo = categoria_repo
    
    def execute(self, nombre: str, descripcion: str = None) -> Categoria:
        # Validar datos
        categoria = Categoria(
            id=None,
            nombre=nombre,
            descripcion=descripcion
        )
        categoria.validate()
        
        # Verificar que no exista una categoría con el mismo nombre
        if self.categoria_repo.exists_by_nombre(nombre):
            raise ValueError(f"Ya existe una categoría con el nombre '{nombre}'")
        
        # Crear la categoría
        return self.categoria_repo.create(categoria)

