import requests
import pymysql
from decimal import Decimal
from datetime import datetime

def connect_to_database():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='ronaldochoiga',
            password='Ronaldo@choiga1',
            database='coingecko_database'
        )

        if connection.open:
            print("Connected to MySQL database")
            return connection

    except pymysql.Error as e:
        print("Error: {}".format(e))
        return None

def close_database_connection(connection):
    if connection.open:
        connection.close()
        print("Connection to MySQL database closed")

def update_database(symbol, name, price, change_24h, market_cap, volume_24h):
    connection = connect_to_database()

    if connection:
        try:
            with connection.cursor() as cursor:
                # Check if the coin symbol already exists in the database
                cursor.execute("SELECT * FROM cryptocurrency_data WHERE symbol = %s", (symbol,))
                existing_record = cursor.fetchone()

                if existing_record:
                    # Update the existing record in the database
                    update_query = """
                    UPDATE cryptocurrency_data
                    SET name = %s, price = %s, change_24h = %s,
                        market_cap = %s, volume_24h = %s,
                        time_updated = CURRENT_TIMESTAMP
                    WHERE symbol = %s
                    """
                    cursor.execute(update_query, (name, price, change_24h, market_cap, volume_24h, symbol))
                else:
                    # Insert a new record into the database
                    insert_query = """
                    INSERT INTO cryptocurrency_data (symbol, name, price, change_24h, market_cap, volume_24h)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (symbol, name, price, change_24h, market_cap, volume_24h))

                # Commit the changes
                connection.commit()
                print("Database updated successfully")

        except pymysql.Error as e:
            print("Error: {}".format(e))

        finally:
            close_database_connection(connection)

def get_top_cryptocurrencies(limit=1000):
    base_url = "https://api.coingecko.com/api/v3"
    endpoint = "/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h",
    }

    url = f"{base_url}{endpoint}"
    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            return data
        else:
            print(f"Error: {response.status_code}, {data}")
            return []

    except Exception as e:
        print(f"Error: {e}")
        return []

def display_top_cryptocurrencies_info(data):
    if not data:
        print("Failed to retrieve information for the top cryptocurrencies")
        return

    for index, crypto_data in enumerate(data, start=1):
        symbol = crypto_data.get("symbol", "N/A")
        name = crypto_data.get("name", "N/A")
        price = crypto_data.get("current_price", "N/A")
        change_24h = crypto_data.get("price_change_percentage_24h", "N/A")
        market_cap = crypto_data.get("market_cap", "N/A")
        volume_24h = crypto_data.get("total_volume", "N/A")

        # Update the database with the retrieved information
        update_database(symbol, name, price, change_24h, market_cap, volume_24h)

        # Display information
        print(f"#{index}: {symbol} Information:")
        print(f"Name: {name}")
        print(f"Price (USD): {price}")
        print(f"Percentage Change (24h): {change_24h}%")
        print(f"Market Cap (USD): {market_cap}")
        print(f"Volume (24h): {volume_24h}")
        print()

# Retrieve information for the top cryptocurrencies
top_crypto_data = get_top_cryptocurrencies(limit=250)

# Display and update the database with the retrieved information
display_top_cryptocurrencies_info(top_crypto_data)
