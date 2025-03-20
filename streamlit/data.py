import pandas as pd
# import numpy as np
from datetime import timedelta

from sqlalchemy import and_, or_, func
from sqlalchemy.orm import Session

from models import OU, Call, WeeklyStat, Service
from database import get_calls, get_engine
from utils.time import get_week_start_and_end, get_last_week
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


def get_children(ou, keywords=None):
    with Session(get_engine()) as session:
        # start new way (hacky) #
        if keywords:
            if ou.lower() in keywords:
                children = session.query(OU.nexus_name).filter(OU.nexus_name.contains(ou)).distinct().all()
                return [child.nexus_name for child in children]
        # end new way#

        ous = session.query(OU).filter(OU.nexus_name == ou).all()
        if any(ou.children for ou in ous):
            children = []
            for ou in ous:
                if ou.children:
                    children.extend([child.nexus_name for child in ou.children])

            # start new way (hacky) #
            if keywords:
                if any('område' in ou.nexus_name.lower() for ou in ous):
                    children = [child for child in children if not any(keyword in child.lower() for keyword in keywords)]
                elif 'kultur og omsorg' in ou.nexus_name.lower():
                    children.extend([word.capitalize() for word in keywords])
            # end new way #

            return children
        return []


# start new way (hacky) #
def get_filtered_overview_data(week=None, ou=None, keywords_exclude=None):
    if week is None:
        week = get_last_week()

    start, end = get_week_start_and_end(week)

    with Session(get_engine()) as session:
        total_calls, answered_calls, unanswered_calls, average_duration, active_residents = None, None, None, None, None
        if ou:
            ous = session.query(OU).filter(OU.nexus_name.contains(ou)).all()
            ous_children = [child for ou in ous for child in ou.children]

            if keywords_exclude:
                ous = [ou for ou in ous if not any([keyword.lower() in ou.nexus_name.lower() for keyword in keywords_exclude])]
                ous_children = [ou for ou in ous_children if not any([keyword.lower() in ou.nexus_name.lower() for keyword in keywords_exclude])]

            ou_ids = [ou.id for ou in ous]

            ou_children_ids = [child.id for child in ous_children]
            if any([ou.children for ou in ous]):
                total_calls = session.query(Call).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(OU.id.in_(ou_children_ids)).count()
                answered_calls = session.query(Call).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(OU.id.in_(ou_children_ids)).count()
                average_duration = session.query(Call).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(OU.id.in_(ou_children_ids)).with_entities(func.avg(Call.duration)).scalar()
                active_residents = session.query(Call).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(OU.id.in_(ou_children_ids)).distinct(Call.callee_cpr).count()
                all_residents = session.query(func.sum(WeeklyStat.residents)).join(OU, WeeklyStat.ou_id == OU.id).filter(WeeklyStat.week == week).filter(OU.id.in_(ou_children_ids)).scalar()
            else:
                total_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(Call.caller_ou_id.in_(ou_ids)).count()
                answered_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(Call.caller_ou_id.in_(ou_ids)).count()
                average_duration = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(Call.caller_ou_id.in_(ou_ids)).with_entities(func.avg(Call.duration)).scalar()
                active_residents = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(Call.caller_ou_id.in_(ou_ids)).distinct(Call.callee_cpr).count()
                all_residents = session.query(func.sum(WeeklyStat.residents)).filter(WeeklyStat.week == week).filter(WeeklyStat.ou_id.in_(ou_ids)).scalar()
        else:
            if keywords_exclude:
                ous_to_exclude = session.query(OU).filter(or_(*[func.lower(OU.nexus_name).contains(keyword.lower()) for keyword in keywords_exclude])).all()
                ou_ids_to_exclude = [ou.id for ou in ous_to_exclude]

                total_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee', ~Call.caller_ou_id.in_(ou_ids_to_exclude))).count()
                answered_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee', ~Call.caller_ou_id.in_(ou_ids_to_exclude))).count()
                average_duration = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee', ~Call.caller_ou_id.in_(ou_ids_to_exclude))).with_entities(func.avg(Call.duration)).scalar()
                active_residents = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee', ~Call.caller_ou_id.in_(ou_ids_to_exclude))).distinct(Call.callee_cpr).count()
                all_residents = session.query(func.sum(WeeklyStat.residents)).filter(WeeklyStat.week == week, ~WeeklyStat.ou_id.in_(ou_ids_to_exclude)).scalar()
            else:
                total_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).count()
                answered_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).count()
                average_duration = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).with_entities(func.avg(Call.duration)).scalar()
                active_residents = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).distinct(Call.callee_cpr).count()
                all_residents = session.query(func.sum(WeeklyStat.residents)).filter(WeeklyStat.week == week).scalar()

        unanswered_calls = total_calls - answered_calls

        if not all_residents:
            all_residents = '-'

        if all_residents == 0:
            conversion_rate = 0
        elif all_residents == '-':
            conversion_rate = '-'
        else:
            conversion_rate = active_residents / all_residents

        if active_residents == 0:
            use_level = 0
        else:
            use_level = answered_calls / active_residents / 7

        if not average_duration:
            average_duration = timedelta(seconds=0)

        return {"Opkald besvarede": answered_calls, "Opkald ubesvarede": unanswered_calls, "Opkald gennemsnitlig varighed": average_duration, "Borgere aktive": active_residents, "Anvendelsesgrad": use_level, "Omlægningsgrad": conversion_rate}
