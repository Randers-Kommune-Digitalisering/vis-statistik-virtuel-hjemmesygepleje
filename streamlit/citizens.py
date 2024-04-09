from dateutil import parser

from vitacomm import get_active_citizens
from utils.time import generate_start_and_end_datetime
from utils.district import get_district_applikator_id

def amount_active_citizens(district='all', delta_days=30, start_time=None, end_time=None):
    start_datetime, end_datetime = generate_start_and_end_datetime(delta_days, start_time, end_time)
    citizens = get_active_citizens()
    if district == 'all':
        login_times = [parser.parse(c['lastLoggedInAt']) for c in citizens]
    else:
        district_ids = get_district_applikator_id(district)
        if district_ids:
            login_times = [parser.parse(c['lastLoggedInAt']) for c in  filter(lambda c: c['organizationalUnitId'] in district_ids, citizens)]
        else:
            return 0
        
    return len([i for i in login_times if start_datetime < i < end_datetime])