import pytz
from database import SessionLocal

tashkent_tz = pytz.timezone("Asia/Tashkent")

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
