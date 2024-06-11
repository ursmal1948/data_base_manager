from app.model import Trip, TravelAgency
from app.loaders import TxtDataLoader
from app.enums import Continent
from dataclasses import dataclass, field
from typing import Self
from collections import defaultdict
from decimal import Decimal


@dataclass
class Offer:
    agency_trips: dict[TravelAgency, list[Trip]] = field(default=dict)

    @classmethod
    def connect_data(cls, filename: str) -> Self:
        data = {}
        agencies = TxtDataLoader().load(filename)
        for agency in agencies:
            if agency not in data:
                data[agency] = Trip.find_all_by_agency_id(agency.id)
        return cls(data)

    def get_all_trips(self):
        return [t for trips in self.agency_trips.values() for t in trips]

    def get_trips_by_continent(self, continent: Continent) -> list[Trip]:
        def continent_countries_path(cont: Continent) -> str:
            return f'data/countries/{cont.name.lower()}.txt'

        path = continent_countries_path(continent)
        with open(path, 'r') as f:
            countries = [c.strip() for c in f.readlines()]
        return [trip for trip in self.get_all_trips() if trip.destination in countries]

    def get_agency_with_most_trips(self) -> list[TravelAgency] | TravelAgency:
        grouped_by_number_of_trips = defaultdict(list)
        for agency in self.agency_trips.keys():
            trips_number = len(self.agency_trips[agency])
            if trips_number:
                grouped_by_number_of_trips[trips_number].append(agency)
        agencies_with_most_trips = max(grouped_by_number_of_trips.items(), key=lambda e: e[0])[1]
        return agencies_with_most_trips[0] if len(agencies_with_most_trips) == 1 else agencies_with_most_trips

    def trips_by_participants_count(self):
        grouped_by_people_count = defaultdict(list)
        all_trips = self.get_all_trips()
        for trip in all_trips:
            grouped_by_people_count[trip.tourists_number].append(trip)

    def _get_trips_by_agency(self, agency_id: int) -> list[Trip]:
        desired_agency = [agency for agency in self.agency_trips.keys() if agency.id == agency_id][0]
        return self.agency_trips[desired_agency]

    def _calculate_agency_income_from_trips(self, agency_id: int, tax_rate: int) -> int:
        trips = self._get_trips_by_agency(agency_id)
        return sum([
            (Decimal(trip.tourists_number * trip.price)) * Decimal('0.1') * (Decimal(100 - tax_rate) / Decimal(100))
            for trip in trips])

    def _get_agency_by_id(self, agency_id: int) -> TravelAgency:
        return [agency for agency in self.agency_trips.keys() if agency.id == agency_id][0]

    def get_agency_with_highest_income(self, tax_rate: int) -> TravelAgency:
        agencies_income = [
            (agency.id, self._calculate_agency_income_from_trips(agency.id, tax_rate))
            for agency in self.agency_trips.keys()]
        agency_id__with_highest_income = max(agencies_income, key=lambda e: e[1])[0]
        return self._get_agency_by_id(agency_id__with_highest_income)
