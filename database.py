from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Database setup
engine = create_engine("sqlite:///todo.db")
Base = declarative_base()


# Table declaration
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    task = Column(String(50))
