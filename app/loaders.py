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
            lines = [line.strip().split(';') for line in f.readlines()]
            return [TravelAgency(id=int(line[0]), name=line[1], city=line[2]) for line in lines]
