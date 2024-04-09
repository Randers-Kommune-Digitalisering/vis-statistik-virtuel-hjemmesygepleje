import json
import importlib
import sqlalchemy
import datetime
import threading
import pandas as pd

from sqlalchemy import UniqueConstraint, exc, inspect, text, select
from sqlalchemy.orm import Session
from io import StringIO

from models import Base, District, WeeklyStat, Service, Call
from utils.time import generate_start_and_end_datetime
from vitacomm import get_call_log_api
from config.logging import logger
from config.settings import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_DATABASE, SEED_FILE

engine = None
session = None


def get_engine():
    global engine
    if not engine:
        engine = sqlalchemy.create_engine(f'mariadb+mariadbconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}')
    return engine

def create_db():
    Base.metadata.create_all(get_engine())

def execute_sql(sql):
    try:
        with get_engine().connect() as conn:
            conn.execute(text(sql))
            conn.commit()
    except exc.SQLAlchemyError as e:
        print(e)

def extract_unique_constraints(cls):
    unique_constraints = [
        tuple(attr.name for attr in constraint.columns)
        for constraint in cls.__table__.constraints 
        if isinstance(constraint, UniqueConstraint)
    ]
    return list(sum(unique_constraints, ()))

def generate_sql_add_or_update(object_list, include_primary_key = False):
    allowed_models = [District, WeeklyStat, Service, Call]
    cls = type(object_list[0])

    if cls not in allowed_models:
        raise TypeError(f'Type: "{cls.__name__}" is not allowed')
    
    if len(set(map(type, object_list))) == 1:        
        keys = []
        mapper = inspect(cls)
        table = cls.__table__

        if include_primary_key:
            keys = [ c.key for c in mapper.columns]
        else:
            keys = [ c.key for c in mapper.columns if c.key != mapper.primary_key[0].name ]

        keys.sort()

        keys_to_update = [k for k in keys if k not in extract_unique_constraints(cls)]
        keys_to_update.sort()

        def filter_keys(pair):
            key, _ = pair
            if key in  keys:
                return True
            else:
                return False
            
        rows = []
        
        for obj in object_list:
            row = list(zip(*sorted(dict(filter(lambda pair: True if pair[0] in keys else False, obj.__dict__.items())).items())))[1]
            rows.append(str(row))

        if len(keys_to_update) > 0:
            sql = f'INSERT INTO {table} (' + ','.join(keys) +') VALUES\n'
            sql += ','.join(rows)
            sql += '\nON DUPLICATE KEY UPDATE\n'
            sql += ','.join(map(lambda k: f'{k}=VALUES({k})', keys_to_update))
            return sql
        else:          
            sql = f'INSERT IGNORE INTO {table} (' + ','.join(keys) +') VALUES\n'
            sql += ','.join(rows)
            return sql
    else:
       raise TypeError('Not all objects are the same type')
    
def seed_db():
    with Session(get_engine()) as session:
        if not session.query(WeeklyStat).first() and not session.query(Service).first() and not session.query(Call).first():
            logger.info('Database empty - seeding')
            with open(SEED_FILE, 'r', encoding='utf') as jf:
                for c in json.load(jf):
                    target_module, target_class = c['target_class'].split(':')
                    cls = getattr(importlib.import_module(target_module), target_class)
                    new_objs = [cls(**obj) for obj in c['data']]
                    add_or_update_multiple(new_objs)
        else:
            logger.info('Database not empty - not seeding')

def add_or_update_multiple(object_list):
    execute_sql(generate_sql_add_or_update(object_list))

def pandas_insert_ignore(dataframe, table=None):
    if not isinstance(dataframe, pd.DataFrame):
        raise Exception('Dataframe missing')
    elif table not in inspect(get_engine()).get_table_names():
        raise Exception(f'Unknown table {table}')
        
    for i in range(len(dataframe)):
        try:
            dataframe.iloc[i:i+1].to_sql(name=table, con=get_engine(), if_exists='append', index=False)
        except exc.IntegrityError:
            pass
    
def get_districts(amount=None):
    with Session(get_engine()) as sess:
        if amount:
            query = select(District).limit(amount)
        else:
            query = select(District)
    
        return sess.scalars(query).all()
    

def get_weekly_stats_dataframe_by_week(week):
    if not isinstance(week, str):
        raise Exception('No week string')

    query = f"SELECT * FROM weekly_stat WHERE week = '{week}'"
    df = pd.read_sql(query, get_engine().connect())

    if df.empty:
        return None

    with Session(get_engine()) as sess:
        districts = sess.scalars(select(District)).all()
        df['district_id'] = df['district_id'].apply( lambda value: next(d for d in districts if d.id == value).nexus_district)
        df.rename(columns={'district_id':'district'}, inplace=True)

    df = df.sort_values('district')
    df = df.drop(columns=['week', 'id'])
    df = df.set_index('district')
    df.loc['Randers Kommune'] = df.sum(numeric_only=True)
    
    return df

def get_services_dataframes():
    query = f"SELECT * FROM service"
    df = pd.read_sql(query, get_engine().connect())
    
    with Session(get_engine()) as sess:
        districts = sess.scalars(select(District)).all()
        df['district_id'] = df['district_id'].apply( lambda value: next(d for d in districts if d.id == value).nexus_district)
        df.rename(columns={'district_id':'district'}, inplace=True)
    
    screen = df.loc[df['screen'] == 1]

    non_screen = df.loc[df['screen'] == 0]

    return screen, non_screen

