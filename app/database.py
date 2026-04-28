from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app.models import Base

# DATABASE_URL hardcoded di Railway
DATABASE_URL = "postgresql://postgres:bjnoaSvAtwHUytGpFayWMWTwDzTqqPpJ@shortline.proxy.rlwy.net:57052/railway"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
