import models
from fastapi import FastAPI, Depends
from database import engine
from sqlalchemy.orm import Session
from general import get_session
from schemas import AssignmentCreateSchema

models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="To Do Project")


@app.get('/assignments')
async def get_assignments(session: Session = Depends(get_session)):
    assignments = session.query(models.AssignmentTable).all()
    return {
        "assignments": assignments
    }

@app.post('/assignments')
async def create_assignment(
    data: AssignmentCreateSchema,
    session: Session = Depends(get_session)):
    assignment = models.AssignmentTable(
        title=data.title,
        description=data.description,
        priority=data.priority,
        created_at=data.created_at
    )
    session.add(assignment)
    session.commit()
    session.refresh(assignment)

    return assignment