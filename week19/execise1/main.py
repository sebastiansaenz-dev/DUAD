from flask import Flask, request, jsonify
from data import check_if_file_exists, export_data, is_homework_in_list, check_valid_status
from logic import export_homework, import_homeworks
from models import HomeworkManager


def setup_routes(app, manager):
    @app.route('/homeworks')
    def root():
        hw_list = import_homeworks()
        title_filter = request.args.get('title')
        id_filter = request.args.get('id')
        status_filter = request.args.get('status')

        if id_filter:
            try:
                id_filter = int(id_filter)
            except ValueError:
                return jsonify(message='id must be an integer')


        if title_filter or id_filter or status_filter:
            hw_list = [
                hw for hw in hw_list 
                if (title_filter and hw['title'] == title_filter) 
                or (id_filter and hw['id'] == id_filter) 
                or (status_filter and hw['status'] == status_filter)
            ]
            
    
        return hw_list

    @app.route('/homeworks', methods=["POST"])
    def crate_homework():
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
                    new_homework = manager.create_homework(request_body['title'], request_body['description'], request_body['status'])
                    export_homework(new_homework)
                else:
                    return jsonify(message="status must be 'not started', 'on progress' or 'done'"), 400
            else:
                return jsonify(message='There is a homeworks with the same title'), 400


            return jsonify(message="Homework created")
        except ValueError as ex:
            print(ex)
            return jsonify(message='there was an error'), 400
        except Exception as ex:
            return jsonify(message='there was an error'), 500
            
    @app.route('/homeworks/<int:id>', methods=["PATCH"])
    def update_homework(id):
        try:
            request_body = request.json
            
            if "id" in request_body:
                return jsonify(message="field 'id' cannot be updated")
            
            allowed_fields = {"title", "description", "status"}
            invalid_fields = [k for k in request_body.keys() if k not in allowed_fields]

            if invalid_fields:
                return jsonify(message='only title, description and status fields are allowed')


            if "status" in request_body:
                if not check_valid_status(request_body['status']):
                    return jsonify(message="status must be 'not started', 'on progress' or 'done'"), 400

            homeworks = import_homeworks()
            for hw in homeworks:
                if hw['id'] == id:
                    hw.update(request_body)
                    export_data(homeworks)
                    return jsonify(message='Homework updated')
                
            return jsonify(message='homeworks not founded'), 400

        except Exception as ex:
            return jsonify(message='there was an error'), 500
        
    @app.route('/homeworks/<int:id>', methods=["DELETE"])
    def delete_homework(id):
        try:

            homeworks = import_homeworks()

            for index, hw in enumerate(homeworks):
                if hw['id'] == id:
                    homeworks.pop(index)
                    export_data(homeworks)
                    return jsonify(message='Homework deleted')
                
            return jsonify(message='homeworks not founded'), 400
        
        except Exception as ex:
            return jsonify(message='there was an error')



def main():

    existing_homeworks = import_homeworks()
    if existing_homeworks:
        max_id = max(hw['id'] for hw in existing_homeworks) + 1
    else:
        max_id = 0

    app = Flask(__name__)
    manager = HomeworkManager(max_id)
    setup_routes(app, manager)
    return app

if __name__ == '__main__':
    check_if_file_exists("./homeworks.json")
    app = main()
    app.run(host='localhost', debug=True)