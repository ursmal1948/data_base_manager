import sqlite3
from functools import wraps


def connect_to_database2(func):
    # Wrapper function in which the argument is called
    # inner function cas access the outer local functions like in this case func.
    def wrapper(*args, **kwargs):
        with sqlite3.connect('trips_db') as conn:
            cursor = conn.cursor()

            # calling the actual function now isnde the wrapper function.
            result = func(cursor, *args, **kwargs)
            return result

    return wrapper


# defining a function to be called inside a warapper.
@connect_to_database2
def find_all2(cursor):
    cursor.execute('select tourists_number from trips')
    return cursor.fetchall()


