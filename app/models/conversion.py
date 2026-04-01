from pydantic import BaseModel


class Conversion(BaseModel):
    celsius: float
    fahrenheit: float
    timestamp: str
