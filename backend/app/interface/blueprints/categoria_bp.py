from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.application.use_cases.categoria.create_categoria import CreateCategoriaUseCase
from app.application.use_cases.categoria.list_categorias import ListCategoriasUseCase
from app.application.use_cases.categoria.get_categoria import GetCategoriaUseCase
from app.application.use_cases.categoria.update_categoria import UpdateCategoriaUseCase
from app.application.use_cases.categoria.delete_categoria import DeleteCategoriaUseCase
from app.infrastructure.repository_impl.categoria_repo import CategoriaRepository
from app.interface.http.dtos import CreateCategoriaDTO, UpdateCategoriaDTO, validate_json

categoria_bp = Blueprint('categoria', __name__)

# Instanciar repositorio y casos de uso
categoria_repo = CategoriaRepository()
create_use_case = CreateCategoriaUseCase(categoria_repo)
list_use_case = ListCategoriasUseCase(categoria_repo)
get_use_case = GetCategoriaUseCase(categoria_repo)
update_use_case = UpdateCategoriaUseCase(categoria_repo)
delete_use_case = DeleteCategoriaUseCase(categoria_repo)

@categoria_bp.route('', methods=['GET'])
@jwt_required()
def list_categorias():
    try:
        # Log para debugging
        auth_header = request.headers.get('Authorization')
        print(f"🔍 List categorias - Authorization header: {auth_header}")
        
        # Obtener parámetros de query
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        search = request.args.get('q', None, type=str)
        
        # Ejecutar caso de uso
        categorias, total = list_use_case.execute(page=page, per_page=size, search=search)
        
        # Convertir entidades a diccionarios
        categorias_dict = []
        for categoria in categorias:
            categorias_dict.append({
                'id': categoria.id,
                'nombre': categoria.nombre,
                'descripcion': categoria.descripcion,
                'created_at': categoria.created_at.isoformat() if categoria.created_at else None,
                'updated_at': categoria.updated_at.isoformat() if categoria.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': {
                'items': categorias_dict,
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

@categoria_bp.route('', methods=['POST'])
@jwt_required()
def create_categoria():
    try:
        # Log para debugging
        auth_header = request.headers.get('Authorization')
        print(f"🔍 Create categoria - Authorization header: {auth_header}")
        
        # Validar datos de entrada
        data = validate_json(CreateCategoriaDTO, request.get_json())
        
        # Ejecutar caso de uso
        categoria = create_use_case.execute(
            nombre=data['nombre'],
            descripcion=data.get('descripcion')
        )
        
        return jsonify({
            'success': True,
            'message': 'Categoría creada exitosamente',
            'data': {
                'id': categoria.id,
                'nombre': categoria.nombre,
                'descripcion': categoria.descripcion,
                'created_at': categoria.created_at.isoformat() if categoria.created_at else None,
                'updated_at': categoria.updated_at.isoformat() if categoria.updated_at else None
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

@categoria_bp.route('/<int:categoria_id>', methods=['GET'])
@jwt_required()
def get_categoria(categoria_id):
    try:
        # Ejecutar caso de uso
        categoria = get_use_case.execute(categoria_id)
        
        if not categoria:
            return jsonify({
                'success': False,
                'message': 'Categoría no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': categoria.id,
                'nombre': categoria.nombre,
                'descripcion': categoria.descripcion,
                'created_at': categoria.created_at.isoformat() if categoria.created_at else None,
                'updated_at': categoria.updated_at.isoformat() if categoria.updated_at else None
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

@categoria_bp.route('/<int:categoria_id>', methods=['PUT'])
@jwt_required()
def update_categoria(categoria_id):
    """
    Actualiza una categoría existente por su ID.
    
    Args:
        categoria_id (int): ID de la categoría a actualizar
        
    Returns:
        JSON: Respuesta con la categoría actualizada o error
    """
    try:
        # Validar datos de entrada usando el DTO correspondiente
        data = validate_json(UpdateCategoriaDTO, request.get_json())
        
        # Ejecutar caso de uso para actualizar la categoría
        categoria = update_use_case.execute(
            categoria_id=categoria_id,
            nombre=data['nombre'],
            descripcion=data.get('descripcion')
        )
        
        if not categoria:
            return jsonify({
                'success': False,
                'message': 'Categoría no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Categoría actualizada exitosamente',
            'data': {
                'id': categoria.id,
                'nombre': categoria.nombre,
                'descripcion': categoria.descripcion,
                'created_at': categoria.created_at.isoformat() if categoria.created_at else None,
                'updated_at': categoria.updated_at.isoformat() if categoria.updated_at else None
            }
        }), 200
        
    except ValueError as e:
        # Error de validación de datos
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        # Error interno del servidor
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

@categoria_bp.route('/<int:categoria_id>', methods=['DELETE'])
@jwt_required()
def delete_categoria(categoria_id):
    try:
        # Ejecutar caso de uso
        deleted = delete_use_case.execute(categoria_id)
        
        if not deleted:
            return jsonify({
                'success': False,
                'message': 'Categoría no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Categoría eliminada exitosamente'
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
