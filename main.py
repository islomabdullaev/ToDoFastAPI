import models
from fastapi import FastAPI
from database import Base, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="To Do Project")


@app.get('/')
async def get_data():
    return {
        "message": "Hello world"
    }
