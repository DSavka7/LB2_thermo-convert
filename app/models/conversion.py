from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String

from app.db import Base


# ── Pydantic schema (API responses & service layer) ──────────────────────────
class ConversionSchema(BaseModel):
    celsius: float
    fahrenheit: float
    timestamp: str

    class Config:
        from_attributes = True


# ── SQLAlchemy ORM model ─────────────────────────────────────────────────────
class DbConversion(Base):
    __tablename__ = "conversions"

    id = Column(Integer, primary_key=True, index=True)
    celsius = Column(Float)
    fahrenheit = Column(Float)
    timestamp = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))