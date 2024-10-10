import sys
import threading
from datetime import datetime
from streamlit.web import cli as stcli
from apscheduler.schedulers.background import BackgroundScheduler

from database import create_db, seed_db, seed_call_logs, update_call_db
from nexus import read_bi_data

sched = BackgroundScheduler()


def start_up_job():
    seed_call_logs()
    read_bi_data()


def hourly_job():
    update_call_db(days=1, start=datetime.now())


def daily_job():
    read_bi_data()


def setup():
    create_db()
    seed_db()


if __name__ == '__main__':
    setup()

    sched.add_job(start_up_job, 'date', run_date=datetime.now())
    sched.add_job(hourly_job, 'cron', minute='30')
    sched.add_job(daily_job, 'cron', hour='12', minute='45')
    sched.start()

    sys.argv = ["streamlit", "run", "streamlit_app.py", "--client.toolbarMode=minimal", "--server.port=8080"] # "--server.address=0.0.0.0"]
    sys.exit(stcli.main())






    # from database import seed_db_new
    # create_db()
    # seed_db_new()


    # # import re
    # # from vitacomm import get_call_log_api
    # # import pandas as pd
    # # from io import StringIO

    # call_log = get_call_log_api()
    # data = StringIO(call_log)
    # df = pd.read_csv(data, sep=';', dtype={"Caller's CPR": str, "Callee's CPR": str})

    # print(df['Caller OU'].unique())

    # df.dropna(how='all', inplace=True)
    # df.dropna(how='all', axis=1, inplace=True)

    # df = df.drop(columns=['CallerAlias', 'Media info'])
    # df.columns = [re.sub(r"'s|\(|\)", "", c.lower().replace(' ', '_')) for c in list(df)]
    # pd.set_option('display.max_columns', None)
    # print(df)
