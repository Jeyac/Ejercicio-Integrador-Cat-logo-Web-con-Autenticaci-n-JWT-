from decimal import Decimal
from app.domain.entities.producto import Producto
from app.infrastructure.repository_impl.producto_repo import ProductoRepository
from app.infrastructure.repository_impl.categoria_repo import CategoriaRepository
from app.infrastructure.repository_impl.presentacion_repo import PresentacionRepository

class CreateProductoUseCase:
    def __init__(self, producto_repo: ProductoRepository, categoria_repo: CategoriaRepository, 
                 presentacion_repo: PresentacionRepository):
        self.producto_repo = producto_repo
        self.categoria_repo = categoria_repo
        self.presentacion_repo = presentacion_repo
    
    def execute(self, nombre: str, precio: float, categoria_id: int, 
                presentacion_id: int, activo: bool = True) -> Producto:
        # Validar que la categoría existe
        categoria = self.categoria_repo.get_by_id(categoria_id)
        if not categoria:
            raise ValueError(f"No existe una categoría con ID {categoria_id}")
        
        # Validar que la presentación existe
        presentacion = self.presentacion_repo.get_by_id(presentacion_id)
        if not presentacion:
            raise ValueError(f"No existe una presentación con ID {presentacion_id}")
        
        # Validar datos del producto
        producto = Producto(
            id=None,
            nombre=nombre,
            precio=Decimal(str(precio)),
            categoria_id=categoria_id,
            presentacion_id=presentacion_id,
            activo=activo
        )
        producto.validate()
        
        # Verificar que no exista un producto con el mismo nombre
        if self.producto_repo.exists_by_nombre(nombre):
            raise ValueError(f"Ya existe un producto con el nombre '{nombre}'")
        
        # Crear el producto
        return self.producto_repo.create(producto)