def get_calls(days=30, start=None, end=None):
    start_datetime, end_datetime = generate_start_and_end_datetime(days, start, end)
    query = f"SELECT * FROM `call` WHERE NOT (start_time > '{end_datetime.replace(tzinfo=None)}' OR end_time < '{start_datetime.replace(tzinfo=None)}')"
    df = pd.read_sql(query, get_engine().connect())

    if len(df) < 2:
        df = update_call_db(days, start, end)
    else:
        newest = df['end_time'].max()
        oldest = df['start_time'].min()
        
        if end_datetime.replace(tzinfo=None) > datetime.datetime.now():
            end_datetime = datetime.datetime.now()
        
        if (newest + datetime.timedelta(hours=3)) < end_datetime.replace(tzinfo=None) or (oldest - datetime.timedelta(hours=3)) > start_datetime.replace(tzinfo=None):
            df = update_call_db(days, start, end)

    with Session(get_engine()) as sess:
        districts = sess.scalars(select(District)).all()
        df['callee_district_id'] = df['callee_district_id'].apply( lambda value: next(d for d in districts if d.id == value).nexus_district)
        df['caller_district_id'] = df['caller_district_id'].apply( lambda value: next(d for d in districts if d.id == value).nexus_district)
        df.rename(columns={'callee_district_id':'callee_district'}, inplace=True)
        df.rename(columns={'caller_district_id':'caller_district'}, inplace=True)

    return df

def update_call_db(days, start, end):
    call_log = get_call_log_api(days, start, end)
    data = StringIO(call_log)
    df = pd.read_csv(data, sep=';')
    
    df.dropna(how='all', inplace=True)
    df.dropna(how='all', axis=1, inplace=True)
    
    df = df.drop(columns=['CallerAlias', 'Media info'])
    df.columns = [c.lower().replace(' ', '_').replace("'s",'') for c in list(df)]
    
    with Session(get_engine()) as sess:
        districts = sess.scalars(select(District)).all()

        for col, dt in df.dtypes.items():
            if dt == object:
                df[col] = df[col].apply(lambda x : x[2:].strip() if x.startswith("1:") else x)
                
            if 'time' in col:
                df[col] = pd.to_datetime(df[col], utc=True)
            elif dt == 'int64' and 'seconds' in col:
                df[col] = pd.to_timedelta(df[col], unit='s')
                df[col] = df[col].astype(str).apply(lambda x : x.split(' ')[-1])
                df.rename({col: col.split('_')[0]}, axis=1, inplace=True)
            elif 'cpr' in col:
                df[col] = df[col].fillna('0000000000')
                df[col.split('_')[0]] = df[col.split('_')[0]].astype(str) + ';' + df[col].astype(str)
                df.drop([col], axis=1, inplace=True)
            elif 'role' in col:
                df[col] = df[col].map({'Employee': True, 'Resident': False})
                df.rename({col: col.replace('role', 'employee')}, axis=1, inplace=True)
            elif 'ou' in col:
                df[col] = df[col].apply( lambda value: next(d for d in districts if d.vitacomm_district == value.strip()).id)
                df.rename({col: col.replace('ou', 'district_id')}, axis=1, inplace=True)
            elif 'id' in col:
                df.rename({col: 'id'}, axis=1, inplace=True)

        df_to_save = df.copy(deep=True)       
        thread = threading.Thread(target=pandas_insert_ignore, args=(df_to_save, Call.__tablename__))
        thread.start()

        return df

"""
def get_services_dataframes_by_week(week):
    return None

def get_services(amount=None, top=True, screen=None, district_id=None, week=None):
    if district_id and week:
        filters = (Service.screen == screen, Service.district_id == district_id, Service.week == week)
    elif district_id:
        filters = (Service.screen == screen, Service.district_id == district_id)
    elif week:
        filters = (Service.screen == screen, Service.week == week)
    elif screen:
        filters = (Service.screen == screen,)
    else:
        filters = ()
    
    with Session(get_engine()) as sess:
        if top and amount:
            query = select(Service).filter(*filters).order_by(Service.visits.desc()).limit(amount)
        elif amount:
            query = select(Service).filter(*filters).order_by(Service.visits.asc()).limit(amount)
        elif top:
            query = select(Service).filter(*filters).order_by(Service.visits.desc())
        else:
            query = select(Service).filter(*filters).order_by(Service.visits.asc())
        
        return sess.scalars(query).all()
    
def get_weekly_stats(amount=None, top=True, order_by='citizens', district_id=None, week=None):
    if district_id and week:
        filters = (WeeklyStat.district_id == district_id, WeeklyStat.week == week)
    elif district_id:
        filters = (WeeklyStat.district_id == district_id,)
    elif week:
        filters = (WeeklyStat.week == week,)
    else:
        filters = ()
    
    with Session(get_engine()) as sess:
        if top and amount:
            query = select(WeeklyStat).filter(*filters).order_by(text(f'{order_by} desc')).limit(amount)
        elif amount:
            query = select(WeeklyStat).filter(*filters).order_by(text(f'{order_by} asc')).limit(amount)
        elif top:
            query = select(WeeklyStat).filter(*filters).order_by(text(f'{order_by} desc'))
        else:
            query = select(WeeklyStat).filter(*filters).order_by(text(f'{order_by} asc'))
        
        return sess.scalars(query).all()
"""