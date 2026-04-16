from sqlalchemy import Column, String, Text, JSON, Boolean, Float, DateTime, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    ean = Column(String(13), primary_key=True)
    name = Column(Text, nullable=False)
    brand = Column(Text)
    ingredients_raw = Column(Text, nullable=False)
    ingredients_normalized = Column(JSONB)
    last_update = Column(DateTime, default=datetime.utcnow)
    data_quality = Column(String, default="manual")
    image_url = Column(Text)

class ProductIngredient(Base):
    __tablename__ = "product_ingredients"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_ean = Column(String(13), nullable=False)
    token_original = Column(Text, nullable=False)
    ingredient_norm = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    confidence = Column(Float, default=1.0)
    is_warning = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Dictionary(Base):
    __tablename__ = "dictionary"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    term = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    is_e_number = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ShelfMap(Base):
    __tablename__ = "shelf_map"
    shelf_id = Column(String, primary_key=True)
    store_id = Column(String, nullable=False)
    name = Column(Text)
    zone = Column(Text)
    products = Column(JSONB, nullable=False)
    last_verified_at = Column(DateTime, default=datetime.utcnow)
    confidence = Column(Float, default=0.9)