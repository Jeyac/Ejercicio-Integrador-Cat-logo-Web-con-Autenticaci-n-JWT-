from marshmallow import Schema, fields, validate, ValidationError

# DTOs para Autenticación
class RegisterUserDTO(Schema):
    email = fields.Email(required=True, error_messages={"required": "El email es requerido"})
    password = fields.Str(required=True, validate=validate.Length(min=6), 
                         error_messages={"required": "La contraseña es requerida"})
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=100),
                       error_messages={"required": "El nombre es requerido"})

class LoginUserDTO(Schema):
    email = fields.Email(required=True, error_messages={"required": "El email es requerido"})
    password = fields.Str(required=True, error_messages={"required": "La contraseña es requerida"})

# DTOs para Categoría
class CreateCategoriaDTO(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=100),
                       error_messages={"required": "El nombre es requerido"})
    descripcion = fields.Str(missing=None, validate=validate.Length(max=500))

class UpdateCategoriaDTO(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=100),
                       error_messages={"required": "El nombre es requerido"})
    descripcion = fields.Str(missing=None, validate=validate.Length(max=500))

# DTOs para Presentación
class CreatePresentacionDTO(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=100),
                       error_messages={"required": "El nombre es requerido"})
    descripcion = fields.Str(missing=None, validate=validate.Length(max=500))

class UpdatePresentacionDTO(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=100),
                       error_messages={"required": "El nombre es requerido"})
    descripcion = fields.Str(missing=None, validate=validate.Length(max=500))

# DTOs para Producto
class CreateProductoDTO(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=200),
                       error_messages={"required": "El nombre es requerido"})
    precio = fields.Decimal(required=True, validate=validate.Range(min=0.01),
                           error_messages={"required": "El precio es requerido"})
    categoria_id = fields.Int(required=True, validate=validate.Range(min=1),
                             error_messages={"required": "La categoría es requerida"})
    presentacion_id = fields.Int(required=True, validate=validate.Range(min=1),
                                error_messages={"required": "La presentación es requerida"})
    activo = fields.Bool(missing=True)

class UpdateProductoDTO(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=200),
                       error_messages={"required": "El nombre es requerido"})
    precio = fields.Decimal(required=True, validate=validate.Range(min=0.01),
                           error_messages={"required": "El precio es requerido"})
    categoria_id = fields.Int(required=True, validate=validate.Range(min=1),
                             error_messages={"required": "La categoría es requerida"})
    presentacion_id = fields.Int(required=True, validate=validate.Range(min=1),
                                error_messages={"required": "La presentación es requerida"})
    activo = fields.Bool(missing=True)

# Función helper para validar datos
def validate_json(schema_class, json_data):
    schema = schema_class()
    try:
        return schema.load(json_data)
    except ValidationError as err:
        raise ValueError(f"Datos inválidos: {err.messages}")

