from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from decimal import Decimal

@dataclass
class Producto:
    id: Optional[int]
    nombre: str
    precio: Decimal
    categoria_id: int
    presentacion_id: int
    activo: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.nombre:
            self.nombre = self.nombre.strip()
        if isinstance(self.precio, (int, float)):
            self.precio = Decimal(str(self.precio))
    
    def validate(self):
        if not self.nombre or len(self.nombre.strip()) == 0:
            raise ValueError("El nombre del producto es requerido")
        if len(self.nombre) > 200:
            raise ValueError("El nombre del producto no puede exceder 200 caracteres")
        if self.precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if not self.categoria_id or self.categoria_id <= 0:
            raise ValueError("Debe especificar una categoría válida")
        if not self.presentacion_id or self.presentacion_id <= 0:
            raise ValueError("Debe especificar una presentación válida")

