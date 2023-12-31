#!/usr/bin/python3
import pymysql
from operator import itemgetter

# Database connection parameters
db_params = {
    'host': '3.85.54.217',
    'user': 'ronaldochoiga',
    'password': 'Ronaldo@choiga1',
    'database': 'binance_database',
}

def fetch_top_losers_from_database(table_name, limit=10):
    try:
        # Connect to the database
        connection = pymysql.connect(**db_params)

        # Create a cursor object
        cursor = connection.cursor()

        # Fetch top gainers data from the database
        query = f"SELECT coin_symbol, percentage_change_24h, current_price FROM {table_name} WHERE coin_symbol LIKE '%usdt%' ORDER BY percentage_change_24h ASC LIMIT {limit}"
        cursor.execute(query)

        # Fetch all the data into a list of dictionaries
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Close the connection
        connection.close()

        return data

    except Exception as e:
        print(f"Error fetching data from the database: {e}")
        return None

# Fetch top gainers data from the 'cryptocurrency_data' table
top_losers_data = fetch_top_losers_from_database('cryptocurrency_data')

# Print or use the fetched data as needed
print(top_losers_data)
