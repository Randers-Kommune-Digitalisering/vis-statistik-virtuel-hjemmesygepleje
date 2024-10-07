import warnings
import io
import pandas as pd
import functools as ft

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import OU, Service, WeeklyStat
from database import get_engine, add_or_update_multiple
from sftp import list_all_files
from config.settings import SFTP_PATH

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def read_bi_data():
    file_list, sftp_conn = list_all_files()

    with Session(get_engine()) as sess:
        for f in file_list:
            if f[:4] == 'vhsp' and f[-4:] == 'xlsx':

                file_path = SFTP_PATH + '/' + f
                file = sftp_conn.open(file_path)
                xls = pd.ExcelFile(io.BytesIO(file.read()))
                week = pd.read_excel(xls, 'ugenr').iloc[0,0]

                service_dfs = []
                week_stats_df = []

                for s in xls.sheet_names:
                    
                    if 'ydelser' in s:
                        districts = sess.scalars(select(OU)).all()
                        df = pd.read_excel(xls, s)

                        df.dropna(how='all', inplace=True)
                        df.dropna(how='all', axis=1, inplace=True)
                        
                        id_vars = []
                        for col_name in df.columns:
                            if df.columns.get_loc(col_name) > 0:
                                df[col_name] = df[col_name].fillna(0).astype(int)
                            else:
                                id_vars.append(col_name)
                        
                        value_vars = df.columns.difference(id_vars)
                        df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='name', value_name='visits')
                        df.rename(columns={id_vars[0]: 'district_id'}, inplace=True)
                        df['week'] = week
                        if 'skærm' in s:
                            df['screen'] = True
                        else:
                            df['screen'] = False

                        df['district_id'] = df['district_id'].apply( lambda value: next(d for d in districts if d.nexus_name == value).id)

                        service_dfs.append(df)

                    if 'planlagt' in s:
                        districts = sess.scalars(select(OU)).all()
                        df = pd.read_excel(xls, s)

                        df.dropna(how='all', inplace=True)
                        df.dropna(how='all', axis=1, inplace=True)

                        id_vars = []
                        for col_name in df.columns:
                            id_vars.append(col_name)
                            if df.columns.get_loc(col_name) > 2:
                                df[col_name] = df[col_name].fillna(0).astype(int)

                        df.drop(id_vars[1], axis=1, inplace=True)
                        df.rename(columns={id_vars[0]: 'district_id'}, inplace=True)

                        names = ['planned_hours', 'citizens_with_planned_visits', 'planned_visits']
                        if 'skærm' in s:
                            names = ['screen_' + n for n in names]
                        
                        df.rename(columns={id_vars[2]: names[0]}, inplace=True)
                        df.rename(columns={id_vars[3]: names[1]}, inplace=True)
                        df.rename(columns={id_vars[4]: names[2]}, inplace=True)

                        df[names[0]] = df[names[0]].apply( lambda value: round(value,2) )
                        df['district_id'] = df['district_id'].apply( lambda value: next(d for d in districts if d.nexus_name == value).id )

                        week_stats_df.append(df)
                        
                    if 'borgere' in s:
                        districts = sess.scalars(select(OU)).all()
                        df = pd.read_excel(xls, s)

                        df.dropna(how='all', inplace=True)
                        df.dropna(how='all', axis=1, inplace=True)

                        df.rename(columns={df.columns[0]: 'district_id'}, inplace=True)
                        df.rename(columns={df.columns[1]: 'citizens'}, inplace=True)
                        df['district_id'] = df['district_id'].apply( lambda value: next(d for d in districts if d.nexus_name == value).id )
                        
                        week_stats_df.append(df)

                week_stats_df = ft.reduce(lambda left, right: pd.merge(left, right, on='district_id'), week_stats_df)
                week_stats_df['week'] = week

                week_stats = []

                for _, row in week_stats_df.iterrows():
                    week_stats.append(WeeklyStat(**row))

                add_or_update_multiple(week_stats)

                service_df = pd.concat(service_dfs)

                services = []

                for _, row in service_df.iterrows():
                    services.append(Service(**row))

                add_or_update_multiple(services)