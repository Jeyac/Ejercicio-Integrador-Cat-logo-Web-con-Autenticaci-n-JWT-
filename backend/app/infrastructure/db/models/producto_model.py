from ..base import db, BaseModel
from decimal import Decimal
from sqlalchemy import Index, func

class ProductoModel(BaseModel):
    __tablename__ = 'productos'
    
    nombre = db.Column(db.String(200), unique=True, nullable=False, index=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    
    # Foreign Keys
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    presentacion_id = db.Column(db.Integer, db.ForeignKey('presentaciones.id'), nullable=False)
    
    # Índice case-insensitive para búsquedas
    __table_args__ = (
        Index('ix_productos_nombre_lower', func.lower(nombre)),
    )
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': float(self.precio) if self.precio else 0,
            'categoria_id': self.categoria_id,
            'presentacion_id': self.presentacion_id,
            'activo': self.activo,
            'categoria': self.categoria.to_dict() if self.categoria else None,
            'presentacion': self.presentacion.to_dict() if self.presentacion else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
