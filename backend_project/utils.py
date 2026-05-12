
from flask import jsonify
import logging
import traceback
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException, Forbidden
from marshmallow import ValidationError
from redis import RedisError
import json
import hashlib
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_jwt_extended.exceptions import RevokedTokenError
import inspect


def error_response(message, status):
    return jsonify({
        'error': {
            'message': message
        }
    }), status


def require_auth(role=None):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):

            claims = get_jwt()
            user_roles = claims.get('roles', [])

            if role and role not in user_roles:
                raise Forbidden('Invalid permissions')
            
            sig = inspect.signature(func)

            if 'current_user_id' in sig.parameters:
                kwargs['current_user_id'] = get_jwt_identity()

            if 'current_user_roles' in sig.parameters:
                kwargs['current_user_roles'] = user_roles

            return func(*args, **kwargs)
        return wrapper
    return decorator


def generate_filters_hash(filters):
    if not filters:
        return None
    
    filters_sorted = json.dumps(filters, sort_keys=True, separators=(',', ':'))

    return hashlib.md5(filters_sorted.encode('utf-8')).hexdigest()


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except RevokedTokenError as ex:
            return error_response(str(ex), 401)

        except ValueError as ex:
            return error_response(str(ex), 400)
        
        except ValidationError as ex:
            return error_response(ex.messages, 400)
        
        except TypeError as ex:
            return error_response(str(ex), 400)
        
        except HTTPException as ex:
            return error_response(ex.description, ex.code)
        
        except RedisError as ex:
            return error_response(str(ex), 400)
        
        except SQLAlchemyError as ex:
            return error_response('internal server error', 500)
        
        except Exception as ex:
            logging.error(f'unexpected error: {str(ex)}')
            logging.error(traceback.format_exc())
            return error_response('internal server error', 500)
    
    return wrapper
