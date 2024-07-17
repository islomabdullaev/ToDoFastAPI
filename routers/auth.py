import models
from fastapi import APIRouter, Depends

from schemas import UserCreateSchema
from utils import hash_password
from general import get_session
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter(
    prefix="/auth",
    tags=["auth"])


@router.post("/signin")
async def signin():
    return {
        "user": "Authenticated !"
    }


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
        data: UserCreateSchema,
        session: Session = Depends(get_session)):
    user = models.UserTable(
        first_name=data.first_name,
        last_name=data.last_name,
        username=data.username,
        email=data.email,
        password=hash_password(password=data.password)
    )
    session.add(user)
    session.commit()

    return data