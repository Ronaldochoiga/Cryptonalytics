#!/usr/bin/python3
import pymysql
from operator import itemgetter

# Database connection parameters
db_params = {
    'host': 'localhost',
    'user': 'ronaldochoiga',
    'password': 'Ronaldo@choiga1',
    'database': 'coingecko_database',
}

def fetch_top_losers_from_database(table_name, limit=10):
    try:
        # Connect to the database
        connection = pymysql.connect(**db_params)

        # Create a cursor object
        cursor = connection.cursor()

        # Fetch top gainers data from the database
        query = f"SELECT id, symbol, change_24h, price FROM {table_name} ORDER BY change_24h ASC LIMIT {limit}"
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
    
def get_coin_details(coin_id):
    try:
        # Connect to the database
        connection = pymysql.connect(**db_params)
        cursor = connection.cursor()
        
        # Fetch the coin name using the coin_id
        query = f"SELECT name FROM cryptocurrency_data WHERE id = {coin_id}"
        cursor.execute(query)
        coin_name = cursor.fetchone()[0]
        
        # Close the connection
        connection.close()
        
        return coin_name

    except Exception as e:
        print(f"Error fetching coin details from the database: {e}")
        return None

# Fetch top gainers data from the 'cryptocurrency_data' table
top_losers_data = fetch_top_losers_from_database('cryptocurrency_data')
coin_details = get_coin_details('id')
# Print or use the fetched data as needed
print(top_losers_data)
print(coin_details)
