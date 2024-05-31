from models import Trip, TravelAgency
from loaders import TxtDataLoader
from enum import Enum
from dataclasses import dataclass, field
from typing import Self


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
