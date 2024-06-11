import sqlite3
from abc import ABC, abstractmethod
from app.model import Trip, TravelAgency
from typing import Any


class DataLoader(ABC):

    @abstractmethod
    def load(self, source: str) -> list[Any]:
        pass


class DbDataLoader(DataLoader):

    def load(self, source: str) -> list[Any]:
        with sqlite3.connect(source) as conn:
            cursor = conn.cursor()
            sql = 'select * from trips'
            cursor.execute(sql)
            return [Trip(*row) for row in cursor.fetchall()]


class TxtDataLoader(DataLoader):

    def load(self, source: str) -> list[Any]:
        with open(source, 'r') as f:
            return [TravelAgency.from_string(line) for line in f.readlines()]
