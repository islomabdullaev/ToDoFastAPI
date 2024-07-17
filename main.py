import models
from fastapi import FastAPI
from database import engine
from routers import assignment, auth


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="To Do Project")

app.include_router(router=auth.router)
app.include_router(router=assignment.router)