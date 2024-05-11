from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api import schemas, models, oauth
import api.functions as func

user = APIRouter(
    prefix="/user",
    tags=['users']
)

auth = APIRouter(
        tags=['Authentication'] 
)

todo = APIRouter(
    prefix="/todo",
    tags=['todos']  
)


get_db = models.get_db

# CREATE USER ROUTES FROM PREDEFINED FUNCTIONS
# create new user
@user.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: schemas.User, db:Session = Depends(get_db)):
    return func.create_user(request, db)

# get user info
@user.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id:int, db: Session = Depends(get_db)):
    return func.get_user(id, db)

# CREATE SEPERATE AUTHENTICATION ROUTE
# this handles login and session access tokens
@auth.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user: # user not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not func.Hash.verify(user.password, request.password): # password does not match
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")
    access_token = oauth.create_access_token(data={"sub": user.email}) # oauth2 does this
    return {"access_token": access_token, "token_type": "bearer"}

# CREATE TO-DO ROUTES FOR PREDEFINED FUNCTIONS
# get all tasks from current user
@todo.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowTodo])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return func.get_all(db)

# create new task
@todo.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Todo, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return func.create(request, db)

# filter tasks
@todo.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowTodo)
def read_one(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return func.show(id, db)

# delete a task
@todo.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destory(id:int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return func.destroy(id, db)

# update a task
@todo.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: schemas.Todo, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth.get_current_user)):
    return func.update(id, request, db)