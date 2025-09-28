from flask import Flask, request, jsonify
from flask.views import MethodView
from data import export_data, is_homework_in_list, check_valid_status
from logic import export_homework, import_homeworks
import secrets


class HomeworkAPI(MethodView):

    def __init__(self, manager):
        self.manager = manager


    def require_auth(func):
        def wrapper(self, *args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify(message='Unauthorized'), 401
            token = auth_header.split()[1]
            if token not in tokens:
                return jsonify(message='Unauthorized'), 401
            return func(self, *args, **kwargs)
        return wrapper

    @require_auth
    def get(self):
        hw_list = import_homeworks()
        title_filter = request.args.get('title')
        id_filter = request.args.get('id')

        if title_filter:
            hw_list = [hw for hw in hw_list if hw['title'] == title_filter]
        
        if id_filter:
            try:
                id_filter = int(id_filter)
            except ValueError:
                return jsonify(message='id must be an integer')

            hw_list = [hw for hw in hw_list if hw['id'] == id_filter]

        if title_filter and id_filter:
            return jsonify(message='only 1 filter can be accepted')
    
        return hw_list
    
    @require_auth
    def post(self):
        try:
            request_body = request.json
            
            if "title" not in request_body:
                raise ValueError('title missing from the body')

            if "description" not in request_body:
                raise ValueError('description missing from the body')
            
            if "status" not in request_body:
                request_body['status'] = 'not started'

            homeworks = import_homeworks()

            if not is_homework_in_list(request_body['title'], homeworks):
                if check_valid_status(request_body['status']):
                    new_homework = self.manager.create_homework(request_body['title'], request_body['description'], request_body['status'])
                    export_homework(new_homework)
                else:
                    return jsonify(message="status must be 'not started', 'on progress' or 'done'"), 400
            else:
                return jsonify(message='There is a homeworks with the same title')


            return jsonify(message="Homework created")
        except ValueError as ex:
            return jsonify(message=str(ex)), 400
        except Exception as ex:
            return jsonify(message=str(ex)), 500

    @require_auth
    def patch(self, id):
        try:
            request_body = request.json
            
            if "id" in request_body:
                return jsonify(message="field 'id' cannot be updated")
            
            allowed_fields = {"title", "description", "status"}
            invalid_fields = [k for k in request_body.keys() if k not in allowed_fields]

            if invalid_fields:
                return jsonify(message='only title, description and status fields are allowed')

            if check_valid_status(request_body['status']):
                homeworks = import_homeworks()
                for hw in homeworks:
                    if hw['id'] == id:
                        hw.update(request_body)
                        export_data(homeworks)
                        return jsonify(message='Homework updated')
            else:
                return jsonify(message="status must be 'not started', 'on progress' or 'done'"), 400
                
            return jsonify(message='homeworks not founded'), 400

        except Exception as ex:
            return jsonify(message=str(ex)), 500

    @require_auth
    def delete(self, id):
        try:

            homeworks = import_homeworks()

            for index, hw in enumerate(homeworks):
                if hw['id'] == id:
                    homeworks.pop(index)
                    export_data(homeworks)
                    return jsonify(message='Homework deleted')
                
            return jsonify(message='homeworks not founded'), 400
        
        except Exception as ex:
            return jsonify(message=str(ex))


tokens = {}
class LoginAPI(MethodView):

    users = {
        "admin": "1234"
    }


    def post(self):
        request_body = request.json
        username = request_body['username']
        password = request_body['password']

        if username in self.users and self.users[username] == password:
            token = secrets.token_hex(16)
            tokens[token] = username
            return jsonify(token=token)
        else:
            jsonify(message='invalid credentials'), 401

