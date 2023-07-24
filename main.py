from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base, engine, Todo


# Model declaration: ToDoRequest Base Model
class ToDoRequest(BaseModel):
    task: str


# Create Database
Base.metadata.create_all(engine)

# FastAPI setup
app = FastAPI()


@app.get("/")
def root():
    return "todo"


@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoRequest):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    # create and instance of the ToDo database model
    todo = Todo(task=todo.task)
    # add it to session and commit
    session.add(todo)
    session.commit()
    # grad the id given
    todo_id = todo.id
    return f"Created a todo item with id:{todo_id}"


@app.get("/todo/{todo_id}")
def read_todo(todo_id: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    # make query
    todo = session.query(Todo).get(todo_id)
    # close session
    session.close()
    # exception handling
    if not todo:
        raise HTTPException(status_code=404, detail=f"Item not found {todo_id}")
    return f"Read specific todo with id:{todo.id} and task: {todo.task}"


@app.put("/todo/{todo_id}")
def update_todo(todo_id: int, task: str):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    # make query to get item from db
    todo = session.query(Todo).get(todo_id)
    # update item if exists
    if todo:
        todo.task = task
        session.commit()
    # close session
    session.close()
    # exception handling
    if not todo:
        raise HTTPException(status_code=404, detail=f"Item not found {todo_id}")
    return todo


@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    # make query to get item from db
    todo = session.query(Todo).get(todo_id)
    # delete item if exists
    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with {todo_id}")
    return None


@app.get("/todo")
def read_all_todo(todo_id: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    # make query
    todo_list = session.query(Todo).all()
    # close session
    session.close()
    return todo_list
