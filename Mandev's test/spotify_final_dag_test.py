import datetime as dt
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from sqlalchemy import create_engine
from airflow.utils.dates import days_ago
# Import functions from other python files (scripts)
from recommendations import read_db
from recommendations import make_rec
from etl import get_songs

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': dt.datetime(2023,1,29),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1)
}

dag = DAG(
    'spotify_recommendations',
    default_args=default_args,
    description='Spotify ETL Process and Song Recommendations',
    schedule_interval=dt.timedelta(minutes=50),
)

def play_history():
    print("Started ETL process.")
    df=get_songs()
    conn = BaseHook.get_connection('postgre_sql')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    df.to_sql('song_history', engine, if_exists='replace')

# running read_db function in recommendations.py
def get_history():
    print("Reading play history.")
    read_db()

def recommendations():
    print("Started recommendation creation.")
    df=make_rec()
    conn = BaseHook.get_connection('postgre_sql')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    df.to_sql('recommendations', engine, if_exists='replace')

with dag:    
    create_table= PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgre_sql',
        sql="""
            CREATE TABLE IF NOT EXISTS my_played_tracks(
            song_name VARCHAR(200),
            artist_name VARCHAR(200),
            played_at VARCHAR(200),
            timestamp VARCHAR(200),
            artistid VARCHAR(200),
            songid VARCHAR(200),
            CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
        )
        """
    )

    run_etl = PythonOperator(
        task_id='spotify_etl',
        python_callable=play_history,
        dag=dag,
    )
    
    get_his = PythonOperator(
        task_id='get_history',
        python_callable=get_history,
        dag=dag,
    )

    run_rec = PythonOperator(
        task_id='recommendation_generator',
        python_callable=recommendations,
        dag=dag,
    )

    create_table >> run_etl >> get_his >> run_rec