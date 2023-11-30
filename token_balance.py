#!/usr/bin/python3
import requests

def get_bep20_balance(api_key, contract_address, wallet_address):
    base_url = 'https://api.bscscan.com/api'
    endpoint = 'tokenbalance'

    parameters = {
        'module': 'account',
        'action': 'tokenbalance',
        'contractaddress': contract_address,
        'address': wallet_address,
        'tag': 'latest',
        'apikey': api_key,
    }

    response = requests.get(f'{base_url}?{endpoint}', params=parameters)
    data = response.json()

    if data['status'] == '1':
        return int(data['result'])
    else:
        return None

# Replace 'YOUR_API_KEY' with your actual BSCscan API key
API_KEY = '4YX5I95IW3DU4H4M3N1G17R1JGZBD33EZJ'

# Replace 'TOKEN_CONTRACT_ADDRESS' with the BEP-20 token contract address
TOKEN_CONTRACT_ADDRESS = '0x05995a068bdac17c582eC75AB46bb8e7394be1d9'

# Replace 'WALLET_ADDRESS' with the public address you want to check
WALLET_ADDRESS = '0xB8B71419daAd2C224d107C6F61BA0dC7Cb5F62f2'

# Get the BEP-20 token balance
balance = get_bep20_balance(API_KEY, TOKEN_CONTRACT_ADDRESS, WALLET_ADDRESS)

if balance is not None:
    print(f'The balance of {WALLET_ADDRESS} for the token at {TOKEN_CONTRACT_ADDRESS} is: {balance}')
else:
    print(f'Error retrieving balance. Check the API key and addresses.')
