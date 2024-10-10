import pandas as pd
# import numpy as np
from datetime import timedelta

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from models import OU, Call, WeeklyStat
from database import get_calls, get_engine
from utils.time import get_week_start_and_end, get_last_week, format_decimal_hours
from utils.ou import get_district_vitacomm, get_nexus_district
from utils.call import only_employee_to_resident, only_answered_calls


def get_calls_dataframe(week=None, deltadays=None):
    if week is None:
        week = get_last_week()

    start, end = get_week_start_and_end(week)
    if deltadays:
        return get_calls(days=deltadays, end=end)
    else:
        return get_calls(start_=start, end=end)


def answered_unanwsered_by_district(dataframe, district_id=None):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    if district_id:
        df = df[df['callee_district'].str.contains(district_id)]

    df = only_employee_to_resident(df)

    # Assuming that an answered calls have a duration greater than 0 and vice versa
    data = {'answered': [len(df[df['duration'] > timedelta(seconds=0)])], 'unanswered': [len(df[df['duration'] == timedelta(seconds=0)])]}

    return pd.DataFrame(data)


def answered_unanwsered_all_districts(dataframe):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    # Assuming that an answered calls have a duration greater than 0 and vice versa
    df = df.groupby('caller_district_id')['duration'].apply(lambda x: pd.Series([(x > timedelta(seconds=0)).sum(), (x == timedelta(seconds=0)).sum()])).unstack()

    df = df.reset_index()

    df.columns = ['caller_district_id', 'answered', 'unanswered']

    return df


def average_duration_all_districts(dataframe):
    print('HEJ!!!')
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    df = only_employee_to_resident(df)
    df = only_answered_calls(df)

    overall_avg_duration = pd.to_timedelta(df['duration'].mean(), unit='s')
    df.loc[:, 'duration'] = pd.to_timedelta(df['duration'], unit='s')

    durations_df = df.groupby('caller_district_id')['duration'].mean().sort_values(ascending=False)
    durations_df = durations_df.sort_index(ascending=True)
    durations_df = pd.concat([durations_df, pd.Series(overall_avg_duration, index=[0])])
    # durations_df.index.names = ['Distrikt']
    # durations_df.name = 'Gennemsnitlig varighed'
    durations_df = durations_df.astype(str).str[10:].str.split('.').str[0]

    return durations_df


def unique_citizens(dataframe, callee_district=True):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    df = only_employee_to_resident(df)
    df = only_answered_calls(df)

    if callee_district:
        citizens_s = df.groupby('caller_district_id')['callee_cpr'].nunique().sort_values(ascending=False)
    else:
        citizens_s = df.groupby('caller_district_id')['callee_cpr'].nunique().sort_values(ascending=False)

    citizens_s = pd.concat([citizens_s, pd.Series(df['callee_cpr'].nunique(), index=[0])])
    # citizens_s.name = 'Borgere med opkald'

    return citizens_s


def visits_data(dataframe):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    df = only_employee_to_resident(df)
    df = only_answered_calls(df)

    citizens_s = df.groupby('caller_district_id')['callee_cpr'].nunique().sort_values(ascending=False)
    citizens_s = pd.concat([citizens_s, pd.Series(df['callee_cpr'].nunique(), index=[0])])
    # citizens_s.name = 'Borgere med opkald'

    duration_s = df.groupby('caller_district_id')['duration'].sum()
    duration_s = pd.concat([duration_s, pd.Series(df['duration'].sum(), index=[0])])
    # duration_s = duration_s.apply(lambda x: format_decimal_hours((x.seconds / 3600)))
    # duration_s.name = 'Tid i opkald'

    calls_s = df.groupby('caller_district')['id'].count()
    calls_s = pd.concat([calls_s, pd.Series(df['id'].count(), index=[0])])
    # calls_s.name = 'Besvarede opkald'

    return pd.concat([citizens_s, duration_s, calls_s], axis=1)


def get_children(ou):
    with Session(get_engine()) as session:
        ous = session.query(OU).filter(OU.nexus_name == ou).all()
        if any(ou.children for ou in ous):
            children = []
            for ou in ous:
                if ou.children:
                    children.extend([child.nexus_name for child in ou.children])
            return children
        return []


def get_call_data(week=None, ou=None):
    if week is None:
        week = get_last_week()

    start, end = get_week_start_and_end(week)
    start_active_residents = start - timedelta(days=21)

    with Session(get_engine()) as session:
        total_calls, answered_calls, unansered_calls, average_duration, active_residents = None, None, None, None, None
        if ou:
            ous = session.query(OU).filter(OU.nexus_name == ou).all()
            ou_ids = [ou.id for ou in ous]
            if any([ou.children for ou in ous]):
                total_calls = session.query(Call).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(OU.parent_id.in_(ou_ids)).count()
                answered_calls = session.query(Call).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(OU.parent_id.in_(ou_ids)).count()
                average_duration = session.query(Call).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(OU.parent_id.in_(ou_ids)).with_entities(func.avg(Call.duration)).scalar()
                active_residents = session.query(Call).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start_active_residents, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(OU.parent_id.in_(ou_ids)).distinct(Call.callee_cpr).count()
                all_residents = session.query(func.sum(WeeklyStat.residents)).join(OU, WeeklyStat.ou_id == OU.id).filter(WeeklyStat.week == week).filter(OU.parent_id.in_(ou_ids)).scalar()
                # active_residents_test = session.query(Call.callee_cpr).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start, Call.start_time <= end, OU.parent_id == ou.id, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).distinct(Call.callee_cpr).all()
            else:
                total_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(Call.caller_ou_id.in_(ou_ids)).count()
                answered_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(Call.caller_ou_id.in_(ou_ids)).count()
                average_duration = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(Call.caller_ou_id.in_(ou_ids)).with_entities(func.avg(Call.duration)).scalar()
                active_residents = session.query(Call).filter(and_(Call.start_time >= start_active_residents, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(Call.caller_ou_id.in_(ou_ids)).distinct(Call.callee_cpr).count()
                all_residents = session.query(WeeklyStat.residents).filter(WeeklyStat.week == week).filter(WeeklyStat.ou_id.in_(ou_ids)).scalar()
                # active_residents_test = session.query(Call.callee_cpr).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.caller_ou_id == ou.id, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).distinct(Call.callee_cpr).all()
        else:
            total_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).count()
            answered_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).count()
            average_duration = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).with_entities(func.avg(Call.duration)).scalar()
            active_residents = session.query(Call).filter(and_(Call.start_time >= start_active_residents, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).distinct(Call.callee_cpr).count()
            all_residents = session.query(func.sum(WeeklyStat.residents)).filter(WeeklyStat.week == week).scalar()
            # active_residents_test = session.query(Call.callee_cpr).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).distinct(Call.callee_cpr).all()

        unansered_calls = total_calls - answered_calls

        if not all_residents:
            all_residents = 0

        if all_residents == 0:
            conversion_rate = 0
        else:
            conversion_rate = active_residents / all_residents

        if active_residents == 0:
            use_level = 0
        else:
            use_level = answered_calls / active_residents / 7

        if not average_duration:
            average_duration = timedelta(seconds=0)

        return {"Opkald i alt": total_calls, "Opkald besvarede": answered_calls, "Opkald Ubesvarede": unansered_calls, "Opkald gennemsnitlig varighed": average_duration, "Borgere i alt": all_residents,  "Borgere aktive": active_residents, "Borgere inaktive": '-', "Anvendelsesgrad": use_level, "Omlægningsgrad": conversion_rate}  # , "active_residents_test": active_residents_test}
    