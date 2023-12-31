#!/usr/bin/python3
from flask import request
from flask_mysqldb import MySQL

def configure_login(app):
    # Configure MySQL
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'ronaldochoiga'
    app.config['MYSQL_PASSWORD'] = 'test_password'
    app.config['MYSQL_DB'] = 'users_database'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql = MySQL(app)

    @app.route('/login')
    def login():
        return render_template('login.html')
    @app.route('/login', methods=['POST'])
    def login_post():
        username = request.form['username']
        password_candidate = request.form['password']

        # Fetch user from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user:
            # Check password
            if bcrypt.checkpw(password_candidate.encode('utf-8'), user['password'].encode('utf-8')):
                # Password matched, store user data in the session
                session['username'] = user['username']
                return redirect(url_for('gainers_fetch.html'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
