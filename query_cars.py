# ============================================
# SCRIPT 2: query_cars.py (RUN WHENEVER NEEDED)
# ============================================

import sqlite3
from sqlite3 import Error

def quick_query(query, db_path="C:\\Users\\Zack\\Desktop\\Data Analyst Project\\kaggle data\\car_sales\\connection_point.sqlite"):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        connection.close()
        return results
    except Error as e:
        print(f"Error: {e}")
        return None

# ============================================
# COMMON QUERIES - Use these anytime!
# ============================================

# Preview first 10 rows
print("=== First 10 cars ===")
results = quick_query("SELECT * FROM cars LIMIT 10")
if results:
    for row in results:
        print(row)

# Count total cars
print("\n=== Total cars in database ===")
count = quick_query("SELECT COUNT(*) FROM cars")
if count:
    print(f"Total cars: {count[0][0]}")

# Get specific columns only
print("\n=== Year, Make, Model, Price ===")
results = quick_query("SELECT year, make, model, sellingprice FROM cars LIMIT 5")
if results:
    for row in results:
        print(f"{row[0]} {row[1]} {row[2]} - ${row[3]}")

# Other useful queries (uncomment as needed):
results = quick_query("SELECT year, sellingprice, state FROM cars WHERE make = 'Toyota' LIMIT 5")
if results:
    print(f"Kia cars: {results}")

results = quick_query("SELECT year, make, model, sellingprice FROM cars WHERE sellingprice > 30000 LIMIT 5")
if results:
    print(f"Top 5 expensive cars: {results}")

results = quick_query("SELECT make, COUNT(*) FROM cars GROUP BY make ORDER BY COUNT(*) DESC LIMIT 10")
if results:
    print(f"Top 10 most common makes: {results}")



