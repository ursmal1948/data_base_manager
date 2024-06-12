import sqlite3
from dataclasses import dataclass
from decimal import Decimal
from typing import Self
from config import db_name


@dataclass
class Trip:
    DB_NAME = db_name

    id_: int | None = None
    destination: str | None = None
    price: Decimal | None = Decimal('0.00')
    tourists_number: int | None = 0
    agency_id: int | None = None

    def __hash__(self):
        return hash((self.id_,))

    def __eq__(self, other):
        return isinstance(other, Trip) and self.id_ == other.id_

    # def __repr__(self):
    #     return str(self)
    #
    # def __str__(self):
    #     return (f'destination {self.destination} price: {self.price} tourists: {self.tourists_number} '
    #             f'agency:{self.agency_id}')

    @classmethod
    def _from_db(cls, trip_data: tuple[str | int]) -> Self:
        return cls(
            id_=trip_data[0],
            destination=trip_data[1],
            price=Decimal(trip_data[2]),
            tourists_number=trip_data[3],
            agency_id=trip_data[4]
        )

    @staticmethod
    def find_all() -> list['Trip']:
        with sqlite3.connect(Trip.DB_NAME) as conn:
            cursor = conn.cursor()
            sql = 'select * from trips'
            cursor.execute(sql)
            return [Trip._from_db(row) for row in cursor.fetchall()]

    @staticmethod
    def find_all_by_agency_id(agency_id: int) -> list['Trip']:
        with sqlite3.connect(Trip.DB_NAME) as conn:
            cursor = conn.cursor()
            sql = f'select * from trips where agency_id={agency_id}'
            cursor.execute(sql)
            return [Trip._from_db(row) for row in cursor.fetchall()]

    @classmethod
    def find_by_id(cls, id_: int) -> 'Trip':
        with sqlite3.connect(Trip.DB_NAME) as connection:
            cursor = connection.cursor()
            sql = f'select * from trips where id={id_}'
            cursor.execute(sql)
            res = cursor.fetchone()
            return Trip._from_db(res) if res else None

    @staticmethod
    def insert(trip: 'Trip') -> int:
        with sqlite3.connect(Trip.DB_NAME) as connection:
            cursor = connection.cursor()
            sql = ('insert into trips (destination, price, tourists_number, agency_id) '
                   'values (?, ?, ?, ?)')
            cursor.execute(sql, (trip.destination, str(trip.price), trip.tourists_number, trip.agency_id))
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def insert_many(trips: list['Trip']) -> int:
        with sqlite3.connect(Trip.DB_NAME) as connection:
            cursor = connection.cursor()
            sql = ('insert into trips (destination, price, tourists_number, agency_id) '
                   'values (?, ?, ?, ?)')

            cursor.executemany(sql,
                               [(trip.destination, str(trip.price), trip.tourists_number, trip.agency_id) for trip in
                                trips])
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def delete_by_id(id_: int) -> int:
        with sqlite3.connect(Trip.DB_NAME) as connection:
            cursor = connection.cursor()
            sql = f'delete from trips where id={id_}'
            cursor.execute(sql)
            connection.commit()
            return id_

    @staticmethod
    def delete_all() -> None:
        with sqlite3.connect(Trip.DB_NAME) as connection:
            cursor = connection.cursor()
            sql = 'delete from trips where id > 0'
            cursor.execute(sql)
            connection.commit()




@dataclass
class TravelAgency:
    id: int
    name: str
    city: str

    def __eq__(self, other):
        return isinstance(other,
                          TravelAgency) and self.id == other.id

    def __hash__(self):
        return hash((self.id,))

    @classmethod
    def from_string(cls, line: str) -> Self:
        id_, name, city = line.strip().split(';')
        return cls(id=int(id_), name=name, city=city)

    @staticmethod
    def get_all_agencies(filename: str) -> list['TravelAgency']:
        with open(filename, 'r') as f:
            return [TravelAgency.from_string(row) for row in f.readlines()]

    @staticmethod
    def delete_all_agencies(filename: str) -> None:
        with open(filename, 'w'):
            pass

    @staticmethod
    def _get_last_travel_agency_id(filename: str) -> int:
        with open(filename, 'r') as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1]
                return int(last_line[0])

    @staticmethod
    def add_travel_agency(filename: str, name: str, city: str) -> None:
        with open(filename, 'a') as f:
            id_ = TravelAgency._get_last_travel_agency_id(filename)
            travel_agency_id = id_ + 1 if id_ else 1
            new_agency_data = ';'.join([str(travel_agency_id), name, city])
            f.write('\n' + new_agency_data if travel_agency_id != 1 else new_agency_data)
