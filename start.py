from sql_tables import Project_table, engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


DBSession = sessionmaker(bind = engine)
session = DBSession()


class Project():
    exist_project = [] # query to all proj

    def __init__(self, name):
        table_object = Project_table(name = name)
        session.add(table_object)
        session.commit()
        self.table_object = table_object
        Project.exist_project.append(self)

class User():
    def __init__(self, name):
        self.name = name

class Subject():
    def __init__(self, name):
        self.name = name

class Tasks():
    def __init__(self):
        self.tasks = []
    def chose_maker(self, users):
        # show_users()
        # chose_user()
    def chose_task(self):
        pass
    def create_last_date(self):
        pass
    def edit_task(self):
        pass

class ToBuy():
    def __init__(self, user):
        self.subjects = []
    def chose_subject(self):
        # show_subjects()
        # create_subject()

        self.subjects.append(subject)
