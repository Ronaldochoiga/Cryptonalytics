from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from binance_api.binance_mc import get_binance_top_200
from binance_api.gainers_fetch import fetch_top_gainers_from_database
from binance_api.losers_fetch import fetch_top_losers_from_database
from binance_api.higher_cap import fetch_top_cap_from_database
#from cmc_api.search_info import get_crypto_details
#from flask_apscheduler import APScheduler #imports the apscheduler extension
import time
import threading
from flask_mysqldb import MySQL
import bcrypt
import secrets
import pymysql
#from login import configure_login

app = Flask(__name__)
API_KEY = '62beabd5-0e1f-4968-8c3d-62455aa321d1'
BASE_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
app.secret_key = 'test_secret'
user_data = {'user@example.com': {'password': 'user_password'}}
# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'test_password'
app.config['MYSQL_DB'] = 'users_database'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
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

        return redirect(url_for('dashboard', username=session['username']))

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

    # Fetch user from the database (replace this with your actual database logic)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.checkpw(password_candidate.encode('utf-8'), user['password'].encode('utf-8')):
        # Password matched, store user data in the session
        session['username'] = user['username']
        return redirect(url_for('dashboard'))
    else:
        error = 'Invalid login'
        return render_template('login.html', error=error)
def get_user_by_email(email):
    connection = pymysql.connect(host='localhost', user='ronaldochoiga', password='test_password', database='users_database')
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
#def scheduled_job():
 #   print("running the scheduled job as usual after every minute")
 #   get_binance_gainers_losers()
# Schedule the job to be run every 1 minute
#schedular.add_job(id-'job1', func=scheduled_job, trigger='interval', minutes=1)
# This starts the schedular in a separate thread
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

    top_1000 = get_binance_top_200()
    return jsonify(data)
@app.route('/get_losers')
def get_losers():
    # route to retrieve data from the database(the losers)
    table_name = 'cryptocurrency_data'
    losers = fetch_top_losers_from_database(table_name, limit=10) #fetches the top losers from the database
    top_1000 = get_binance_top_200()
    return jsonify(losers)
@app.route('/top_traded')
def top_traded():
    table_name = 'cryptocurrency_data'
    top_cap = fetch_top_cap_from_database(table_name, limit=10) # Fetches the data with the highest market cap from binance trading.
    top_1000 = get_binance_top_200()
    return jsonify(top_cap)

@app.route('/cmc_search', methods=['GET', 'POST'])
def cmc_search():
    # The function allows one to get data on crypto after a redirection
    return render_template('cmc_search.html')
if __name__ == '__main__':
    app.run(debug=True)
