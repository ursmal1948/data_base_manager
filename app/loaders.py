import sqlite3
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from models import Trip, TravelAgency
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
            print(lines)
            return [TravelAgency(*line) for line in lines]
