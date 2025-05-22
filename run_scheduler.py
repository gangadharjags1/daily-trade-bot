# run_scheduler.py

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import pytz
import subprocess

def run_bot_cycle():
    now = datetime.now(pytz.timezone("US/Central")).strftime("%Y-%m-%d %H:%M:%S")
    print(f"⏱️ Running bot at {now}...")
    subprocess.run(["python", "main.py"])  # This runs your existing trading bot

scheduler = BlockingScheduler(timezone="US/Central")

# Run every 10 minutes between 8:30 AM and 3:30 PM CST
scheduler.add_job(run_bot_cycle, 'cron', minute='*/10', hour='8-15', day_of_week='mon-fri')

print("✅ Scheduler started. Bot will run every 10 minutes from 8:30 AM to 3:30 PM CST.")
scheduler.start()
