import models
from fastapi import APIRouter, Depends, HTTPException, Path, status, Response
from sqlalchemy.orm import Session
from general import get_session
from schemas import AssignmentCreateSchema, AssignmentEditSchema, AssignmentPriorityEditSchema, UserSchema
from utils import JWTBearer
from sqlalchemy import select


router = APIRouter(
    prefix="/assignments",
    tags=["assignments"])


@router.get('', status_code=status.HTTP_200_OK)
async def get_assignments(
        user: UserSchema = Depends(JWTBearer()),
        session: Session = Depends(get_session)):
    if user.role != "pm":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
            "message": "You are not permitted"
        })
    assignments = session.execute(select(models.AssignmentTable)).all()
    print(assignments)
    return assignments

@router.post('', status_code=status.HTTP_201_CREATED)
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


@router.get('/{assignment_id}', status_code=status.HTTP_200_OK)
async def get_assignment(
        assignment_id: int = Path(gt=0),
        session: Session = Depends(get_session)):
    assignment = session.query(models.AssignmentTable).filter(
        models.AssignmentTable.id == assignment_id).first()
    if assignment is not None:
        return assignment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found !")


@router.put('/{assignment_id}', status_code=status.HTTP_201_CREATED)
async def update_assignment(
    data: AssignmentEditSchema,
    assignment_id: int = Path(gt=0),
    session: Session = Depends(get_session)):
    assignment = session.query(models.AssignmentTable).filter(
        models.AssignmentTable.id == assignment_id).first()
    if assignment is not None:
        assignment.title = data.title
        assignment.description = data.description
        assignment.is_completed = data.is_completed
        session.add(assignment)
        session.commit()
        session.refresh(assignment)
        return assignment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found !")


@router.patch('/{assignment_id}', status_code=status.HTTP_201_CREATED)
async def update_assignment(
    data: AssignmentPriorityEditSchema,
    assignment_id: int = Path(gt=0),
    session: Session = Depends(get_session)):
    assignment = session.query(models.AssignmentTable).filter(
        models.AssignmentTable.id == assignment_id).first()
    if assignment is not None:
        assignment.priority = data.priority
        session.add(assignment)
        session.commit()
        session.refresh(assignment)
        return assignment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found !")

@router.delete('/{assignment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_assignment(
    assignment_id: int = Path(gt=0),
    session: Session = Depends(get_session)
    ):
    assignment = session.query(models.AssignmentTable).filter(
        models.AssignmentTable.id == assignment_id).first()
    if assignment is not None:
        session.delete(assignment)
        session.commit()
        return Response(content="Deleted!", status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found !")
