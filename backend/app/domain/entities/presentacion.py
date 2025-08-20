from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Presentacion:
    id: Optional[int]
    nombre: str
    descripcion: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.nombre:
            self.nombre = self.nombre.strip()
    
    def validate(self):
        if not self.nombre or len(self.nombre.strip()) == 0:
            raise ValueError("El nombre de la presentación es requerido")
        if len(self.nombre) > 100:
            raise ValueError("El nombre de la presentación no puede exceder 100 caracteres")
        if self.descripcion and len(self.descripcion) > 500:
            raise ValueError("La descripción no puede exceder 500 caracteres")

