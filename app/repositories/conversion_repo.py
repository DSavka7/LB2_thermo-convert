from typing import List
from sqlalchemy.orm import Session

from app.models.conversion import ConversionSchema, DbConversion


class ConversionRepository:
    def add(self, schema: ConversionSchema, db: Session, user_id: int) -> None:
        record = DbConversion(
            celsius=schema.celsius,
            fahrenheit=schema.fahrenheit,
            timestamp=schema.timestamp,
            user_id=user_id,
        )
        db.add(record)
        db.commit()
        db.refresh(record)

    def get_all(self, db: Session, user_id: int) -> List[ConversionSchema]:
        records = (
            db.query(DbConversion)
            .filter(DbConversion.user_id == user_id)
            .order_by(DbConversion.id.desc())
            .all()
        )
        return [
            ConversionSchema(celsius=r.celsius, fahrenheit=r.fahrenheit, timestamp=r.timestamp)
            for r in records
        ]

    def clear(self, db: Session, user_id: int) -> None:
        db.query(DbConversion).filter(DbConversion.user_id == user_id).delete()
        db.commit()