<<<<<<< HEAD
import mysql.connector
from flask import Flask, Blueprint, render_template, request, redirect, url_for, jsonify,session, flash
import requests
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import logging
from logging.handlers import RotatingFileHandler
#from binance_api.binance_mc import get_binance_top_200
from coingecko_api.gainers_fetch import fetch_top_gainers_from_database, get_coin_details
from coingecko_api.losers_fetch import fetch_top_losers_from_database, get_coin_details
from coingecko_api.higher_cap import fetch_top_cap_from_database, get_coin_details
from coingecko_api.top250 import get_top_cryptocurrencies
from bsc_info import create_table, insert_labeled_address, get_labeled_addresses, get_token_balance, get_recent_transactions
#from cmc_api.search_info import get_crypto_details
from flask_apscheduler import APScheduler #imports the apscheduler extension
from apscheduler.schedulers.background import BackgroundScheduler
=======
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from binance_api.binance_mc import get_binance_top_200
from binance_api.gainers_fetch import fetch_top_gainers_from_database
from binance_api.losers_fetch import fetch_top_losers_from_database
from binance_api.higher_cap import fetch_top_cap_from_database
#from cmc_api.search_info import get_crypto_details
#from flask_apscheduler import APScheduler #imports the apscheduler extension
>>>>>>> a7b8a258312fef0da3078aab9216a54cf8e6dbaa
import time
import threading
from flask_mysqldb import MySQL
import bcrypt
import secrets
import pymysql
<<<<<<< HEAD

#from login import configure_login
#losers_fetch_bp = Blueprint('losers_fetch', __name__)
scheduler = BackgroundScheduler()
=======
#from login import configure_login
>>>>>>> a7b8a258312fef0da3078aab9216a54cf8e6dbaa

app = Flask(__name__)
API_KEY = '62beabd5-0e1f-4968-8c3d-62455aa321d1'
BASE_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
<<<<<<< HEAD
app.secret_key = 'Prince@ronaldo1'
login_manager = LoginManager(app)
user_data = {'user@example.com': {'password': 'user_password'}}
# MySQL Configuration
app.config['MYSQL_HOST'] = '3.85.54.217'
app.config['MYSQL_USER'] = 'ronaldochoiga'
app.config['MYSQL_PASSWORD'] = 'Ronaldo@choiga1'
=======
app.secret_key = 'secret_key'
user_data = {'user@example.com': {'password': 'user_password'}}
# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'ronaldochoiga'
app.config['MYSQL_PASSWORD'] = 'test_password'
>>>>>>> a7b8a258312fef0da3078aab9216a54cf8e6dbaa
app.config['MYSQL_DB'] = 'users_database'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


