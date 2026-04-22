from datetime import datetime
from sqlalchemy.orm import Session

from app.models.conversion import ConversionSchema
from app.repositories.conversion_repo import ConversionRepository
from app.utils.temperature import celsius_to_fahrenheit


class ConversionService:
    def __init__(self, repo: ConversionRepository):
        self.repo = repo

    def convert(self, celsius: float, db: Session, user_id: int) -> ConversionSchema:
        schema = ConversionSchema(
            celsius=celsius,
            fahrenheit=celsius_to_fahrenheit(celsius),
            timestamp=datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        )
        self.repo.add(schema, db, user_id)
        return schema

    def get_history(self, db: Session, user_id: int) -> list[ConversionSchema]:
        return self.repo.get_all(db, user_id)

    def clear_history(self, db: Session, user_id: int) -> None:
        self.repo.clear(db, user_id)