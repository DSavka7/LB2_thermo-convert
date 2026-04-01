from pydantic import BaseModel
from datetime import datetime


class Conversion(BaseModel):
    celsius: float
    fahrenheit: float
    timestamp: str