<<<<<<< HEAD
# The below code ensure proper logging of error for the flask application
handler = RotatingFileHandler('/var/log/flask_test/error.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.ERROR)
app.logger.addHandler(handler)

class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    # Load user from the database (replace this with your actual database logic)
    conn = pymysql.connect(host='3.85.54.217', user='ronaldochoiga', password='Ronaldo@choiga1', database='users_database')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    conn.close()

    if user_data:
        user = User(user_id=user_data[0], username=user_data[1], password=user_data[2])
        return user
    return None
@app.route('/')
def index():
#    return render_template('signup.html')
    return redirect('https://choigaronaldo.wixsite.com/my-site-2')
@app.route('/about_section')
def about_route():
    return render_template('signup.html')
#    return redirect('https://choigaronaldo.wixsite.com/my-site-2')
# Landing page section and redirections

@app.route('/signup', methods=['POST', 'GET'])
=======
@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
>>>>>>> a7b8a258312fef0da3078aab9216a54cf8e6dbaa
def signup():
    # Placeholder for signup logic (insert into database, etc.)
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    #hash the passwors before storage into the database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert user into the database (replace this with your actual database logic)
    try:
        cur = mysql.connection.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        mysql.connection.commit()
        cur.close()

<<<<<<< HEAD
        return redirect(url_for('login')) #, username=session['username']))
=======
        return redirect(url_for('dashboard', username=session['username']))
>>>>>>> a7b8a258312fef0da3078aab9216a54cf8e6dbaa

    except Exception as e:
        print(f"Error during signup: {e}")
        return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password_candidate = request.form['password']

<<<<<<< HEAD

=======
>>>>>>> a7b8a258312fef0da3078aab9216a54cf8e6dbaa
    # Fetch user from the database (replace this with your actual database logic)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.checkpw(password_candidate.encode('utf-8'), user['password'].encode('utf-8')):
<<<<<<< HEAD
        user_data = User(user_id=user['user_id'], username=user['username'], password=user['password'])
        # Password matched, store user data in the session
        session['username'] = user['username']
        login_user(user_data)
=======
        # Password matched, store user data in the session
        session['username'] = user['username']
>>>>>>> a7b8a258312fef0da3078aab9216a54cf8e6dbaa
        return redirect(url_for('dashboard'))
    else:
        error = 'Invalid login'
        return render_template('login.html', error=error)
def get_user_by_email(email):
<<<<<<< HEAD
    connection = pymysql.connect(host='3.85.54.217', user='ronaldochoiga', password='Ronaldo@choiga1', database='users_database')
=======
    connection = pymysql.connect(host='your_db_host', user='your_db_user', password='your_db_password', database='your_db_name')
>>>>>>> a7b8a258312fef0da3078aab9216a54cf8e6dbaa
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user_data = cursor.fetchone()
            return user_data
    finally:
        connection.close()
def generate_reset_token():
    return secrets.token_urlsafe(32)

@app.route('/forget_password')
def forget_password():
    return render_template('forget_password.html')

@app.route('/forget_password', methods=['POST'])
def forget_password_post():
    email = request.form.get('email')
    user_data = get_user_by_email(email)
    if email in user_data:
        # Generate reset token
        reset_token = generate_reset_token()

        # Store reset token in the session
        session['reset_token'] = reset_token

        # Placeholder for sending reset email (in a real application, send an email with the reset token link)
        print(f"Reset Token for {email}: {reset_token}")

        flash('Check your email for instructions to reset your password.')
    else:
        flash('Email not found.')

    return redirect(url_for('login'))
@app.route('/reset_password/<token>')
def reset_password(token):
    # Placeholder for reset password page
    return render_template('reset_password.html', reset_token=token)

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password_post(token):
    if 'reset_token' in session and session['reset_token'] == token:
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            if new_password == confirm_password:
                # Reset the password for the associated user (replace this with your actual logic)
                email = session['email']  # Replace with the email associated with the reset token
                user_data[email]['password'] = new_password

                # Clear the reset token from the session
                session.pop('reset_token', None)

                flash('Password reset successfully.')
                return redirect(url_for('login'))
            else:
                flash('Passwords do not match.')

        return render_template('reset_password.html', reset_token=token)
    else:
        flash('Invalid or expired reset token.')
        return redirect(url_for('login'))
<<<<<<< HEAD
def scheduled_job():
    print("running the scheduled job as usual after every minute")
    get_top_cryptocurrencies(limit=1000)
    # Schedule the job to be run every 1 minute
scheduler.add_job(id='job1', func=scheduled_job, trigger='interval', minutes=1)
# This starts the schedular in a separate thread
def get_user_id():
    if current_user.is_authenticated:
        return str(current_user.id)  # Convert the user ID to a string if necessary
    else:
        return None

=======
#def scheduled_job():
 #   print("running the scheduled job as usual after every minute")
 #   get_binance_gainers_losers()
# Schedule the job to be run every 1 minute
#schedular.add_job(id-'job1', func=scheduled_job, trigger='interval', minutes=1)
# This starts the schedular in a separate thread
>>>>>>> a7b8a258312fef0da3078aab9216a54cf8e6dbaa
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', username=session['username'])

@app.route('/gainers_fetch')
def gainers_fetch():
    # Check if the user is logged in
    if 'username' in session:
        return render_template('gainers_fetch.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/losers_fetch')
def losers_fetch():
    # This returns the losers table
    return render_template('losers_fetch.html')

@app.route('/Top_trade')
def higher_cap():
    #this function routes the toptrated file in the dasboard
    return render_template('higher_cap.html')
@app.route('/coingecko_route')
def coingecko():
    #the fuction redirects to coingecko api
    return render_template('coingecko_search.html')
@app.route('/coinmarketcap')
def coinmarketcap():
    # This function redirects to the cmc api
    return render_template('cmc_search.html')

# Add a route to fetch data (replace this with your actual logic)
@app.route('/get_data')
def get_data():
    table_name = 'cryptocurrency_data'
    # Fetch data from the database (replace this with your actual logic)
    data = fetch_top_gainers_from_database(table_name, limit=10)  # Replace this with your data fetching logic
<<<<<<< HEAD
    top_1000= get_top_cryptocurrencies(limit=1000)

#   top_1000 = get_binance_top_200()
=======

    top_1000 = get_binance_top_200()
>>>>>>> a7b8a258312fef0da3078aab9216a54cf8e6dbaa
    return jsonify(data)
@app.route('/get_losers')
def get_losers():
    # route to retrieve data from the database(the losers)
<<<<<<< HEAD
    top_1000 = get_top_cryptocurrencies(limit=1000)
    table_name = 'cryptocurrency_data'
    losers = fetch_top_losers_from_database(table_name, limit=10) #fetches the top losers from the database
#    top_1000 = get_binance_top_200()
    return jsonify(losers)

@app.route('/get_coin_details/<int:coin_id>')
def get_coin_details_route(coin_id):
    coin_name = get_coin_details(coin_id)

    if coin_name:
        # Redirect to CoinGecko search URL using the coin name
        search_url = f'https://www.coingecko.com/en/coins/{coin_name.lower().replace(" ", "-")}'
        return redirect(search_url)
    else:
        return jsonify({'error': 'Coin details not found'})
=======
    table_name = 'cryptocurrency_data'
    losers = fetch_top_losers_from_database(table_name, limit=10) #fetches the top losers from the database
    top_1000 = get_binance_top_200()
    return jsonify(losers)
>>>>>>> a7b8a258312fef0da3078aab9216a54cf8e6dbaa
@app.route('/top_traded')
def top_traded():
    table_name = 'cryptocurrency_data'
    top_cap = fetch_top_cap_from_database(table_name, limit=10) # Fetches the data with the highest market cap from binance trading.
<<<<<<< HEAD
    top_1000 = get_top_cryptocurrencies(limit=1000)
#    top_1000 = get_binance_top_200()
=======
    top_1000 = get_binance_top_200()
>>>>>>> a7b8a258312fef0da3078aab9216a54cf8e6dbaa
    return jsonify(top_cap)

@app.route('/cmc_search', methods=['GET', 'POST'])
def cmc_search():
    # The function allows one to get data on crypto after a redirection
    return render_template('cmc_search.html')
<<<<<<< HEAD

@app.route('/bsc_scan')
def bsc_info():
    labeled_addresses = get_labeled_addresses(current_user.id)
    return render_template('bsc_info.html', labeled_addresses=labeled_addresses)

@app.route('/add_address', methods=['POST'])
def add_address():
    print("adding addresses to the database")
    user_id = get_user_id()
    address = request.form.get('address')
    label = request.form.get('label')
    contract_address = request.form.get('contract_address')

    if user_id:
        # Assuming you have a function to insert labeled addresses associated with the user ID
        insert_labeled_address(user_id, address, label, contract_address)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'User not authenticated'})

@app.route('/get_labeled_addresses')
def retrieve_addresses():
    user_id = get_user_id()
    try:
        addresses = get_labeled_addresses(current_user.id)
        print("Addresses:", addresses)
        result = [{'address': address, 'label': label, 'contract_address': contract_address} for address, label, contract_address in addresses]

        return jsonify(result)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
@app.route('/get_info', methods=['POST'])
def get_info():
    user_address = request.form.get('user_address')
    contract_address = request.form.get('contract_address')

    balance = get_token_balance(user_address, contract_address)
    transactions = get_recent_transactions(user_address, contract_address)

    return jsonify({'balance': balance, 'transactions': transactions})
if __name__ == '__main__':
    scheduler.start()
=======
if __name__ == '__main__':
>>>>>>> a7b8a258312fef0da3078aab9216a54cf8e6dbaa
    app.run(debug=True)