# end new way #


def get_overview_data(week=None, ou=None):
    if week is None:
        week = get_last_week()

    start, end = get_week_start_and_end(week)
    # start_active_residents = start - timedelta(days=21)

    with Session(get_engine()) as session:
        total_calls, answered_calls, unanswered_calls, average_duration, active_residents = None, None, None, None, None
        if ou:
            ous = session.query(OU).filter(OU.nexus_name == ou).all()
            ou_ids = [ou.id for ou in ous]
            if any([ou.children for ou in ous]):
                total_calls = session.query(Call).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(OU.parent_id.in_(ou_ids)).count()
                answered_calls = session.query(Call).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(OU.parent_id.in_(ou_ids)).count()
                average_duration = session.query(Call).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(OU.parent_id.in_(ou_ids)).with_entities(func.avg(Call.duration)).scalar()
                active_residents = session.query(Call).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(OU.parent_id.in_(ou_ids)).distinct(Call.callee_cpr).count()
                all_residents = session.query(func.sum(WeeklyStat.residents)).join(OU, WeeklyStat.ou_id == OU.id).filter(WeeklyStat.week == week).filter(OU.parent_id.in_(ou_ids)).scalar()
                # active_residents_test = session.query(Call.callee_cpr).join(OU, Call.caller_ou_id == OU.id).filter(and_(Call.start_time >= start, Call.start_time <= end, OU.parent_id == ou.id, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).distinct(Call.callee_cpr).all()
            else:
                total_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(Call.caller_ou_id.in_(ou_ids)).count()
                answered_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(Call.caller_ou_id.in_(ou_ids)).count()
                average_duration = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(Call.caller_ou_id.in_(ou_ids)).with_entities(func.avg(Call.duration)).scalar()
                active_residents = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).filter(Call.caller_ou_id.in_(ou_ids)).distinct(Call.callee_cpr).count()
                all_residents = session.query(WeeklyStat.residents).filter(WeeklyStat.week == week).filter(WeeklyStat.ou_id.in_(ou_ids)).scalar()
                # active_residents_test = session.query(Call.callee_cpr).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.caller_ou_id == ou.id, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).distinct(Call.callee_cpr).all()
        else:
            total_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).count()
            answered_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).count()
            average_duration = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).with_entities(func.avg(Call.duration)).scalar()
            active_residents = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Resident', Call.caller_role == 'Employee')).distinct(Call.callee_cpr).count()
            all_residents = session.query(func.sum(WeeklyStat.residents)).filter(WeeklyStat.week == week).scalar()
            # active_residents_test = session.query(Call.callee_cpr).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Resident', Call.caller_role == 'Employee')).distinct(Call.callee_cpr).all()

        unanswered_calls = total_calls - answered_calls

        if not all_residents:
            all_residents = '-'

        if all_residents == 0:
            conversion_rate = 0
        elif all_residents == '-':
            conversion_rate = '-'
        else:
            conversion_rate = active_residents / all_residents

        if active_residents == 0:
            use_level = 0
        else:
            use_level = answered_calls / active_residents / 7

        if not average_duration:
            average_duration = timedelta(seconds=0)

        return {"Opkald besvarede": answered_calls, "Opkald ubesvarede": unanswered_calls, "Opkald gennemsnitlig varighed": average_duration, "Borgere aktive": active_residents, "Anvendelsesgrad": use_level, "Omlægningsgrad": conversion_rate}  # , "active_residents_test": active_residents_test}


