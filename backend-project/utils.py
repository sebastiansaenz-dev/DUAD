from flask import jsonify
from datetime import datetime
import logging
import traceback


def error_response(message, status):
    return jsonify({
        'success': False,
        'error': {
            'message': message
        }
    }), status


def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ex:
            return error_response(str(ex), 400)
        except Exception as ex:
            logging.error(f'unexpected error: {str(ex)}')
            logging.error(traceback.format_exc())
            return error_response('internal server error', 500)
    
    return wrapper


def validate_int(value, field):
    try:
        return int(value)
    except:
        raise ValueError(f'{field} must be an integer')


def validate_date(value):
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return value
    except:
        raise ValueError('invalid date format')
