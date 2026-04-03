from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from app.db import Base

class Conversion(BaseModel):
    celsius: float
    fahrenheit: float
    timestamp: str

class DbConversion(Base):
    __tablename__ = "conversions"

    id = Column(Integer, primary_key=True, index=True)
    celsius = Column(Float)
    fahrenheit = Column(Float)
    timestamp = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))