from flask import Flask
from data import check_if_file_exists
from logic import import_homeworks
from models import HomeworkManager
from views import HomeworkAPI, LoginAPI




def main():

    existing_homeworks = import_homeworks()
    if existing_homeworks:
        max_id = max(hw['id'] for hw in existing_homeworks) + 1
    else:
        max_id = 0

    app = Flask(__name__)
    manager = HomeworkManager(max_id)

    homework_view = HomeworkAPI.as_view('homework_api', manager=manager)
    login_view = LoginAPI.as_view('login_api')

    app.add_url_rule('/homeworks', view_func=homework_view, methods=["GET", "POST"])
    app.add_url_rule('/homeworks/<int:id>', view_func=homework_view, methods=['PATCH', 'DELETE'])
    app.add_url_rule('/login', view_func=login_view, methods=["POST"])

    return app

if __name__ == '__main__':
    check_if_file_exists("./homeworks.json")
    app = main()
    app.run(host='localhost', port=5001, debug=True)