from app.model import Trip, TravelAgency
from app.loaders import TxtDataLoader
from enum import Enum
from dataclasses import dataclass, field
from typing import Self
from collections import defaultdict, Counter


class Continent(Enum):
    EUROPE = 0
    ASIA = 1
    AFRICA = 2
    NORTH_AMERICA = 3
    SOUTH_AMERICA = 4
    AUSTRALIA = 5


class TravelAgenciesService:

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
            id_ = TravelAgenciesService._get_last_travel_agency_id(filename)
            travel_agency_id = id_ + 1 if id_ else 1
            new_agency_data = ';'.join([str(travel_agency_id), name, city])
            f.write('\n' + new_agency_data if travel_agency_id != 1 else new_agency_data)


@dataclass
class Offer:
    agency_trips: dict[TravelAgency, list[Trip]] = field(default=dict)

    # def get_all_trips(self):
    #     return [t for trips in self.agency_trips.values() for t in trips]

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

    def get_agency_with_most_trips(self):
        grouped_by_number_of_trips = Counter()
        for agency in self.agency_trips.keys():
            trips = len(self.agency_trips[agency])
            grouped_by_number_of_trips[agency] = trips
        return max(grouped_by_number_of_trips.items(), key=lambda e: e[1])[0]

    def trips_by_participants_count(self):
        grouped_by_people_count = defaultdict(list)
        all_trips = self.get_all_trips()
        for trip in all_trips:
            grouped_by_people_count[trip.tourists_number].append(trip)
