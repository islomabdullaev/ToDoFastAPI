import models
from fastapi import APIRouter, Depends, HTTPException, Response

from schemas import UserCreateSchema
from utils import create_access_token, hash_password, bcrypt_context
from general import get_session
from sqlalchemy.orm import Session
from starlette import status
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated

router = APIRouter(
    prefix="/auth",
    tags=["auth"])


async def authenticate_user(username: str, password: str, session: Session):
    user = session.query(models.UserTable).filter(models.UserTable.username == username).first()
    if user is None:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    else:
        return user


@router.post("/signin")
async def signin(
        data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(get_session)):
    user = await authenticate_user(username=data.username, password=data.password, session=session)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "message": "User not found !"
        })
    token = create_access_token(username=user.username, user_id=user.id)
    return {
        "token": token,
        "type": "Bearer"
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