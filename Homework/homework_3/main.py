import os
import requests
import zipfile
import pandas as pd
from datetime import datetime as dt
import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

blue_bike_url = "https://s3.amazonaws.com/hubway-data/201905-bluebikes-tripdata.zip"
zip_file_path = "201905-bluebikes-tripdata.zip"
extract_folder = "/Users/yiliu/DS-593/Homework/homework_3/dataset/"
save_folder = "/Users/yiliu/DS-593/Homework/homework_3/dataset/transform_data/"
os.makedirs(extract_folder, exist_ok=True)
os.makedirs(save_folder, exist_ok=True)

# fetch blue bike data
response = requests.get(blue_bike_url)
with open(zip_file_path, 'wb') as file:
  file.write(response.content)
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)
bb_csv_file_path = extract_folder + zip_file_path.replace('.zip', '.csv')
print(f"Blue Bike data is stored in {bb_csv_file_path}")

# Bluebike data cleaning
bluebike_data = pd.read_csv(bb_csv_file_path)
bluebike_data['starttime'] = pd.to_datetime(bluebike_data['starttime'])
bluebike_data['stoptime'] = pd.to_datetime(bluebike_data['stoptime'])
bluebike_data['date'] = bluebike_data['starttime'].dt.strftime("%Y-%m-%d")
transformed_bluebike = bluebike_data[['bikeid','date','starttime','stoptime','tripduration']]
transformed_bluebike.to_csv(save_folder + "/transformed_bluebike.csv")
print("Transformed Blue Bike data, contains columns: ", transformed_bluebike.columns)

# fetch rainfall data
rainfall_path = "dataset/BWSC_Rainfall_Daily_Charlestown_Bunker_Hill.csv"
rainfall_data = pd.read_csv(rainfall_path)
# Rainfall data cleaning
rainfall_data['Date'] = pd.to_datetime(rainfall_data['Date'], format = "%m/%d/%y")
rainfall_data['Date'] = rainfall_data['Date'].dt.strftime("%Y-%m-%d")
rainfall_data.columns = ['date','rainfall']
rainfall_data.to_csv(save_folder + "/transformed_rainfall.csv")

# Daily Avg ridership with rainfall in May 2019
daily_avg_ridership = transformed_bluebike.groupby('date')['tripduration'].sum().reset_index()
daily_avg_ridership['tripduration'] = round(daily_avg_ridership['tripduration']/60,2)
daily_avg_ridership.columns = ['date','sum_duration_in_min']
avg_ridership_with_rainfall = pd.merge(daily_avg_ridership, rainfall_data, on='date')
avg_ridership_with_rainfall.to_csv(save_folder + "/avg_ridership_with_rainfall.csv")

def get_engine(url):
    while True:
        try:
            engine = create_engine(url)            
            with engine.connect() as conn:
                return engine
        except Exception as e:
            print("Error while connecting: ", e)
            time.sleep(3)

def save_POSTGRESQL(url, data, table_name):
    # SAVE DATA TO POSTGRESQL
    try:
        print("Attempting to create engine...")
        engine = get_engine(url)
        print("Engine created")
        data.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Table {table_name} is saved to PostgreSQL")
    except Exception as e:
        print(f"Failed to save table {table_name} to PostgreSQL:{e}")


# SAVE DATA TO POSTGRESQL
USER = "admin"
PASSWORD = "password"
Unmodified_DB = "mydb_1"
Avg_usage_DB = "mydb_2"
Unmodified_HOST = "unmodified_db"
Avg_usage_HOST = "avg_usage_db"
PORT = "5432"
Unmodified_URL = f"postgresql://{USER}:{PASSWORD}@{Unmodified_HOST}:{PORT}/{Unmodified_DB}"
Avg_usage_URL = f"postgresql://{USER}:{PASSWORD}@{Avg_usage_HOST}:{PORT}/{Avg_usage_DB}"
print("PostgreSQL database for step b: ", Unmodified_URL)
print("PostgreSQL database for step c: ", Avg_usage_URL)

# Save unmodified tables to PostgreSQL
save_POSTGRESQL(Unmodified_URL, transformed_bluebike, 'bluebike_data')
save_POSTGRESQL(Unmodified_URL, rainfall_data, 'rainfall_data')

# Save transformed tables to PostgreSQL
save_POSTGRESQL(Avg_usage_URL, avg_ridership_with_rainfall, 'avg_ridership_with_rainfall')
