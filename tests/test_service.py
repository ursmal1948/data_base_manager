from unittest.mock import MagicMock
from app.enums import Continent


class TestServiceMethods:

    def test_get_unique_destinations(self, offer):
        offer.get_unique_destinations = MagicMock(return_value=['MALTA', 'USA', 'PORTUGAL', 'NEW ZEALAND', 'INDIA'])
        expected_destinations = ['MALTA', 'USA', 'PORTUGAL', 'NEW ZEALAND', 'INDIA']
        destinations = offer.get_unique_destinations()
        assert destinations == expected_destinations

    def test_get_trips_by_continent_when_more_than_one_trip(self, offer):
        trips_idx_in_europe = [t.id_ for t in offer.get_trips_by_continent(Continent.EUROPE)]
        expected_trips_idx = [7, 1, 8, 3, 9]
        assert trips_idx_in_europe == expected_trips_idx

    def test_get_trips_by_continent_with_exactly_one_trip(self, offer):
        trips_idx_in_asia = [t.id_ for t in offer.get_trips_by_continent(Continent.ASIA)]
        assert trips_idx_in_asia == [4]

    def test_get_trips_by_continent_with_no_trips(self, offer):
        assert offer.get_trips_by_continent(Continent.SOUTH_AMERICA) == []

    def test_agency_with_most_trips(self, offer):
        agency_id_with_most_trips = offer.get_agency_with_most_trips().id
        assert agency_id_with_most_trips == 1

    def test_group_trips_by_tourists_count(self, offer):
        trips_by_tourists_count = offer.group_trips_by_tourists_count()
        assert len(trips_by_tourists_count.keys()) == 5
        assert len(trips_by_tourists_count[20]) == 3
        assert len(trips_by_tourists_count[50]) == 2
        assert len(trips_by_tourists_count[100]) == 1
        assert len(trips_by_tourists_count[200]) == 1
        assert len(trips_by_tourists_count[300]) == 1
        # logging.info(trips_by_tourists_count)

    def test_get_most_frequent_travel_agency_index_for_each_destination(self, offer):
        offer.get_unique_destinations = MagicMock(return_value=['MALTA', 'USA', 'PORTUGAL', 'NEW ZEALAND', 'INDIA'])
        result = offer.get_most_frequent_travel_agency_index_for_each_destination()
        assert len(result) == 5
        assert result['MALTA'] == [2]
        assert result['USA'] == [1]
        assert result['PORTUGAL'] == [3, 4]
        assert result['NEW ZEALAND'] == [3]
        assert result['INDIA'] == [1]

    def test_get_agency_with_highest_income(self, offer):
        tax_rate = 19
        agency_with_highest_income = offer.get_agency_with_highest_income(tax_rate)
        assert agency_with_highest_income.id == 3
