import pytest
from app.model import Trip, TravelAgency
from app.service import Offer
from decimal import Decimal


@pytest.fixture
def first_travel_agency():
    return TravelAgency(id=1, name='HORIZON', city='NEW YORK')


@pytest.fixture
def second_travel_agency():
    return TravelAgency(id=2, name='GLOBAL EXPLORER', city='LOS ANGELES')


@pytest.fixture
def third_travel_agency():
    return TravelAgency(id=3, name='WANDER GLOBE', city='CHICAGO')


@pytest.fixture
def fourth_travel_agency():
    return TravelAgency(id=4, name='ITAKA', city='MIAMI')


@pytest.fixture
def first_travel_agency_trips():
    return [
        Trip(id_=2, destination='USA', price=Decimal('100'), tourists_number=200, agency_id=1),
        Trip(id_=4, destination='INDIA', price=Decimal('200'), tourists_number=20, agency_id=1),
        Trip(id_=7, destination='MALTA', price=Decimal('2000'), tourists_number=50, agency_id=1)]


@pytest.fixture
def second_travel_agency_trips():
    return [
        Trip(id_=1, destination='MALTA', price=Decimal('1000'), tourists_number=100, agency_id=2),
        Trip(id_=8, destination='MALTA', price=Decimal('100'), tourists_number=20, agency_id=2)
    ]


@pytest.fixture
def third_travel_agency_with_trips():
    return [
        Trip(id_=6, destination='NEW ZEALAND', price=Decimal('3000'), tourists_number=300, agency_id=3),
        Trip(id_=3, destination='PORTUGAL', price=Decimal('200'), tourists_number=20, agency_id=5)
    ]


@pytest.fixture
def fourth_travel_agency_with_trips():
    return [Trip(id_=9, destination='PORTUGAL', price=Decimal('3000'), tourists_number=50, agency_id=4)]


@pytest.fixture
def travel_agency_with_trips(first_travel_agency, second_travel_agency, third_travel_agency, fourth_travel_agency,
                             first_travel_agency_trips,
                             second_travel_agency_trips,
                             third_travel_agency_with_trips,
                             fourth_travel_agency_with_trips):
    return {first_travel_agency: first_travel_agency_trips,
            second_travel_agency: second_travel_agency_trips,
            third_travel_agency: third_travel_agency_with_trips,
            fourth_travel_agency: fourth_travel_agency_with_trips}


@pytest.fixture
def offer(travel_agency_with_trips):
    return Offer(travel_agency_with_trips)
