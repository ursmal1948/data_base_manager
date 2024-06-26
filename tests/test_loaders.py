import unittest
from config import test_db_name
from app.loaders import TxtDataLoader, DbDataLoader
from app.model import Trip, TravelAgency
from alembic.config import Config
from alembic import command
from tests.test_model import Trips


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
        cls.db_path = test_db_name
        alembic_cfg = Config('alembic.ini')
        command.downgrade(alembic_cfg, 'base')
        command.upgrade(alembic_cfg, 'head')

    def test_loader(self):
        db_data_loader = DbDataLoader()
        expected_trips = db_data_loader.load(self.db_path)
        trips = [Trips.TRIP_1, Trips.TRIP_2]
        self.assertEqual(trips, expected_trips)
