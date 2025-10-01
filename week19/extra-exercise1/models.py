


class Homework:
    def __init__(self, id, title, description, status):
        self.id = id
        self.title = title
        self.description = description
        self.status = status

    def convert_to_dict(self):
        dic = {}

        dic["id"] = self.id
        dic["title"] = self.title
        dic["description"] = self.description
        dic["status"] = self.status

        return dic
    


class HomeworkManager:

    def __init__(self, start_id=0):
        self.id_counter = start_id


    def create_homework(self, title, description, status):
        new_homework = Homework(self.id_counter, title, description, status)
        self.id_counter += 1
        return new_homework.convert_to_dict()
    
