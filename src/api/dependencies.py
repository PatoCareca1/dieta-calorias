from fastapi import Depends
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.database import get_db


def get_db() -> Session:
    """
    Dependency para fornecer uma sessão de DB e fechá-la depois.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
