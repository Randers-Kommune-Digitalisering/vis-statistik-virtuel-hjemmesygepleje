import datetime
import pytz

def generate_start_and_end_datetime(days, start, end):
    local_tz = pytz.timezone('Europe/Copenhagen')

    if start and end:
        if start > end:
            raise Exception('End time before start time')
        end_datetime = local_tz.localize(end)
        start_datetime = local_tz.localize(start)
    elif end:
        if not days:
            raise Exception('No delta_days')
        end_datetime = local_tz.localize(end)
        start_datetime = local_tz.localize(end) - datetime.timedelta(days)
    elif start:
        if not days:
            raise Exception('No delta_days')
        start_datetime = local_tz.localize(start)
        end_datetime = local_tz.localize(start) + datetime.timedelta(days)
    else:
        if not days:
            raise Exception('No delta_days')
        end_datetime = datetime.datetime.now(local_tz) - datetime.timedelta(minutes=1)
        start_datetime = end_datetime - datetime.timedelta(days)
    
    return start_datetime, end_datetime

def get_week_start_and_end(week):
    year, week = week.split('-')
    week_start = datetime.datetime.fromisocalendar(int(year), int(week), 1)
    week_end = week_start + datetime.timedelta(weeks=1) - datetime.timedelta(seconds=1)
    return week_start, week_end

def get_last_week():
    current_year, current_week, _ = (datetime.date.today() - datetime.timedelta(days=7)).isocalendar()
    return f'{current_year}-{current_week}'
    
def format_decimal_hours(decimal_hours):
    from datetime import timedelta
    return  str(timedelta(hours=decimal_hours)).replace('days', 'døgn')
    hours = int(decimal_hours)
    minutes = int((decimal_hours*60) % 60)
    seconds = int((decimal_hours*3600) % 60)
    return f'{hours}:{minutes}:{seconds}'
