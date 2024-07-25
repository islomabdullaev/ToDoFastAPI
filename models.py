from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database import Base
from datetime import datetime
from general import tashkent_tz



class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128), unique=True)
    username = Column(String(36), unique=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    password = Column(String())
    is_active = Column(Boolean, default=True)
    role = Column(String(24))
    created_at = Column(DateTime, nullable=False, default=datetime.now(tz=tashkent_tz))
    updated_at = Column(DateTime, onupdate=datetime.now(tz=tashkent_tz))

class AssignmentTable(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64))
    description = Column(String)
    priority = Column(String(16))
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(tz=tashkent_tz))
    updated_at = Column(DateTime, onupdate=datetime.now(tz=tashkent_tz))
    user_id = Column(Integer, ForeignKey("users.id"))
