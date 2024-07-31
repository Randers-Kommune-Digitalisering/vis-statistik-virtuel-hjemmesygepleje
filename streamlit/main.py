import sys
from datetime import datetime
from streamlit.web import cli as stcli
from apscheduler.schedulers.background import BackgroundScheduler

from database import create_db, seed_db, update_call_db
from nexus import read_bi_data

sched = BackgroundScheduler()

def hourly_job():
    update_call_db(days=1, start=datetime.now())

def daily_job():
    read_bi_data()

def setup():
    create_db()
    seed_db()
    read_bi_data()

if __name__ == '__main__':
    setup()

    sched.add_job(hourly_job, 'cron', minute='30')
    sched.add_job(daily_job, 'cron', hour='12', minute='45')
    sched.start()

    sys.argv = ["streamlit", "run", "streamlit_app.py", "--client.toolbarMode=auto", "--server.port=8501", "--server.address=0.0.0.0"]
    sys.exit(stcli.main())
