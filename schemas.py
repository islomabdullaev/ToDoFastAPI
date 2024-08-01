from datetime import datetime
from general import tashkent_tz
from pydantic import BaseModel

class AssignmentCreateSchema(BaseModel):
    title: str
    description: str
    priority: str
    created_at: datetime = datetime.now(tashkent_tz)


class AssignmentEditSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool


class AssignmentPriorityEditSchema(BaseModel):
    priority: str


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    role: str
    phone: str | None = None


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    role: str
    phone: str | None = None