# ============================================
# SCRIPT 1: setup_database.py (RUN ONCE ONLY)
# ============================================

import sqlite3
import pandas as pd
from sqlite3 import Error

def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):    
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# ONE-TIME SETUP
connection = create_connection("C:\\your_path...\\my_db.sqlite")

# Create table
create_table = """
CREATE TABLE IF NOT EXISTS cars (
                    id INTEGER PRIMARY KEY,
                    year INTEGER NOT NULL,
                    make TEXT NOT NULL,
                    model TEXT NOT NULL,
                    trim TEXT NOT NULL,
                    body TEXT NOT NULL,
                    transmission TEXT NOT NULL,
                    vin TEXT NOT NULL,
                    state TEXT NOT NULL,
                    condition INTEGER NOT NULL,
                    odometer INTEGER NOT NULL,
                    color TEXT NOT NULL,
                    interior TEXT NOT NULL,
                    seller TEXT NOT NULL,
                    mmr INTEGER NOT NULL,
                    sellingprice INTEGER NOT NULL,
                    saledate DATE NOT NULL                    
                );"""

execute_query(connection, create_table)

# Load CSV data into SQLite
csv_file_path = "C:\\your_path...\\output.csv"
df = pd.read_csv(csv_file_path)
df.to_sql('cars', connection, if_exists='append', index=False)
print(f"Loaded {len(df)} records")

connection.close()
print("Database setup complete!")
