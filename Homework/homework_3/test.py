USER = "admin"
PASSWORD = "password"
Unmodified_DB = "mydb_1"
Avg_usage_DB = "mydb_2"
Unmodified_HOST = "unmodified_db"
Avg_usage_HOST = "avg_usage_db"
PORT = "5432"

from sqlalchemy import create_engine
import time

def get_engine(url):
    while True:
        try:
            print("Attempting to create engine...")
            engine = create_engine(url)   
            print("Engine created")         
            with engine.connect() as conn:
                print("Connected to database")
                return engine

        except Exception as e:
            print("Error while connecting: ", e)
            time.sleep(3)

Unmodified_URL = f"postgresql://{USER}:{PASSWORD}@{Avg_usage_HOST}:{PORT}/{Avg_usage_DB}"
get_engine(Unmodified_URL)