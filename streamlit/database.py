import json
import importlib
import sqlalchemy
import datetime
import re
import urllib.parse
import pandas as pd

from sqlalchemy import UniqueConstraint, exc, inspect, text, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from io import StringIO

from models import Base, OU, WeeklyStat, Service, Call
from vitacomm import get_call_log_api
from utils.time import generate_start_and_end_datetime, get_last_week, get_fortnight_start_and_end, get_weeks
from config.logging import logger
from config.settings import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_DATABASE, SEED_FILE


def get_engine():
    return sqlalchemy.create_engine(f'postgresql+psycopg2://{urllib.parse.quote_plus(DB_USER)}:{urllib.parse.quote_plus(DB_PASS)}@{urllib.parse.quote_plus(DB_HOST)}:{urllib.parse.quote_plus(DB_PORT)}/{urllib.parse.quote_plus(DB_DATABASE)}')


def create_db(): 
    Base.metadata.create_all(get_engine())


def execute_sql(sql):
    with get_engine().connect() as conn:
        res = conn.execute(text(sql))
        conn.commit()
        return res


def extract_unique_constraints(cls):
    unique_constraints = [
        tuple(attr.name for attr in constraint.columns)
        for constraint in cls.__table__.constraints 
        if isinstance(constraint, UniqueConstraint)
    ]
    return list(sum(unique_constraints, ()))


def generate_sql_add_or_update(object_list, include_primary_key=False):
    allowed_models = [OU, WeeklyStat, Service, Call]
    cls = type(object_list[0])

    if cls not in allowed_models:
        raise TypeError(f'Type: "{cls.__name__}" is not allowed')

    if len(set(map(type, object_list))) == 1:        
        keys = []
        mapper = inspect(cls)
        table = cls.__table__

        if include_primary_key:
            keys = [c.key for c in mapper.columns]
        else:
            keys = [c.key for c in mapper.columns if c.key != mapper.primary_key[0].name]

        keys.sort()

        keys_to_update = [k for k in keys if k not in extract_unique_constraints(cls)]
        keys_to_update.sort()

        def filter_keys(pair):
            key, _ = pair
            if key in keys:
                return True
            else:
                return False
            
        rows = []
        
        for obj in object_list:
            row = list(zip(*sorted(dict(filter(lambda pair: True if pair[0] in keys else False, obj.__dict__.items())).items())))[1]
            rows.append(str(row))

        if len(keys_to_update) > 0:
            sql = f'INSERT INTO {table} (' + ','.join(keys) + ') VALUES\n'
            sql += ','.join(rows)
            sql += '\nON DUPLICATE KEY UPDATE\n'
            sql += ','.join(map(lambda k: f'{k}=VALUES({k})', keys_to_update))
            return sql
        else:          
            sql = f'INSERT IGNORE INTO {table} (' + ','.join(keys) + ') VALUES\n'
            sql += ','.join(rows)
            return sql
    else:
        raise TypeError('Not all objects are the same type')


def generate_sql_add_or_ignore(object_list):
    allowed_models = [OU, WeeklyStat, Service, Call]
    cls = type(object_list[0])

    if cls not in allowed_models:
        raise TypeError(f'Type: "{cls.__name__}" is not allowed')

    if len(set(map(type, object_list))) == 1:        
        mapper = inspect(cls)
        table = cls.__table__

        keys = [c.key for c in mapper.columns]
        keys.sort()

        rows = []

        for obj in object_list:
            row = list(zip(*sorted(dict(filter(lambda pair: True if pair[0] in keys else False, obj.__dict__.items())).items())))[1]
            rows.append(str(row))

        sql = f'INSERT IGNORE INTO {table} (' + ','.join(keys) + ') VALUES\n'
        sql += ','.join(rows)
        return sql
    else:
        raise TypeError('Not all objects are the same type')


# def seed_db():
#     with open(SEED_FILE, 'r', encoding='utf') as jf:
#         for c in json.load(jf):
#             target_module, target_class = c['target_class'].split(':')
#             cls = getattr(importlib.import_module(target_module), target_class)
#             new_objs = [cls(**obj) for obj in c['data']]
#             add_or_update_multiple(new_objs)

