from typing import List
from app.models.conversion import Conversion


class ConversionRepository:
    def __init__(self):
        self._data: List[Conversion] = []

    def add(self, conversion: Conversion):
        self._data.append(conversion)

    def get_all(self) -> List[Conversion]:
        return self._data

    def clear(self):
        self._data.clear()