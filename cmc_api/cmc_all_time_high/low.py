#!/usr/bin/python3
import requests

def get_crypto_info(api_key, symbol):
    coinmarketcap_api_url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'

    try:
        # Set up the request headers with your CoinMarketCap API key
        headers = {
            'X-CMC_PRO_API_KEY': api_key
        }

        # Set up the request parameters, including the cryptocurrency symbol
        params = {
            'symbol': symbol
        }

        # Make a GET request to get information about the specified cryptocurrency
        response = requests.get(coinmarketcap_api_url, headers=headers, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            crypto_info = response.json()
            # Print all the info to inspect the nature of the api calls
            print(crypto_info)

            # Extract relevant information (replace 'your_key' with the actual key in the response)
            all_time_high_price = crypto_info['data'][symbol]['quote']['USD']['ath']['price']
            all_time_low_price = crypto_info['data'][symbol]['quote']['USD']['atl']['price']
            launch_date = crypto_info['data'][symbol]['date_added']

            # Print the information
            print(f"Symbol: {symbol}")
            print(f"All-Time High Price: {all_time_high_price}")
            print(f"All-Time Low Price: {all_time_low_price}")
            print(f"Launch Date: {launch_date}")

        else:
            print(f"Error: Unable to fetch data. Status Code: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Replace 'your_api_key' with your actual CoinMarketCap API key
    api_key = '62beabd5-0e1f-4968-8c3d-62455aa321d1'

    # Replace 'BTC' with the symbol of the cryptocurrency you want to get information about
    symbol = 'BTC'

    get_crypto_info(api_key, symbol)