# start new way (hacky) #
def get_filtered_employee_data(week=None, ou=None, keywords_exclude=None):
    if week is None:
        week = get_last_week()

    start, end = get_week_start_and_end(week)

    with Session(get_engine()) as session:
        total_calls, answered_calls, unanswered_calls, average_duration = None, None, None, None
        if ou:
            ous = session.query(OU).filter(OU.nexus_name.contains(ou)).all()
            ous_children = [child for ou in ous for child in ou.children]

            if keywords_exclude:
                ous = [ou for ou in ous if not any([keyword.lower() in ou.nexus_name.lower() for keyword in keywords_exclude])]
                ous_children = [ou for ou in ous_children if not any([keyword.lower() in ou.nexus_name.lower() for keyword in keywords_exclude])]

            ou_ids = [ou.id for ou in ous]

            ou_children_ids = [child.id for child in ous_children]
            if any([ou.children for ou in ous]):
                total_calls = session.query(Call).join(OU, or_(Call.caller_ou_id == OU.id, Call.callee_ou_id == OU.id)).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Employee', Call.caller_role == 'Employee')).filter(OU.id.in_(ou_children_ids)).count()
                answered_calls = session.query(Call).join(OU, or_(Call.caller_ou_id == OU.id, Call.callee_ou_id == OU.id)).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee')).filter(OU.id.in_(ou_children_ids)).count()
                average_duration = session.query(Call).join(OU, or_(Call.caller_ou_id == OU.id, Call.callee_ou_id == OU.id)).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee')).filter(OU.id.in_(ou_children_ids)).with_entities(func.avg(Call.duration)).scalar()
            else:
                total_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Employee', Call.caller_role == 'Employee')).filter(or_(Call.caller_ou_id.in_(ou_ids), Call.callee_ou_id.in_(ou_ids))).count()
                answered_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee')).filter(or_(Call.caller_ou_id.in_(ou_ids), Call.callee_ou_id.in_(ou_ids))).count()
                average_duration = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee')).filter(or_(Call.caller_ou_id.in_(ou_ids), Call.callee_ou_id.in_(ou_ids))).with_entities(func.avg(Call.duration)).scalar()
        else:
            if keywords_exclude:
                ous_to_exclude = session.query(OU).filter(or_(*[func.lower(OU.nexus_name).contains(keyword.lower()) for keyword in keywords_exclude])).all()
                ou_ids_to_exclude = [ou.id for ou in ous_to_exclude]

                total_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Employee', Call.caller_role == 'Employee', ~Call.caller_ou_id.in_(ou_ids_to_exclude), ~Call.callee_ou_id.in_(ou_ids_to_exclude))).count()
                answered_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee', ~Call.caller_ou_id.in_(ou_ids_to_exclude), ~Call.callee_ou_id.in_(ou_ids_to_exclude))).count()
                average_duration = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee', ~Call.caller_ou_id.in_(ou_ids_to_exclude), ~Call.callee_ou_id.in_(ou_ids_to_exclude))).with_entities(func.avg(Call.duration)).scalar()
            else:
                total_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Employee', Call.caller_role == 'Employee')).count()
                answered_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee')).count()
                average_duration = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee')).with_entities(func.avg(Call.duration)).scalar()

        unanswered_calls = total_calls - answered_calls

        if not average_duration:
            average_duration = timedelta(seconds=0)

        return {"Opkald besvarede": answered_calls, "Opkald ubesvarede": unanswered_calls, "Opkald gennemsnitlig varighed": average_duration}
# end new way #


