# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kxlupgWo41DO2-pZ2QmUXqKEJoSAxkpe
"""

import sqlite3
import csv

# Define the database and table name
db_name = 'health_events_data.db'
table_name = 'health_events'

# Define the CSV file path
csv_file = '/content/funny_epidemiological_events.csv'  # Replace with the actual path to your CSV file

# Connect to the SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create a table based on the CSV headers
def create_table_from_csv(csv_file, cursor):
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the first line as headers
        columns = ', '.join([f'"{header}" TEXT' for header in headers])  # Use TEXT type for simplicity
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')

# Insert CSV data into the SQLite table
def import_csv_to_sqlite(csv_file, cursor):
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip headers for insertion
        placeholders = ', '.join(['?'] * len(headers))
        insert_query = f'INSERT INTO {table_name} VALUES ({placeholders})'

        for row in reader:
            cursor.execute(insert_query, row)

# Run the functions to create the table and import data
create_table_from_csv(csv_file, cursor)
import_csv_to_sqlite(csv_file, cursor)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Data imported successfully into {db_name}!")