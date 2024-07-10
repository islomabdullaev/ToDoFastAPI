from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from datetime import datetime

class AssignmentTable(Base):
    __tablename__ = "assignment"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64))
    description = Column(String)
    priority = Column(String(16))
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
