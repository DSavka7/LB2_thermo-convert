from datetime import datetime
from app.models.conversion import Conversion
from app.repositories.conversion_repo import ConversionRepository


class ConversionService:
    def __init__(self, repo: ConversionRepository):
        self.repo = repo

    def convert(self, celsius: float) -> Conversion:
        fahrenheit = round(celsius * 9 / 5 + 32, 2)

        conversion = Conversion(
            celsius=celsius,
            fahrenheit=fahrenheit,
            timestamp=datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        )

        self.repo.add(conversion)
        return conversion

    def get_history(self):
        return self.repo.get_all()

    def clear_history(self):
        self.repo.clear()