import requests

BASE_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

def get_crypto_details(api_key, symbol):
    parameters = {
        'symbol': symbol,
        'convert': 'USD',
        'apiKey': api_key,
    }
    response = requests.get(BASE_URL, params=parameters)
    data = response.json()
    return data['data'][0]
