from typing import List
from app.models.conversion import Conversion


class ConversionRepository:
    def __init__(self):
        self._data: List[Conversion] = []

    def add(self, conversion: Conversion) -> None:
        self._data.append(conversion)

    def get_all(self) -> List[Conversion]:
        return list(reversed(self._data))

    def clear(self) -> None:
        self._data.clear()
