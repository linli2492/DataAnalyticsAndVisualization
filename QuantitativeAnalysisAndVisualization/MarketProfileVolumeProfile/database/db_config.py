import os 
from dotenv import load_dotenv

load_dotenv()

db_config = {"host": "localhost",
             "database": "ficc_data",
             "user": "postgres",
             "password": os.getenv("DB_PASSWORD")}
