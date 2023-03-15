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
