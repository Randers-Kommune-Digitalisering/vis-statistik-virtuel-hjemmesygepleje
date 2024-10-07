import datetime
import pytz


def last_week_for_year(year):
    last_week = datetime.date(year, 12, 28)
    return last_week.isocalendar().week


def generate_start_and_end_datetime_by_week(weeks, end):
    end_datetime = end + datetime.timedelta(minutes=1)
    start_datetime = end + datetime.timedelta(minutes=1) - datetime.timedelta(weeks=weeks)
    return start_datetime, end_datetime


def generate_start_and_end_datetime(days=None, start=None, end=None):
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


def get_fortnight_start_and_end(week):
    year, week = week.split('-')
    fortnight_end = datetime.datetime.fromisocalendar(int(year), int(week)+1, 1)
    fortnight_start = fortnight_end - datetime.timedelta(weeks=2)
    return fortnight_start, fortnight_end - datetime.timedelta(seconds=1)


def get_last_week():
    current_year, current_week, _ = (datetime.date.today() - datetime.timedelta(days=7)).isocalendar()
    return f'{current_year}-{current_week}'


def get_weeks(start_week, end_week):
    min_year, min_week = [int(x) for x in start_week.split('-')]
    max_year, max_week = [int(x) for x in end_week.split('-')]

    if min_year == max_year:
        return [f'{min_year}-{str(week).zfill(2)}' for week in range(min_week, max_week+1)]
    else:
        week_list = []
        for year in range(min_year, max_year+1):
            sw = min_week if year == min_year else 1
            ew = max_week if year == max_year else last_week_for_year(year)
            week_list += [f'{year}-{str(week).zfill(2)}' for week in range(sw, ew+1)]

        return week_list


def format_decimal_hours(decimal_hours):
    from datetime import timedelta
    return str(timedelta(hours=decimal_hours)).replace('days', 'døgn')
