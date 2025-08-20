from app.infrastructure.repository_impl.categoria_repo import CategoriaRepository

class DeleteCategoriaUseCase:
    def __init__(self, categoria_repo: CategoriaRepository):
        self.categoria_repo = categoria_repo
    
    def execute(self, categoria_id: int) -> bool:
        if categoria_id <= 0:
            raise ValueError("El ID de la categoría debe ser mayor a 0")
        
        # Verificar que la categoría existe
        categoria_existente = self.categoria_repo.get_by_id(categoria_id)
        if not categoria_existente:
            return False
        
        # Intentar eliminar (el repositorio verificará si tiene productos asociados)
        return self.categoria_repo.delete(categoria_id)

