from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Importiamo Base dal file models
from app.models import Base

# === DATABASE URL DI RAILWAY (hardcoded per POC) ===
DATABASE_URL = 
"postgresql://postgres:bjnoaSvAtwHUytGpFayWMWTwDzTqqPpJ@shortline.proxy.rlwy.net:57052/railway"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, 
bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Importiamo Base dal file models
from app.models import Base

# === DATABASE URL DI RAILWAY (hardcoded per POC) ===
DATABASE_URL = 
"postgresql://postgres:bjnoaSvAtwHUytGpFayWMWTwDzTqqPpJ@shortline.proxy.rlwy.net:57052/railway"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, 
bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
