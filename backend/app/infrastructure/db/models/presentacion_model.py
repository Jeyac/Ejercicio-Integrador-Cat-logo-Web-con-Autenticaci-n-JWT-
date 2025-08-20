from ..base import db, BaseModel
from sqlalchemy import Index, func

class PresentacionModel(BaseModel):
    __tablename__ = 'presentaciones'
    
    nombre = db.Column(db.String(100), unique=True, nullable=False, index=True)
    descripcion = db.Column(db.Text, nullable=True)
    
    # Índice case-insensitive para búsquedas
    __table_args__ = (
        Index('ix_presentaciones_nombre_lower', func.lower(nombre)),
    )
    
    # Relación con productos
    productos = db.relationship('ProductoModel', backref='presentacion', lazy='dynamic')
    
    def __repr__(self):
        return f'<Presentacion {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
