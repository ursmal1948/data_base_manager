import unittest
from config import DB_NAME
import pytest
from app.loaders import TxtDataLoader, DbDataLoader
from app.model import Trip, TravelAgency
from alembic.config import Config
from alembic import command
from decimal import Decimal


class TestTxtLoader:
    def test_loader(self):
        txt_data_loader = TxtDataLoader()
        expected_travel_agencies = txt_data_loader.load('data/test_travel_agencies.txt')
        travel_agencies = [
            TravelAgency(id=1, name='HORIZON', city='WARSSSSAW'),
            TravelAgency(id=2, name='VOYAGER EXPERT', city='MALAGA'),
            TravelAgency(id=3, name='ADVENTURES TRAVEL', city='LISBONA')
        ]
        assert travel_agencies == expected_travel_agencies


class TestDbLoader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = DB_NAME
        alembic_cfg = Config('alembic.ini')
        command.downgrade(alembic_cfg, 'base')
        command.upgrade(alembic_cfg, 'head')

    def test_loader(self):
        db_data_loader = DbDataLoader()
        expected_trips = db_data_loader.load(self.db_path)
        trips = [
            Trip(id_=1, destination='USA', price=Decimal('1000'), tourists_number=30, agency_id=1),
            Trip(id_=2, destination='EGIPT', price=Decimal('500'), tourists_number=150, agency_id=2)
        ]
        self.assertEqual(trips, expected_trips)
