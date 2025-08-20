from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.application.use_cases.presentacion.create_presentacion import CreatePresentacionUseCase
from app.application.use_cases.presentacion.list_presentaciones import ListPresentacionesUseCase
from app.application.use_cases.presentacion.get_presentacion import GetPresentacionUseCase
from app.application.use_cases.presentacion.update_presentacion import UpdatePresentacionUseCase
from app.application.use_cases.presentacion.delete_presentacion import DeletePresentacionUseCase
from app.infrastructure.repository_impl.presentacion_repo import PresentacionRepository
from app.interface.http.dtos import CreatePresentacionDTO, UpdatePresentacionDTO, validate_json

presentacion_bp = Blueprint('presentacion', __name__)

# Instanciar repositorio y casos de uso
presentacion_repo = PresentacionRepository()
create_use_case = CreatePresentacionUseCase(presentacion_repo)
list_use_case = ListPresentacionesUseCase(presentacion_repo)
get_use_case = GetPresentacionUseCase(presentacion_repo)
update_use_case = UpdatePresentacionUseCase(presentacion_repo)
delete_use_case = DeletePresentacionUseCase(presentacion_repo)

@presentacion_bp.route('', methods=['GET'])
@jwt_required()
def list_presentaciones():
    try:
        # Obtener parámetros de query
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        search = request.args.get('q', None, type=str)
        
        # Ejecutar caso de uso
        presentaciones, total = list_use_case.execute(page=page, per_page=size, search=search)
        
        # Convertir entidades a diccionarios
        presentaciones_dict = []
        for presentacion in presentaciones:
            presentaciones_dict.append({
                'id': presentacion.id,
                'nombre': presentacion.nombre,
                'descripcion': presentacion.descripcion,
                'created_at': presentacion.created_at.isoformat() if presentacion.created_at else None,
                'updated_at': presentacion.updated_at.isoformat() if presentacion.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'data': {
                'items': presentaciones_dict,
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

@presentacion_bp.route('', methods=['POST'])
@jwt_required()
def create_presentacion():
    try:
        # Validar datos de entrada
        data = validate_json(CreatePresentacionDTO, request.get_json())
        
        # Ejecutar caso de uso
        presentacion = create_use_case.execute(
            nombre=data['nombre'],
            descripcion=data.get('descripcion')
        )
        
        return jsonify({
            'success': True,
            'message': 'Presentación creada exitosamente',
            'data': {
                'id': presentacion.id,
                'nombre': presentacion.nombre,
                'descripcion': presentacion.descripcion,
                'created_at': presentacion.created_at.isoformat() if presentacion.created_at else None,
                'updated_at': presentacion.updated_at.isoformat() if presentacion.updated_at else None
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

@presentacion_bp.route('/<int:presentacion_id>', methods=['GET'])
@jwt_required()
def get_presentacion(presentacion_id):
    try:
        # Ejecutar caso de uso
        presentacion = get_use_case.execute(presentacion_id)
        
        if not presentacion:
            return jsonify({
                'success': False,
                'message': 'Presentación no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': presentacion.id,
                'nombre': presentacion.nombre,
                'descripcion': presentacion.descripcion,
                'created_at': presentacion.created_at.isoformat() if presentacion.created_at else None,
                'updated_at': presentacion.updated_at.isoformat() if presentacion.updated_at else None
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

@presentacion_bp.route('/<int:presentacion_id>', methods=['PUT'])
@jwt_required()
def update_presentacion(presentacion_id):
    """
    Actualiza una presentación existente por su ID.
    
    Args:
        presentacion_id (int): ID de la presentación a actualizar
        
    Returns:
        JSON: Respuesta con la presentación actualizada o error
    """
    try:
        # Validar datos de entrada usando el DTO correspondiente
        data = validate_json(UpdatePresentacionDTO, request.get_json())
        
        # Ejecutar caso de uso para actualizar la presentación
        presentacion = update_use_case.execute(
            presentacion_id=presentacion_id,
            nombre=data['nombre'],
            descripcion=data.get('descripcion')
        )
        
        if not presentacion:
            return jsonify({
                'success': False,
                'message': 'Presentación no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Presentación actualizada exitosamente',
            'data': {
                'id': presentacion.id,
                'nombre': presentacion.nombre,
                'descripcion': presentacion.descripcion,
                'created_at': presentacion.created_at.isoformat() if presentacion.created_at else None,
                'updated_at': presentacion.updated_at.isoformat() if presentacion.updated_at else None
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

@presentacion_bp.route('/<int:presentacion_id>', methods=['DELETE'])
@jwt_required()
def delete_presentacion(presentacion_id):
    try:
        # Ejecutar caso de uso
        deleted = delete_use_case.execute(presentacion_id)
        
        if not deleted:
            return jsonify({
                'success': False,
                'message': 'Presentación no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Presentación eliminada exitosamente'
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

