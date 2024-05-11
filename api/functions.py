from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from api import models, schemas, oauth
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str):
        return pwd_context.hash(password)
    
    def verify(hashed_password, plain_password):
        return pwd_context.verify(plain_password, hashed_password)

def create_user(request: schemas.Todo, db: Session):
    # hashedPassword = pwd_context.hash(request.password)
    new_user = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(id:int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with that id {id} not found")
    return user

def get_all(db: Session):
    todos = db.query(models.Todo).all()
    return todos


def create(request: schemas.Todo, db: Session):
    new_todo = models.Todo(title = request.title, desc = request.desc, user_id = 1)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


def destroy(id:int, db: Session):
    todo = db.query(models.Todo).filter(models.Todo.id == id)
    if not todo.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with that id {id} not found")
    todo.delete(synchronize_session=False)
    db.commit()


def update(id:int, request: schemas.Todo, db:Session):
    todo = db.query(models.Todo).filter(models.Todo.id == id)
    if not todo.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with that id {id} not found")
    todo.update(request.model_dump())
    db.commit()


def show(id:int, db:Session):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with that id {id} not found")
    return todo