from app.model import Trip, TravelAgency
from app.loaders import TxtDataLoader
from enum import Enum
from dataclasses import dataclass, field
from typing import Self
from collections import defaultdict,Counter


class Continent(Enum):
    EUROPE = 0
    ASIA = 1
    AFRICA = 2
    NORTH_AMERICA = 3
    SOUTH_AMERICA = 4
    AUSTRALIA = 5


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
        def continent_path(continent: Continent) -> str:
            return f'../data/countries/{continent.name}.txt'
        path = continent_path(continent)
        with open(path,'r') as f:
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

