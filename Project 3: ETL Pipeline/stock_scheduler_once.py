import pandas as pd
import sqlite3
import requests
from datetime import datetime

API_KEY = "your_api_key_here"

def get_stock_data(symbol):
    print(f"Getting stock data for {symbol}...")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=compact"
    
    response = requests.get(url)
    data = response.json()
    
    if "Time Series (Daily)" not in data:
        print("Couldn't get stock data. Check your API key!")
        return None
    
    stock_records = []
    for date, prices in data["Time Series (Daily)"].items():
        stock_records.append({
            "Date": date,
            "Open": float(prices["1. open"]),
            "High": float(prices["2. high"]),
            "Low": float(prices["3. low"]),
            "Close": float(prices["4. close"]),
            "Volume": int(prices["5. volume"])
        })
    
    df = pd.DataFrame(stock_records)
    df = df.sort_values("Date")
    print(f"Got {len(df)} days of stock data!")
    return df

def save_to_database(df, symbol):
    if df is None:
        return
    
    print(f"Saving {symbol} data to database...")
    with sqlite3.connect("/home/ec2-user/stock_scheduler/my_stocks.db") as conn: # Full path in ec2
        df['Symbol'] = symbol
        df.to_sql("stock_prices", conn, if_exists="append", index=False)
        print("Data saved successfully!")

# Main execution
symbols = ["AAPL", "AMZN", "GOOGL", "META", "NVDA"]
for symbol in symbols:
    stock_data = get_stock_data(symbol)
    save_to_database(stock_data, symbol)