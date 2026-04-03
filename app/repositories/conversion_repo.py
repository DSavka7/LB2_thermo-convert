from typing import List
from sqlalchemy.orm import Session

from app.models.conversion import Conversion, DbConversion

class ConversionRepository:
    def add(self, conversion: Conversion, db: Session, user_id: int) -> None:
        db_conversion = DbConversion(
            celsius=conversion.celsius,
            fahrenheit=conversion.fahrenheit,
            timestamp=conversion.timestamp,
            user_id=user_id,
        )
        db.add(db_conversion)
        db.commit()
        db.refresh(db_conversion)

    def get_all(self, db: Session, user_id: int) -> List[Conversion]:
        db_conversions = db.query(DbConversion).filter(DbConversion.user_id == user_id).order_by(DbConversion.id.desc()).all()
        return [
            Conversion(
                celsius=c.celsius,
                fahrenheit=c.fahrenheit,
                timestamp=c.timestamp,
            )
            for c in db_conversions
        ]

    def clear(self, db: Session, user_id: int) -> None:
        db.query(DbConversion).filter(DbConversion.user_id == user_id).delete()
        db.commit()