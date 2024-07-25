from fastapi.security import OAuth2PasswordBearer
import pytz
from database import SessionLocal

tashkent_tz = pytz.timezone("Asia/Tashkent")
SECRET_KEY = "631c915424288e2b5e505f5a363d3b62131a2176fbbfb1b81b3c269df2dea6d6"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
