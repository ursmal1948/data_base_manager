import sqlite3
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from models import Trip

load_dotenv()
db_name = os.getenv('DATABASE_NAME')


class DataLoader(ABC):

    @abstractmethod
    def load(self, source: str) -> list[str]:
        pass


class DbDataLoader(DataLoader):

    def load(self, source: str) -> list[Trip]:
        with sqlite3.connect(source) as conn:
            cursor = conn.cursor()
            sql = 'select * from trips'
            cursor.execute(sql)
            return [Trip(*row) for row in cursor.fetchall()]
