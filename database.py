from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# database_url = "sqlite:///./todo.db"
database_url = "postgresql://postgres:postgres@localhost/todo_db"

engine = create_engine(url=database_url)
SessionLocal =  sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
