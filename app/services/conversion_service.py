from datetime import datetime
from app.models.conversion import Conversion
from app.repositories.conversion_repo import ConversionRepository
from sqlalchemy.orm import Session

class ConversionService:
    def __init__(self, repo: ConversionRepository):
        self.repo = repo

    def convert(self, celsius: float, db: Session, user_id: int) -> Conversion:
        fahrenheit = round(celsius * 9 / 5 + 32, 2)
        conversion = Conversion(
            celsius=celsius,
            fahrenheit=fahrenheit,
            timestamp=datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        )
        self.repo.add(conversion, db, user_id)
        return conversion

    def get_history(self, db: Session, user_id: int) -> list:
        return self.repo.get_all(db, user_id)

    def clear_history(self, db: Session, user_id: int) -> None:
        self.repo.clear(db, user_id)