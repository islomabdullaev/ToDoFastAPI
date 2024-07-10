from datetime import datetime
from general import tashkent_tz
from pydantic import BaseModel

class AssignmentCreateSchema(BaseModel):
    title: str
    description: str
    priority: str
    created_at: datetime = datetime.now(tashkent_tz)
    