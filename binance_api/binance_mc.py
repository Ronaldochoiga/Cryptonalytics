#!/usr/bin/python3
import requests
import pymysql

def connect_to_database():
    try:
        # Establish a connection to the MySQL database
        connection = pymysql.connect(
            host='localhost',
            user='ronaldochoiga',
            password='test_password',
            database='binance_database'
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

def update_database(coin_symbol, current_price, percentage_change_24h, market_cap_usdt, all_time_high_price):
    connection = connect_to_database()

    if connection:
        try:
            with connection.cursor() as cursor:
                # Check if the coin symbol already exists in the database
                cursor.execute("SELECT * FROM cryptocurrency_data WHERE coin_symbol = %s", (coin_symbol,))
                existing_record = cursor.fetchone()

                if existing_record:
                    # Update the existing record in the database
                    update_query = """
                    UPDATE cryptocurrency_data
                    SET current_price = %s, percentage_change_24h = %s,
                        market_cap_usdt = %s, all_time_high_price = %s
                    WHERE coin_symbol = %s
                    """
                    cursor.execute(update_query, (current_price, percentage_change_24h, market_cap_usdt, all_time_high_price, coin_symbol))
                else:
                    # Insert a new record into the database
                    insert_query = """
                    INSERT INTO cryptocurrency_data (coin_symbol, current_price, percentage_change_24h, market_cap_usdt, all_time_high_price)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (coin_symbol, current_price, percentage_change_24h, market_cap_usdt, all_time_high_price))

                # Commit the changes
                connection.commit()
                print("Database updated successfully")

        except pymysql.Error as e:
            print("Error: {}".format(e))

        finally:
            close_database_connection(connection)

def get_binance_top_200():
    binance_api_url = 'https://api.binance.com/api/v3/ticker/24hr'

    try:
        # Make a GET request to get the 24-hour price statistics for all symbols
        response = requests.get(binance_api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            ticker_data = response.json()

            # Sort symbols based on market cap (Note: Market cap is not directly provided, you might need additional data for accurate market cap calculation)
            sorted_symbols = sorted(ticker_data, key=lambda x: float(x['quoteVolume']), reverse=True)[:1000]

            # Print information about the top 200 cryptocurrencies
            for symbol in sorted_symbols:
                coin_symbol = symbol['symbol']
                current_price = symbol['lastPrice']
                percentage_change_24h = symbol['priceChangePercent']
                market_cap_usdt = symbol['quoteVolume']
                all_time_high_price = symbol.get('highPrice', 'N/A')  # 'N/A' if all-time high is not available

                # Update the database with the retrieved information
                update_database(coin_symbol, current_price, percentage_change_24h, market_cap_usdt, all_time_high_price)

        else:
            print("Error: Unable to fetch data. Status Code: {}".format(response.status_code))

    except Exception as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    get_binance_top_200()
