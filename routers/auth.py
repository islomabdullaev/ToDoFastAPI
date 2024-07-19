import models
from fastapi import APIRouter, Depends, HTTPException, Response

from schemas import UserCreateSchema
from utils import hash_password
from general import get_session
from sqlalchemy.orm import Session
from starlette import status
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated

SECRET_KEY = "631c915424288e2b5e505f5a363d3b62131a2176fbbfb1b81b3c269df2dea6d6"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

router = APIRouter(
    prefix="/auth",
    tags=["auth"])


@router.post("/signin")
async def signin(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = autnetuicated_user(data.username, password)
    return {
        "user": "Authenticated !"
    }


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
        data: UserCreateSchema,
        session: Session = Depends(get_session)):
    try:
        hashed_password = hash_password(password=data.password)
        user = models.UserTable(
            first_name=data.first_name,
            last_name=data.last_name,
            username=data.username,
            email=data.email,
            password=hashed_password
        )
        session.add(user)
        session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "User with username or email already registered !"
            })

    return {
        "message": "Created Successfully !"
    }