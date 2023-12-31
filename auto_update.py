from threading import Thread
from time import sleep
from flask import Flask
from flask_apscheduler import APScheduler
from binance_api.gainers_losers import get_binance_gainers_losers

app = Flask(__name__)

# Set the interval for automatic API reload (in seconds)
AUTO_RELOAD_INTERVAL = 300  # 1 minute, adjust as needed

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Function to update Binance data (replace this with your actual update function)
def update_data_job():
    fetch_data_from_database(table_name)

# Schedule the job to run at the specified interval
scheduler.add_job(id='update_data_job', func=update_data_job, trigger='interval', seconds=AUTO_RELOAD_INTERVAL)

# Thread to run the Flask development server with autoreload
def run_flask():
    app.run(debug=True)

if __name__ == '__main__':
    # Start the Flask development server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Sleep to allow time for Flask to start before scheduling the job
    sleep(2)

    # Schedule the job to run immediately on startup
    scheduler.get_job('update_data_job').modify(next_run_time=None)
    
    flask_thread.join()  # Wait for the Flask thread to finish
