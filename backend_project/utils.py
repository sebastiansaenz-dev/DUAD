
from flask import jsonify, request
import logging
import traceback
from functools import wraps
from extensions import jwt_manager
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError


def error_response(message, status):
    return jsonify({
        'error': {
            'message': message
        }
    }), status


def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify('invalid token'), 400
        
        token = token.replace("Bearer ", "")

        decoded = jwt_manager.decode(token)

        if decoded is None:
            return jsonify('invalid token'), 403

        user_id = decoded.get('id')

        kwargs['current_user_id'] = user_id

        return func(*args, **kwargs)
    return wrapper


def require_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith("Bearer "):
            return jsonify('invalid token'), 400
        
        token = token.replace("Bearer ", "")

        decoded = jwt_manager.decode(token)

        if decoded is None:
            return jsonify('invalid token'), 403
        
        user_roles = decoded.get('roles')


        if 'admin' not in user_roles:
            return jsonify('invalid permissions'), 403

        
        return func(*args, **kwargs)
        
    return wrapper


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ex:
            return error_response(str(ex), 400)
        
        except ValidationError as ex:
            return error_response(ex.messages, 400)
        
        except TypeError as ex:
            return error_response(str(ex), 400)
        
        except HTTPException as ex:
            return error_response(ex.description, ex.code)
        
        except SQLAlchemyError as ex:
            return error_response('internal server error', 500)
        
        except Exception as ex:
            logging.error(f'unexpected error: {str(ex)}')
            logging.error(traceback.format_exc())
            return error_response('internal server error', 500)
    
    return wrapper