def get_employee_data(week=None, ou=None):
    if week is None:
        week = get_last_week()

    start, end = get_week_start_and_end(week)

    with Session(get_engine()) as session:
        total_calls, answered_calls, unanswered_calls, average_duration = None, None, None, None
        if ou:
            ous = session.query(OU).filter(OU.nexus_name == ou).all()
            ou_ids = [ou.id for ou in ous]
            if any([ou.children for ou in ous]):
                total_calls = session.query(Call).join(OU, or_(Call.caller_ou_id == OU.id, Call.callee_ou_id == OU.id)).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Employee', Call.caller_role == 'Employee')).filter(OU.parent_id.in_(ou_ids)).count()
                answered_calls = session.query(Call).join(OU, or_(Call.caller_ou_id == OU.id, Call.callee_ou_id == OU.id)).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee')).filter(OU.parent_id.in_(ou_ids)).count()
                average_duration = session.query(Call).join(OU, or_(Call.caller_ou_id == OU.id, Call.callee_ou_id == OU.id)).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee')).filter(OU.parent_id.in_(ou_ids)).with_entities(func.avg(Call.duration)).scalar()
            else:
                total_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Employee', Call.caller_role == 'Employee')).filter(or_(Call.caller_ou_id.in_(ou_ids), Call.callee_ou_id.in_(ou_ids))).count()
                answered_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee')).filter(or_(Call.caller_ou_id.in_(ou_ids), Call.callee_ou_id.in_(ou_ids))).count()
                average_duration = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee')).filter(or_(Call.caller_ou_id.in_(ou_ids), Call.callee_ou_id.in_(ou_ids))).with_entities(func.avg(Call.duration)).scalar()
        else:
            total_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.callee_role == 'Employee', Call.caller_role == 'Employee')).count()
            answered_calls = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee')).count()
            average_duration = session.query(Call).filter(and_(Call.start_time >= start, Call.start_time <= end, Call.duration > timedelta(seconds=0), Call.callee_role == 'Employee', Call.caller_role == 'Employee')).with_entities(func.avg(Call.duration)).scalar()

        unanswered_calls = total_calls - answered_calls

        if not average_duration:
            average_duration = timedelta(seconds=0)

        return {"Opkald besvarede": answered_calls, "Opkald ubesvarede": unanswered_calls, "Opkald gennemsnitlig varighed": average_duration}


def get_service_data(week=None, ou=None):
    if week is None:
        week = get_last_week()

    screen_visit, visit, call_visit = None, None, None

    with Session(get_engine()) as session:
        if ou:
            ous = session.query(OU).filter(OU.nexus_name == ou).all()
            ou_ids = [ou.id for ou in ous]
            if any([ou.children for ou in ous]):
                screen_visit = session.query(Service.name, func.sum(Service.visits).label('visits')).join(OU, Service.ou_id == OU.id).filter(OU.parent_id.in_(ou_ids)).filter(Service.week == week).filter(Service.type == "Skærmbesøg").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
                visit = session.query(Service.name, func.sum(Service.visits).label('visits')).join(OU, Service.ou_id == OU.id).filter(OU.parent_id.in_(ou_ids)).filter(Service.week == week).filter(Service.type == "Besøg").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
                call_visit = session.query(Service.name, func.sum(Service.visits).label('visits')).join(OU, Service.ou_id == OU.id).filter(OU.parent_id.in_(ou_ids)).filter(Service.week == week).filter(Service.type == "Telefonopkald").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
            else:
                screen_visit = session.query(Service).filter(Service.ou_id.in_(ou_ids)).filter(Service.week == week).filter(Service.type == "Skærmbesøg").order_by(Service.visits.desc()).with_entities(Service.name, Service.visits).all()
                visit = session.query(Service).filter(Service.ou_id.in_(ou_ids)).filter(Service.week == week).filter(Service.type == "Besøg").order_by(Service.visits.desc()).with_entities(Service.name, Service.visits).all()
                call_visit = session.query(Service).filter(Service.ou_id.in_(ou_ids)).filter(Service.week == week).filter(Service.type == "Telefonopkald").order_by(Service.visits.desc()).with_entities(Service.name, Service.visits).all()
        else:
            screen_visit = session.query(Service.name, func.sum(Service.visits).label('visits')).filter(Service.week == week).filter(Service.type == "Skærmbesøg").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
            visit = session.query(Service.name, func.sum(Service.visits).label('visits')).filter(Service.week == week).filter(Service.type == "Besøg").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
            call_visit = session.query(Service.name, func.sum(Service.visits).label('visits')).filter(Service.week == week).filter(Service.type == "Telefonopkald").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()

    screen_visit_list = [{"name": service.name, "visits": service.visits} for service in screen_visit]
    visit_list = [{"name": service.name, "visits": service.visits} for service in visit]
    call_visit_list = [{"name": service.name, "visits": service.visits} for service in call_visit]

    return {"Besøg": visit_list, "Skærmbesøg": screen_visit_list, "Telefonopkald": call_visit_list}


