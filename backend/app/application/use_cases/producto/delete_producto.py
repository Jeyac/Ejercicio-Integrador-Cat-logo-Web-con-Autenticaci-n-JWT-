from app.infrastructure.repository_impl.producto_repo import ProductoRepository

class DeleteProductoUseCase:
    def __init__(self, producto_repo: ProductoRepository):
        self.producto_repo = producto_repo
    
    def execute(self, producto_id: int) -> bool:
        if producto_id <= 0:
            raise ValueError("El ID del producto debe ser mayor a 0")
        
        # Verificar que el producto existe
        producto_existente = self.producto_repo.get_by_id(producto_id)
        if not producto_existente:
            return False
        
        # Eliminar el producto
        return self.producto_repo.delete(producto_id)

