#!/usr/bin/python3
import requests
import pymysql
import schedule
import time

def get_binance_gainers_losers():
    binance_api_url = 'https://api.binance.com/api/v3/ticker/24hr'

    try:
        # Make a GET request to get the 24-hour price statistics for all symbols
        response = requests.get(binance_api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            ticker_data = response.json()
            usdt_symbols = [symbol for symbol in ticker_data if symbol['symbol'].endswith('USDT')]

            # Filter gainers and losers
            gainers = [symbol for symbol in usdt_symbols if float(symbol['priceChangePercent']) > 15]
            losers = [symbol for symbol in usdt_symbols if float(symbol['priceChangePercent']) < -5]

            # Print information about gainers
            print("Gainers:")
            for symbol in gainers[:15]:  # Print the top 15 gainers
                print(f"Symbol: {symbol['symbol']}, Price: {symbol['lastPrice']}, "
                      f"Price Change (%): {symbol['priceChangePercent']}")

            # Print information about losers
            print("\nLosers:")
            for symbol in losers[:15]:  # Print the top 15 losers
                print(f"Symbol: {symbol['symbol']}, Price: {symbol['lastPrice']}, "
                      f"Price Change (%): {symbol['priceChangePercent']}")

            # Send data to the database
            send_to_database(gainers, 'gainers_table')
            send_to_database(losers, 'losers_table')

        else:
            print(f"Error: Unable to fetch data. Status Code: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

def send_to_database(data, table_name):
    # Database connection parameters
    db_params = {
        'host': 'localhost',
        'user': 'ronaldochoiga',
        'password': 'test_password',
        'database': 'binance_database',
    }

    try:
        # Connect to the database
        connection = pymysql.connect(**db_params)

        # Create a cursor object
        cursor = connection.cursor()

        # Determine the appropriate table name
        if table_name == 'gainers_table':
            table_name = 'gainers_table'
        elif table_name == 'losers_table':
            table_name = 'losers_table'
        else:
            print("Invalid table name.")
            return

        # Insert data into the specified table
        for symbol in data:
            sql = f"INSERT INTO {table_name} (coin, price, percentage) VALUES (%s, %s, %s)"
            values = (symbol['symbol'], float(symbol['lastPrice']), float(symbol['priceChangePercent']))
            cursor.execute(sql, values)
        # Commit changes and close the connection
        connection.commit()
        connection.close()

        print(f"Data successfully sent to the {table_name}.")

    except Exception as e:
        print(f"Error sending data to the database: {e}")

# Schedule the API call every one minute
schedule.every(1).minutes.do(get_binance_gainers_losers)

while True:
    schedule.run_pending()
    time.sleep(1)
