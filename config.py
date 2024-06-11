from dotenv import load_dotenv
import os

load_dotenv()
test_db_name = os.getenv('TEST_DATABASE_NAME')
db_name = os.getenv('DATABASE_NAME')
