import sqlite3
from app.service import Offer


def main() -> None:
    data_conn = Offer.connect_data('data/travel_agencies.txt')
    print(data_conn)


if __name__ == '__main__':
    main()
