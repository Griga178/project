from sql_tables.tables import (
    Base,
    Project_table
)
from sqlalchemy import MetaData, create_engine
DATA_BASE_PATH = 'sqlite:///C:/Users/black_pc/Desktop/my_project.db'

metadata = MetaData()
engine = create_engine(f'{DATA_BASE_PATH}?check_same_thread=False')
Base.metadata.create_all(engine)
