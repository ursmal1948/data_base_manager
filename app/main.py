from service import Offer
from dotenv import load_dotenv
import os
from loaders import DbDataLoader, TxtDataLoader

# print(DbDataLoader().load('app/trips_db'))
# agencies = TxtDataLoader().load('data/travel_agencies.txt')
# print(agencies)
load_dotenv()
DB_NAME = os.getenv('DATABASE_NAME')


def main():
    data_conn = Offer.connect_data('../data/travel_agencies.txt')
    print(data_conn)


if __name__ == '__main__':
    main()
