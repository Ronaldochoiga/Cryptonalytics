import pymysql
import requests
# Replace with your BSCScan API key
API_KEY = '4YX5I95IW3DU4H4M3N1G17R1JGZBD33EZJ'

# MySQL database connection parameters
DB_HOST = 'localhost'
DB_USER = 'ronaldo'
DB_PASSWORD = 'Ronaldo@choiga1'
DB_NAME = 'account_database'

def create_table():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS labeled_addresses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                address VARCHAR(255),
                label VARCHAR(255)
            )
        ''')
    conn.commit()
    conn.close()

def insert_labeled_address(user_id, address, label, contract_address):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO labeled_addresses (user_id, address, label, contract_address) VALUES (%s, %s, %s, %s)', (user_id, address, label, contract_address))
    conn.commit()
    conn.close()

def get_labeled_addresses(user_id):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    with conn.cursor() as cursor:
        cursor.execute('SELECT address, label, contract_address FROM labeled_addresses WHERE user_id = %s', (user_id,))
        addresses = cursor.fetchall()
    conn.close()
    return addresses
def get_token_balance(user_address, contract_address):
    url = f'https://api.bscscan.com/api'
    params = {
        'module': 'account',
        'action': 'tokenbalance',
        'contractaddress': contract_address,
        'address': user_address,
        'tag': 'latest',
        'apikey': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['result']

def get_recent_transactions(user_address, contract_address):
    url = f'https://api.bscscan.com/api'
    params = {
        'module': 'account',
        'action': 'tokentx',
        'contractaddress': contract_address,
        'address': user_address,
        'page': 1,
        'offset': 10,
        'sort': 'desc',
        'apikey': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['result']
#this represents the end of the transactions code
