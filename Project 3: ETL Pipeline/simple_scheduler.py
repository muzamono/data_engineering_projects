# Simple Stock Data Scheduler - Beginner Version

import pandas as pd
import sqlite3
import requests
import schedule
import time
from datetime import datetime

# API key and stock symbol
API_KEY = "API_KEY"  # Get this from alphavantage.co
STOCK_SYMBOL = "AAPL"  # Can change this to any stock

def get_stock_data():
    """This function gets stock data from the internet"""
    print(f"Getting stock data for {STOCK_SYMBOL}...")
    
    # API URL to get daily stock prices
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_SYMBOL}&apikey={API_KEY}&outputsize=compact"
    response = requests.get(url)
    data = response.json()
    
    # Check if we got good data
    if "Time Series (Daily)" not in data:
        print("Couldn't get stock data. Check your API key or stock symbol.")
        return None
    
    # Clean the data with specified typings
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
    
    # Make it into a pandas table and sort by date
    df = pd.DataFrame(stock_records)
    df = df.sort_values("Date")
    print(f"Got {len(df)} days of stock data!")
    return df

def save_to_database(df):
    """This function saves our data to a database file"""
    if df is None:
        print("No data to save")
        return
    
    print("Saving data to database...")
    
    # Connect to the database file (or create it if it doesn't exist)
    with sqlite3.connect("my_stocks.db") as conn:
        df.to_sql("stock_prices", conn, if_exists="replace", index=False) # Save the data to a table
        print("Data saved successfully")

def run_stock_pipeline():
    """This is our main function that does everything"""
    print(f"\n Starting stock data update at {datetime.now()}")
    
    # Step 1: Get the data
    stock_data = get_stock_data()
    
    # Step 2: Save the data
    save_to_database(stock_data)
    
    print("All done!\n" + "="*50)

def show_latest_data():
    """Show the latest stock prices we saved"""
    try:
        with sqlite3.connect("my_stocks.db") as conn:
            df = pd.read_sql_query("SELECT * FROM stock_prices ORDER BY Date DESC LIMIT 5", conn)
        
        print("\n Latest Stock Prices:")
        print(df.to_string(index=False))
        print()
    except:
        print("No data found yet. Run the pipeline first!")

# Set up the schedule
def setup_schedule():
    """Set up when our program should run"""
    
    # Option 1: Run every day at 6 PM (after stock market closes)
    schedule.every().day.at("14:35").do(run_stock_pipeline)
    
    # Option 2: Run only on weekdays (uncomment the lines below if you want this)
    # schedule.every().monday.at("18:00").do(run_stock_pipeline)
    # schedule.every().tuesday.at("18:00").do(run_stock_pipeline)
    # schedule.every().wednesday.at("18:00").do(run_stock_pipeline)
    # schedule.every().thursday.at("18:00").do(run_stock_pipeline)
    # schedule.every().friday.at("18:00").do(run_stock_pipeline)
    
    # Option 3: Run every 30 minutes (for testing - uncomment if needed)
    # schedule.every(30).minutes.do(run_stock_pipeline)
    
    print(" Schedule set up! Will run every day at 6:00 PM")
    print(f" Next run will be: {schedule.next_run()}")

def main():
    """Main program that starts everything"""
    print(" Welcome to Simple Stock Data Scheduler!")
    print("="*50)
    
    # Set up schedule
    setup_schedule()
    
    # Run once right now to test
    print(" Running once right now for testing...")
    run_stock_pipeline()
    
    # Show what we got
    show_latest_data()
    
    # Keep the program running and check for scheduled tasks
    print(" Now waiting for scheduled runs... (Press Ctrl+C to stop)")
    try:
        while True:
            schedule.run_pending()  # Check if it's time to run
            time.sleep(60)  # Wait 1 minute before checking again
    except KeyboardInterrupt:
        print("\n Stopping the scheduler")

if __name__ == "__main__":
    # This runs when you start the program
    main()

