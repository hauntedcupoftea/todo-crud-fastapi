from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from api import models, schemas, oauth
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# provides util for hashing and verifying passwords using bcrypt.
class Hash():
    def bcrypt(password: str):
        return pwd_context.hash(password)
    
    def verify(hashed_password, plain_password):
        return pwd_context.verify(plain_password, hashed_password)

# create a new user in the database
def create_user(request: schemas.Todo, db: Session):
    """
    Creates a new user in the database using the provided user information.
    
    :param request: The `request` parameter is of type `schemas.Todo`, which likely contains the data
    needed to create a new user, such as the user's name, email, and password
    :type request: schemas.Todo
    :param db: The `db` parameter in the `create_user` function is typically a database session object
    that allows you to interact with the database. In this case, it seems to be an instance of a
    database session class that is used to perform database operations such as adding new records,
    committing transactions, and refreshing
    :type db: Session
    :return: The function `create_user` is returning the newly created user object after adding it to
    the database, committing the transaction, and refreshing the object from the database.
    """
    new_user = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # needed for orm
    return new_user

def get_user(id:int, db: Session):
    """
    Retrieves a user from the database based on the provided ID.
    
    :param id: The `id` parameter is an integer representing the unique identifier of the user that we
    want to retrieve from the database
    :type id: int
    :param db: The `db` parameter in the `get_user` function is of type `Session`. It is likely
    referring to a database session object that is used to interact with the database. This session
    object is used to query the database for a specific user based on the provided `id`
    :type db: Session
    :return: The function `get_user` is returning the user object from the database that matches the
    provided `id`. If no user is found with the given `id`, it raises an HTTPException with a status
    code of 404 (Not Found) and a detail message indicating that the user with that specific id was not
    found.
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with that id {id} not found")
    return user

def get_all(db: Session):
    """
    Retrieves all Todo items from the database using the provided SQLAlchemy
    Session.
    
    :param db: Session
    :type db: Session
    :return: A list of all Todo objects from the database is being returned.
    """
    todos = db.query(models.Todo).all()
    return todos


def create(request: schemas.Todo, db: Session):
    """
    Creates a new todo item in the database based on the provided request data.
    
    :param request: schemas.Todo
    :type request: schemas.Todo
    :param db: The `db` parameter in the `create` function is an instance of a database session. It is
    used to interact with the database, such as adding new records, committing changes, and refreshing
    objects. In this case, it is being used to create a new `Todo` record in the database
    :type db: Session
    :return: The `create` function is returning the newly created `Todo` object that was added to the
    database.
    """
    new_todo = models.Todo(title = request.title, desc = request.desc, user_id = 1)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo) # needed for orm
    return new_todo


def destroy(id:int, db: Session):
    """
    Deletes a todo task from a database by its ID if it exists, raising a 404 error
    if the task is not found.
    
    :param id: The `id` parameter is an integer that represents the unique identifier of the task that
    needs to be deleted from the database
    :type id: int
    :param db: The `db` parameter is of type `Session`, which is likely an instance of a database
    session that allows interaction with the database. In this context, it is used to query and delete a
    `Todo` item with a specific `id` from the database
    :type db: Session
    """
    todo = db.query(models.Todo).filter(models.Todo.id == id)
    if not todo.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with that id {id} not found")
    todo.delete(synchronize_session=False)
    db.commit()


def update(id:int, request: schemas.Todo, db:Session):
    """
    Updates a Todo task in a database based on the provided ID and request data.
    
    :param id: The `id` parameter is an integer representing the unique identifier of the todo task that
    needs to be updated in the database
    :type id: int
    :param request: The `request` parameter in the `update` function is of type `schemas.Todo`. It
    likely represents the data that is being sent in the request to update a todo item. This data is
    used to update the corresponding todo item in the database
    :type request: schemas.Todo
    :param db: The `db` parameter in the `update` function is an instance of a database session. It is
    used to interact with the database to perform operations like querying and updating data. In this
    case, it is being used to query the `Todo` model based on the provided `id`, check if
    :type db: Session
    """
    todo = db.query(models.Todo).filter(models.Todo.id == id)
    if not todo.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with that id {id} not found")
    todo.update(request.model_dump())
    db.commit()


def show(id:int, db:Session):
    """
    Retrieves a todo task from the database based on the provided ID and raises a 404
    error if the task is not found.
    
    :param id: The `id` parameter is an integer that represents the unique identifier of a task in the
    database. It is used to query the database for a specific task with the matching identifier
    :type id: int
    :param db: The `db` parameter is of type `Session`, which is likely an instance of a database
    session that allows you to interact with the database. In this context, it is used to query the
    database for a specific `Todo` item based on the provided `id`
    :type db: Session
    :return: the Todo object with the specified id from the database. If a Todo with the given id is not
    found in the database, it raises an HTTPException with a status code of 404 and a message indicating
    that the task with that id was not found.
    """
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with that id {id} not found")
    return todo