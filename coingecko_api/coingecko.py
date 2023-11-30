#!/usr/bin/python3
import requests

def get_crypto_list_with_prices():
    # CoinGecko API endpoint for cryptocurrency list
    list_api_url = 'https://api.coingecko.com/api/v3/coins/list'

    try:
        # Make a GET request to get the list of cryptocurrencies
        list_response = requests.get(list_api_url)

        # Check if the request was successful (status code 200)
        if list_response.status_code == 200:
            # Parse the JSON response
            crypto_list = list_response.json()

            # Iterate through the first few cryptocurrencies
            for crypto in crypto_list[:20]:
                # CoinGecko API endpoint for cryptocurrency prices
                price_api_url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto["id"]}&vs_currencies=usd'

                try:
                    # Make a GET request to get the price of the current cryptocurrency
                    price_response = requests.get(price_api_url)

                    # Check if the price request was successful (status code 200)
                    if price_response.status_code == 200:
                        # Parse the JSON response
                        price_data = price_response.json()

                        # Extract the price in USD
                        price_in_usd = price_data[crypto["id"]]["usd"]

                        # Print information about the cryptocurrency and its price
                        print(f"Name: {crypto['name']}, Symbol: {crypto['symbol']}, ID: {crypto['id']}, Price (USD): {price_in_usd}")

                    else:
                        print(f"Error: Unable to fetch price data for {crypto['name']}. Status Code: {price_response.status_code}")

                except Exception as price_error:
                    print(f"Error fetching price for {crypto['name']}: {price_error}")

        else:
            print(f"Error: Unable to fetch data. Status Code: {list_response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_crypto_list_with_prices()
