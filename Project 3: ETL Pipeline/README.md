Project 3: ETL Pipeline

To demonstrate proficiency of creating and maintaining basic data pipeline. 

Daily stocks data from Alpha Vintage (www.alphavantage.co) is acquired through API using Python.

Packages used in python: pandas, sqlite3, requests, schedule

Raw data acquired thru API -> data assigned into lists, and types are defined -> data saved in pandas table -> pandas table saved into sql database (sqlite) -> the steps are repeated periodically using scheduler package (local scheduling) or cron task (live updates)

simple_scheduler.py: For static, localised data acquisition. 

stock_scheduler_once.py: For live updates. Require setup using the system's background scheduler eg cron.
For linux/unix, 
 `crontab -e` to open crontab file editor, 
 `# Run stock data update every day at 6:00 PM`
`0 18 * * * cd /home/ec2-user/stock_scheduler && /usr/bin/python3 stock_schedule>` (eg. running every day at 6 pm)