# start new way (hacky) #
def get_filtered_service_data(week=None, ou=None, keywords_exclude=None):
    if week is None:
        week = get_last_week()

    screen_visit, visit, call_visit = None, None, None

    with Session(get_engine()) as session:
        if ou:
            ous = session.query(OU).filter(OU.nexus_name.contains(ou)).all()
            ous_children = [child for ou in ous for child in ou.children]

            if keywords_exclude:
                ous = [ou for ou in ous if not any([keyword.lower() in ou.nexus_name.lower() for keyword in keywords_exclude])]
                ous_children = [ou for ou in ous_children if not any([keyword.lower() in ou.nexus_name.lower() for keyword in keywords_exclude])]

            ou_ids = [ou.id for ou in ous]
            ou_children_ids = [child.id for child in ous_children]
            if any([ou.children for ou in ous]):
                screen_visit = session.query(Service.name, func.sum(Service.visits).label('visits')).join(OU, Service.ou_id == OU.id).filter(OU.id.in_(ou_children_ids)).filter(Service.week == week).filter(Service.type == "Skærmbesøg").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
                visit = session.query(Service.name, func.sum(Service.visits).label('visits')).join(OU, Service.ou_id == OU.id).filter(OU.id.in_(ou_children_ids)).filter(Service.week == week).filter(Service.type == "Besøg").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
                call_visit = session.query(Service.name, func.sum(Service.visits).label('visits')).join(OU, Service.ou_id == OU.id).filter(OU.id.in_(ou_children_ids)).filter(Service.week == week).filter(Service.type == "Telefonopkald").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
            else:
                screen_visit = session.query(Service.name, func.sum(Service.visits).label('visits')).join(OU, Service.ou_id == OU.id).filter(OU.id.in_(ou_ids)).filter(Service.week == week).filter(Service.type == "Skærmbesøg").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
                visit = session.query(Service.name, func.sum(Service.visits).label('visits')).join(OU, Service.ou_id == OU.id).filter(OU.id.in_(ou_ids)).filter(Service.week == week).filter(Service.type == "Besøg").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
                call_visit = session.query(Service.name, func.sum(Service.visits).label('visits')).join(OU, Service.ou_id == OU.id).filter(OU.id.in_(ou_ids)).filter(Service.week == week).filter(Service.type == "Telefonopkald").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
        else:
            if keywords_exclude:
                ous_to_exclude = session.query(OU).filter(or_(*[func.lower(OU.nexus_name).contains(keyword.lower()) for keyword in keywords_exclude])).all()
                ou_ids_to_exclude = [ou.id for ou in ous_to_exclude]

                screen_visit = session.query(Service.name, func.sum(Service.visits).label('visits')).filter(Service.week == week).filter(Service.type == "Skærmbesøg").filter(~Service.ou_id.in_(ou_ids_to_exclude)).group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
                visit = session.query(Service.name, func.sum(Service.visits).label('visits')).filter(Service.week == week).filter(Service.type == "Besøg").filter(~Service.ou_id.in_(ou_ids_to_exclude)).group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
                call_visit = session.query(Service.name, func.sum(Service.visits).label('visits')).filter(Service.week == week).filter(Service.type == "Telefonopkald").filter(~Service.ou_id.in_(ou_ids_to_exclude)).group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()

            else:
                screen_visit = session.query(Service.name, func.sum(Service.visits).label('visits')).filter(Service.week == week).filter(Service.type == "Skærmbesøg").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
                visit = session.query(Service.name, func.sum(Service.visits).label('visits')).filter(Service.week == week).filter(Service.type == "Besøg").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()
                call_visit = session.query(Service.name, func.sum(Service.visits).label('visits')).filter(Service.week == week).filter(Service.type == "Telefonopkald").group_by(Service.name).order_by(func.sum(Service.visits).desc()).all()

    screen_visit_list = [{"name": service.name, "visits": service.visits} for service in screen_visit]
    visit_list = [{"name": service.name, "visits": service.visits} for service in visit]
    call_visit_list = [{"name": service.name, "visits": service.visits} for service in call_visit]

    return {"Besøg": visit_list, "Skærmbesøg": screen_visit_list, "Telefonopkald": call_visit_list}
# end new way #
