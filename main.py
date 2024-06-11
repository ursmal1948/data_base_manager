import sqlite3
from app.service import Offer, TravelAgenciesService
from app.service import Continent


def main() -> None:
    data_conn = Offer.connect_data('data/travel_agencies.txt')
    # print(data_conn)
    # print(TravelAgenciesService.get_last_travel_agency_id('datadata/travel_agencies.txt'))
    # print(TravelAgenciesService.add_travel_agency('data/travel_agencies.txt', 'AOTHER NAMEE', 'DUBLIN'))
    #     print(TravelAgenciesService.add_travel_agency('data/empty.txt', 'AOTHER NAMEE', 'DUBLIN'))
    print(data_conn.get_trips_by_continent(Continent.EUROPE))
    # print(data_conn.get_p(Continent.EUROPE))


if __name__ == '__main__':
    main()
