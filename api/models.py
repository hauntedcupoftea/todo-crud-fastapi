from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

values = dotenv_values('./test.env')
SQLALCHEMY_DATABASE_URL = values['DB_CONNECTION']

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()

class Todo(Base):
    __tablename__ = "todo_table"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(25))
    desc = Column(String(100))
    user_id = Column(Integer, ForeignKey('user_table.id'))
    creator = relationship("User", back_populates="todo_table")

class User(Base):
    __tablename__ = "user_table"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    todo_table = relationship("Todo", back_populates="creator")