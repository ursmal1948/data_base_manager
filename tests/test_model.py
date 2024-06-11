import unittest
from config import test_db_name
from app.model import Trip, TravelAgency
from decimal import Decimal
from alembic.config import Config
from alembic import command


class Trips:
    TRIP_1 = Trip(id_=1, destination='USA', price=Decimal('1000'), tourists_number=30, agency_id=1)
    TRIP_2 = Trip(id_=2, destination='EGIPT', price=Decimal('500'), tourists_number=150, agency_id=2)


class TestTripCrudOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Trip.DB_NAME = test_db_name

    def setUp(self):
        alembic_cfg = Config('alembic.ini')
        command.downgrade(alembic_cfg, 'base')
        command.upgrade(alembic_cfg, 'head')

    def test_find_all(self):
        trips = Trip.find_all()
        expected_trips = [Trips.TRIP_1, Trips.TRIP_2]
        self.assertEqual(trips, expected_trips)

    def test_find_by_id(self):
        trip = Trip.find_by_id(1)
        expected_trip = Trips.TRIP_1
        self.assertEqual(trip, expected_trip)

    def test_find_all_by_agency_id(self):
        trips = Trip.find_all_by_agency_id(2)[0]
        expected_trip = Trips.TRIP_2
        self.assertEqual(trips, expected_trip)

    def test_insert(self):
        initial_numbers_of_trips = len(Trip.find_all())
        new_trip = Trip(destination='AUSTRALIA', price=Decimal('300'), tourists_number=20, agency_id=1)
        inserted_id = Trip.insert(new_trip)
        expected_trip = Trip(id_=3, destination='AUSTRALIA', price=Decimal('300'), tourists_number=20, agency_id=1)
        trip_from_db = Trip.find_by_id(inserted_id)
        self.assertEqual(trip_from_db, expected_trip)
        self.assertEqual(len(Trip.find_all()), initial_numbers_of_trips + 1)
        self.assertEqual(inserted_id, 3)

    def test_insert_many(self):
        initial_number_of_trips = len(Trip.find_all())
        new_trips = [
            Trip(destination='JAPAN', price=Decimal('200'), tourists_number=150, agency_id=2),  # 3
            Trip(destination='SPAIN', price=Decimal('100'), tourists_number=300, agency_id=1)  # 4
        ]
        Trip.insert_many(new_trips)
        self.assertEqual(len(Trip.find_all()), initial_number_of_trips + len(new_trips))
        trip_one_from_db = Trip.find_by_id(3)
        trip_two_from_db = Trip.find_by_id(4)
        self.assertEqual(new_trips[0].destination, trip_one_from_db.destination)
        self.assertEqual(new_trips[1].destination, trip_two_from_db.destination)

    def test_delete(self):
        initial_number_of_trips = len(Trip.find_all())
        trip_id_to_delete = 1
        id_of_deleted_trip = Trip.delete_by_id(trip_id_to_delete)
        self.assertEqual(len(Trip.find_all()), initial_number_of_trips - 1)
        self.assertEqual(id_of_deleted_trip, 1)

    def test_delete_all(self):
        initial_number_of_trips = len(Trip.find_all())
        Trip.delete_all()
        self.assertEqual(len(Trip.find_all()), initial_number_of_trips - initial_number_of_trips)


class TestTravelAgencyMethod:
    def test_from_string(self):
        travel_agency_data = '1;TRAVEL ALCHEMY;ALICANTE'
        agency = TravelAgency.from_string(travel_agency_data)
        assert agency == TravelAgency(id=1, name='TRAVEL ALCHEMY', city='ALICANTE')

    def test_add_travel_agency(self):
        filename = 'data/test_travel_agencies_2.txt'
        TravelAgency.add_travel_agency(filename=filename, name='A', city='CITY A')
        agency = TravelAgency.get_all_agencies(filename)
        assert len(agency) == 1
        assert agency[0].id == 1
        assert agency[0].name == 'A'
        assert agency[0].city == 'CITY A'

        TravelAgency.add_travel_agency(filename=filename, name='B', city='CITY B')
        agencies = TravelAgency.get_all_agencies(filename)
        assert len(agencies) == 2
        second_agency = agencies[1]
        assert second_agency.id == 2
        assert second_agency.name == 'B'
        assert second_agency.city == 'CITY B'
        TravelAgency.delete_all_agencies(filename)
