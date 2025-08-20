from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.application.use_cases.producto.create_producto import CreateProductoUseCase
from app.application.use_cases.producto.list_productos import ListProductosUseCase
from app.application.use_cases.producto.get_producto import GetProductoUseCase
from app.application.use_cases.producto.update_producto import UpdateProductoUseCase
from app.application.use_cases.producto.delete_producto import DeleteProductoUseCase
from app.infrastructure.repository_impl.producto_repo import ProductoRepository
from app.infrastructure.repository_impl.categoria_repo import CategoriaRepository
from app.infrastructure.repository_impl.presentacion_repo import PresentacionRepository
from app.interface.http.dtos import CreateProductoDTO, UpdateProductoDTO, validate_json

producto_bp = Blueprint('producto', __name__)

# Instanciar repositorios y casos de uso
producto_repo = ProductoRepository()
categoria_repo = CategoriaRepository()
presentacion_repo = PresentacionRepository()

create_use_case = CreateProductoUseCase(producto_repo, categoria_repo, presentacion_repo)
list_use_case = ListProductosUseCase(producto_repo)
get_use_case = GetProductoUseCase(producto_repo)
update_use_case = UpdateProductoUseCase(producto_repo, categoria_repo, presentacion_repo)
delete_use_case = DeleteProductoUseCase(producto_repo)

@producto_bp.route('', methods=['GET'])
@jwt_required()
def list_productos():
    try:
        # Obtener parámetros de query
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        search = request.args.get('q', None, type=str)
        categoria_id = request.args.get('categoria_id', None, type=int)
        presentacion_id = request.args.get('presentacion_id', None, type=int)
        
        # Ejecutar caso de uso
        productos, total = list_use_case.execute(
            page=page, 
            per_page=size, 
            search=search,
            categoria_id=categoria_id,
            presentacion_id=presentacion_id
        )
        
        # Convertir entidades a diccionarios
        productos_dict = []
        for producto in productos:
            productos_dict.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'categoria_id': producto.categoria_id,
                'presentacion_id': producto.presentacion_id,
                'activo': producto.activo,
                'created_at': producto.created_at.isoformat() if producto.created_at else None,
                'updated_at': producto.updated_at.isoformat() if producto.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': {
                'items': productos_dict,
                'total': total,
                'page': page,
                'size': size
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@producto_bp.route('', methods=['POST'])
@jwt_required()
def create_producto():
    try:
        # Validar datos de entrada
        data = validate_json(CreateProductoDTO, request.get_json())
        
        # Ejecutar caso de uso
        producto = create_use_case.execute(
            nombre=data['nombre'],
            precio=float(data['precio']),
            categoria_id=data['categoria_id'],
            presentacion_id=data['presentacion_id'],
            activo=data.get('activo', True)
        )
        
        return jsonify({
            'success': True,
            'message': 'Producto creado exitosamente',
            'data': {
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'categoria_id': producto.categoria_id,
                'presentacion_id': producto.presentacion_id,
                'activo': producto.activo,
                'created_at': producto.created_at.isoformat() if producto.created_at else None,
                'updated_at': producto.updated_at.isoformat() if producto.updated_at else None
            }
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@producto_bp.route('/<int:producto_id>', methods=['GET'])
@jwt_required()
def get_producto(producto_id):
    try:
        # Ejecutar caso de uso
        producto = get_use_case.execute(producto_id)
        
        if not producto:
            return jsonify({
                'success': False,
                'message': 'Producto no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'categoria_id': producto.categoria_id,
                'presentacion_id': producto.presentacion_id,
                'activo': producto.activo,
                'created_at': producto.created_at.isoformat() if producto.created_at else None,
                'updated_at': producto.updated_at.isoformat() if producto.updated_at else None
            }
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@producto_bp.route('/<int:producto_id>', methods=['PUT'])
@jwt_required()
def update_producto(producto_id):
    try:
        # Validar datos de entrada
        data = validate_json(UpdateProductoDTO, request.get_json())
        
        # Ejecutar caso de uso
        producto = update_use_case.execute(
            producto_id=producto_id,
            nombre=data['nombre'],
            precio=float(data['precio']),
            categoria_id=data['categoria_id'],
            presentacion_id=data['presentacion_id'],
            activo=data.get('activo', True)
        )
        
        if not producto:
            return jsonify({
                'success': False,
                'message': 'Producto no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Producto actualizado exitosamente',
            'data': {
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'categoria_id': producto.categoria_id,
                'presentacion_id': producto.presentacion_id,
                'activo': producto.activo,
                'created_at': producto.created_at.isoformat() if producto.created_at else None,
                'updated_at': producto.updated_at.isoformat() if producto.updated_at else None
            }
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@producto_bp.route('/<int:producto_id>', methods=['DELETE'])
@jwt_required()
def delete_producto(producto_id):
    try:
        # Ejecutar caso de uso
        deleted = delete_use_case.execute(producto_id)
        
        if not deleted:
            return jsonify({
                'success': False,
                'message': 'Producto no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Producto eliminado exitosamente'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