#             date = datetime.datetime(year=2023, month=5, day=1, hour=0, minute=0, second=0)
#             end_date = datetime.datetime.now()

#             while date < end_date:
#                 update_call_db(days=29, start=date)
#                 date = date + datetime.timedelta(days=29)

def seed_call_logs():

    date = datetime.datetime(year=2023, month=5, day=1, hour=0, minute=0, second=0)
    end_date = datetime.datetime.now()

    while date < end_date:
        update_call_db(days=29, start=date)
        date = date + datetime.timedelta(days=29)


from sqlalchemy import update

def seed_db():
    with Session(get_engine()) as session:

        with open(SEED_FILE, 'r', encoding='utf') as jf:
            data = json.load(jf)
            mappings = {}

            for entry in data:
                target_module, target_class = entry['target_class'].split(':')
                cls = getattr(importlib.import_module(target_module), target_class)
                mappings[target_class] = {}
                for obj_data in entry['data']:
                    # Special handling for OU objects
                    if target_class == 'OU':
                        parent_name = obj_data.pop('parent', None)
                        ou = cls(**obj_data)
                        nexus_name = obj_data.get('nexus_name', '') or ''
                        vitacomm_name = obj_data.get('vitacomm_name', '') or ''

                        try:
                            stmt = insert(cls).values(obj_data).on_conflict_do_update(
                                constraint='unique_ou',
                                set_={column.name: getattr(ou, column.name) for column in cls.__table__.columns if column.name != 'id'}
                            ).returning(cls)
                            res = session.execute(stmt)
                        except exc.IntegrityError as e:
                            session.rollback()

                            if "unique_nexus" in str(e.orig):
                                updated_stmt = (
                                    update(OU).
                                    where(OU.nexus_name == obj_data['nexus_name'], OU.vitacomm_name.is_(None)).
                                    values({column.name: getattr(ou, column.name) for column in cls.__table__.columns if column.name not in ['id', 'nexus_name']}).
                                    returning(OU)
                                )
                                res = session.execute(updated_stmt)

                            elif "unique_vitacomm" in str(e.orig):
                                updated_stmt = (
                                    update(OU).
                                    where(OU.nexus_name == obj_data['nexus_name'], OU.applikator_id.is_(None)).
                                    values({column.name: getattr(ou, column.name) for column in cls.__table__.columns if column.name not in ['id', 'vitacomm_name']}).
                                    returning(OU)
                                )
                                res = session.execute(updated_stmt)

                            else:
                                raise e

                        ou = res.fetchone()[0]
                        mappings[target_class][nexus_name + vitacomm_name] = (ou, parent_name)
                        session.commit()
                    else:
                        try:
                            session.add(cls(**obj_data))
                            session.commit()
                        except exc.IntegrityError:
                            session.rollback()

            for target_class in mappings:
                # Special handling for OU objects
                if target_class == 'OU':
                    for ou, parent_name in mappings[target_class].values():
                        if parent_name:
                            parent_ou = mappings[target_class].get(parent_name, (None,))[0]
                            if parent_ou:
                                ou.parent_id = parent_ou.id
            session.commit()


def add_or_update_multiple(object_list):
    execute_sql(generate_sql_add_or_update(object_list))


def add_or_ignore_multiple(object_list):
    execute_sql(generate_sql_add_or_ignore(object_list))


def get_districts(amount=None):
    with Session(get_engine()) as sess:
        if amount:
            query = select(OU).limit(amount)
        else:
            query = select(OU)

        return sess.scalars(query).all()


def get_weekly_stats_dataframe_by_week(week):
    if not isinstance(week, str):
        raise Exception('No week string')

    with get_engine().connect() as conn:
        query = f"SELECT * FROM weekly_stat WHERE week = '{week}'"
        df = pd.read_sql(query, conn)

        if df.empty:
            return None

        districts = Session(conn).scalars(select(OU)).all()
        df['district_id'] = df['district_id'].apply(lambda value: next(d for d in districts if d.id == value).nexus_name)
        df.rename(columns={'district_id': 'district'}, inplace=True)

    df = df.sort_values('district')
    df = df.drop(columns=['week', 'id'])
    df = df.set_index('district')
    df.loc['Randers Kommune'] = df.sum(numeric_only=True)

    return df


