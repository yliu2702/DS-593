# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

# Database name
database_file = 'health_events_data.db'

# Connect to the SQLite database
conn = sqlite3.connect(database_file)
print("Connect DB successfully!")

# Load the data into a pandas DataFrame
df = pd.read_sql_query("SELECT * FROM events", conn)

# 1. Number of missing cells by column
missing_cells = df.isnull().sum()

# 2. Number of unique categories in specific columns
columns_to_check = ['Condition', 'Agent', 'Reporting Agency', 'City']
unique_categories = {col: df[col].nunique() for col in columns_to_check}

# Print the results
print("Number of missing cells by column:")
print(missing_cells)
print("\nNumber of unique categories in specified columns:")
for col, count in unique_categories.items():
    print(f"{col}: {count}")

# Close the database connection
conn.close()
