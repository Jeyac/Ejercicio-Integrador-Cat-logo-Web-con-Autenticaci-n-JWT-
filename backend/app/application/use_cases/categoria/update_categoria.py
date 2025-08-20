from typing import Optional
from app.domain.entities.categoria import Categoria
from app.infrastructure.repository_impl.categoria_repo import CategoriaRepository

class UpdateCategoriaUseCase:
    def __init__(self, categoria_repo: CategoriaRepository):
        self.categoria_repo = categoria_repo
    
    def execute(self, categoria_id: int, nombre: str, descripcion: str = None) -> Optional[Categoria]:
        if categoria_id <= 0:
            raise ValueError("El ID de la categoría debe ser mayor a 0")
        
        # Verificar que la categoría existe
        categoria_existente = self.categoria_repo.get_by_id(categoria_id)
        if not categoria_existente:
            return None
        
        # Validar datos
        categoria_actualizada = Categoria(
            id=categoria_id,
            nombre=nombre,
            descripcion=descripcion
        )
        categoria_actualizada.validate()
        
        # Verificar que no exista otra categoría con el mismo nombre
        if self.categoria_repo.exists_by_nombre(nombre, exclude_id=categoria_id):
            raise ValueError(f"Ya existe otra categoría con el nombre '{nombre}'")
        
        # Actualizar la categoría
        return self.categoria_repo.update(categoria_id, categoria_actualizada)

