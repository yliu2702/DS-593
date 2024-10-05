import pandas as pd
from sklearn import datasets
from sqlalchemy import create_engine
import time

def get_engine(url):
    while True:
        try:
            engine = create_engine(url)
            with engine.connect() as connection:
                return engine
        except Exception as e:
            print("Connection Failed", e)
            time.sleep(5)


if __name__ == '__main__':
    user = "admin"
    password = "password"
    host = "postgres"
    port = "5432"
    database = "mydb"
    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    print(url)
    engine = get_engine(url)
    df = database.fetch_openml("titanic", version=1)['data']
    df.to_sql("titanic", engine, if_exists='replace', index=False)
    print("Data loaded successfully")

