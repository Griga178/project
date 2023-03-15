from sqlalchemy import Column, ForeignKey
from sqlalchemy import Text, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Project_table(Base):
    __tablename__ = "project_table"
    id = Column(Integer, primary_key = True)
    name = Column(Text)
