from dotenv import load_dotenv
import os

load_dotenv()
DB_NAME = os.getenv('DATABASE_NAME')