def get_services_dataframes():
    with get_engine().connect() as conn:
        query = f"SELECT * FROM service"
        df = pd.read_sql(query, conn)

        districts = Session(conn).scalars(select(OU)).all()
        df['district_id'] = df['district_id'].apply( lambda value: next(d for d in districts if d.id == value).nexus_name)
        df.rename(columns={'district_id':'district'}, inplace=True)

        screen = df.loc[df['screen'] == 1]
        non_screen = df.loc[df['screen'] == 0]

        return screen, non_screen


def get_calls(days=30, start=None, end=None):
    with get_engine().connect() as conn:
        start_datetime, end_datetime = generate_start_and_end_datetime(days, start, end)
        query = f"SELECT * FROM `{Call.__tablename__}` WHERE NOT (start_time > '{end_datetime.replace(tzinfo=None)}' OR end_time < '{start_datetime.replace(tzinfo=None)}')"
        query = f"""
            SELECT * FROM "{Call.__tablename__}" 
            WHERE NOT (start_time > '{end_datetime.replace(tzinfo=None)}' OR end_time < '{start_datetime.replace(tzinfo=None)}')
        """
        df = pd.read_sql(query, conn)

        if len(df) < 2:
            df = update_call_db(days, start, end)
        else:
            newest = df['end_time'].max()
            oldest = df['start_time'].min()

            if end_datetime.replace(tzinfo=None) > datetime.datetime.now():
                end_datetime = datetime.datetime.now()

            if (newest + datetime.timedelta(hours=3)) < end_datetime.replace(tzinfo=None) or (oldest - datetime.timedelta(hours=3)) > start_datetime.replace(tzinfo=None):
                df = update_call_db(days, start, end)

            # districts = Session(conn).scalars(select(District)).all()
            # df['callee_district_id'] = df['callee_district_id'].apply( lambda value: next(d for d in districts if d.id == value).nexus_district)
            # df['caller_district_id'] = df['caller_district_id'].apply( lambda value: next(d for d in districts if d.id == value).nexus_district)
            # df.rename(columns={'callee_district_id':'callee_district'}, inplace=True)
            # df.rename(columns={'caller_district_id':'caller_district'}, inplace=True)

        df['duration'] = pd.to_timedelta(df['duration'])
        return df


def get_citizens(weeks=None):
    if weeks:
        weeks = ",".join("'{}'".format(i) for i in weeks)
    with get_engine().connect() as conn:
        query = f"SELECT citizens, district_id, week FROM {WeeklyStat.__tablename__}"
        if weeks:
            query = query + f" WHERE week in ({weeks})"

        df = pd.read_sql(query, conn)

        if df.empty:
            return None

        districts = Session(conn).scalars(select(OU)).all()
        df['district_id'] = df['district_id'].apply( lambda value: next(d for d in districts if d.id == value).nexus_name)
        df.rename(columns={'district_id':'district'}, inplace=True)

        return df


def get_call_citizens(weeks, district=None, callee_district=True):
    result = []

    with get_engine().connect() as conn:
        if district:
            district_id = Session(conn).scalars(select(OU).where(OU.nexus_name == district)).first().id
        for week in weeks:
            start, end = get_fortnight_start_and_end(week)
            query = f"""
                SELECT COUNT(DISTINCT callee)
                FROM {Call.__tablename__} 
                WHERE 
                    (callee_role = 'Resident' AND caller_role = 'Employee')
                    AND NOT (duration = 0)
                    AND NOT (start_time < '{start}' OR end_time > '{end}')
            """
            if district:
                if callee_district:
                    query = query + f"AND (callee_ou_id = {district_id})"
                else:
                    query = query + f"AND (caller_ou_id = {district_id})"
            result.append((Session(conn).execute(text(query)).first()[0],) + (week,))

    df = pd.DataFrame(result, columns=['screen', 'week'])
    df['district'] = district if district else 'Randers kommune'
    return df

# def get_services_dataframes_by_week(week):
#     return None

