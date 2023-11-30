from flask_mysqldb import MySQL

# Create a MySQL instance
mysql = MySQL()

def init_app(app):
    # Initialize the app with MySQL configurations
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'test_password'
    app.config['MYSQL_DB'] = 'users_database'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    mysql.init_app(app)

def insert_user(username, email, password):
    # Insert user information into the database
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
            mysql.connection.commit()
    except Exception as e:
        print(f"Error inserting into database: {e}")
        mysql.connection.rollback()

# You can add more functions for other database operations if needed
