from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import re

@dataclass
class Usuario:
    id: Optional[int]
    email: str
    password_hash: str
    nombre: str
    activo: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.email:
            self.email = self.email.strip().lower()
        if self.nombre:
            self.nombre = self.nombre.strip()
    
    def validate(self):
        if not self.email or len(self.email.strip()) == 0:
            raise ValueError("El email es requerido")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValueError("El formato del email no es válido")
        
        if not self.nombre or len(self.nombre.strip()) == 0:
            raise ValueError("El nombre es requerido")
        if len(self.nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