# def get_services(amount=None, top=True, screen=None, district_id=None, week=None):
#     if district_id and week:
#         filters = (Service.screen == screen, Service.district_id == district_id, Service.week == week)
#     elif district_id:
#         filters = (Service.screen == screen, Service.district_id == district_id)
#     elif week:
#         filters = (Service.screen == screen, Service.week == week)
#     elif screen:
#         filters = (Service.screen == screen,)
#     else:
#         filters = ()
    
#     with Session(get_engine()) as sess:
#         if top and amount:
#             query = select(Service).filter(*filters).order_by(Service.visits.desc()).limit(amount)
#         elif amount:
#             query = select(Service).filter(*filters).order_by(Service.visits.asc()).limit(amount)
#         elif top:
#             query = select(Service).filter(*filters).order_by(Service.visits.desc())
#         else:
#             query = select(Service).filter(*filters).order_by(Service.visits.asc())
        
#         return sess.scalars(query).all()
    
# def get_weekly_stats(amount=None, top=True, order_by='citizens', district_id=None, week=None):
#     if district_id and week:
#         filters = (WeeklyStat.district_id == district_id, WeeklyStat.week == week)
#     elif district_id:
#         filters = (WeeklyStat.district_id == district_id,)
#     elif week:
#         filters = (WeeklyStat.week == week,)
#     else:
#         filters = ()
    
#     with Session(get_engine()) as sess:
#         if top and amount:
#             query = select(WeeklyStat).filter(*filters).order_by(text(f'{order_by} desc')).limit(amount)
#         elif amount:
#             query = select(WeeklyStat).filter(*filters).order_by(text(f'{order_by} asc')).limit(amount)
#         elif top:
#             query = select(WeeklyStat).filter(*filters).order_by(text(f'{order_by} desc'))
#         else:
#             query = select(WeeklyStat).filter(*filters).order_by(text(f'{order_by} asc'))

#         return sess.scalars(query).all()


def update_call_db(days, start=None, end=None):
    call_log = get_call_log_api(days, start, end)

    data = StringIO(call_log)

    df = pd.read_csv(data, sep=';', dtype={"Caller's CPR": str, "Callee's CPR": str})

    df = df.drop(columns=['CallerAlias', 'Media info'])    

    df.dropna(how='all', inplace=True)
    df.dropna(how='all', axis=1, inplace=True)

    df.columns = [re.sub(r"'s|\(|\)", "", c.lower().replace(' ', '_')) for c in list(df)]

    with Session(get_engine()) as sess:
        districts = sess.scalars(select(OU)).all()

        for col, dt in df.dtypes.items():
            if dt == object and 'cpr' not in col:
                df[col] = df[col].apply(lambda x: x[2:].strip() if x.startswith("1:") else x)

            if dt == 'int64' and 'seconds' in col:
                df[col] = pd.to_timedelta(df[col], unit='s')
                df[col] = df[col].astype(str).apply(lambda x: x.split(' ')[-1])
                df.rename({col: col.split('_')[0]}, axis=1, inplace=True)
            elif 'cpr' in col:
                df[col] = df[col].fillna('0000000000')
                # df[col.split('_')[0]] = df[col.split('_')[0]].astype(str) + ';' + df[col].astype(str)
                # df.drop([col], axis=1, inplace=True)
            # elif 'role' in col:
            #     df[col] = df[col].map({'Employee': True, 'Resident': False})
            #     df.rename({col: col.replace('role', 'employee')}, axis=1, inplace=True)
            elif 'ou' in col:
                # Set ou_id based on vitacomm name and drop rows with unknown ou
                df[col] = df[col].apply(lambda value: next((d.id for d in districts if d.vitacomm_name == value.strip()), None))
                df.dropna(subset=[col], inplace=True)
                df.rename({col: col.replace('ou', 'ou_id')}, axis=1, inplace=True)
            elif 'id' in col:
                df.rename({col: 'id'}, axis=1, inplace=True)

        data = df.to_dict(orient='records')
        instances = [Call(**row) for row in data]

        # add_or_ignore_multiple(instances)
        for instance in instances:
            try:
                sess.merge(instance)
                sess.commit()
            except exc.IntegrityError:
                sess.rollback()

        return df
