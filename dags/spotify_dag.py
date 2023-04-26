import datetime as dt
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from sqlalchemy import create_engine
from airflow.utils.dates import days_ago
import time
# Import functions from other python files (scripts)
from extract import get_songs
from playlist_generator import get_seed

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

# Defining DAG with name, args, and schedule
dag = DAG(
    'spotify_recommendations',
    default_args=default_args,
    description='Spotify ETL Process and Song Recommendations',
    schedule=dt.timedelta(minutes=50),
)

# Importing and applying get_songs from extract.py
def play_history():
    print("Started ETL process.")
    df=get_songs()
    conn = BaseHook.get_connection('postgre_sql')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    df.to_sql('song_history', engine, if_exists='replace')

# Importing and applying get_seed from playlist_generator.py
def playlist_generator():
    # Let the user know the playlist is being created
    print("Creating playlist.")
    # Calling the function
    get_seed()

# Create a delay when executing the playlist
def my_task_func():
    time.sleep(300)
    print("Task executed after a 5-minute delay.")

with dag:    
    # Defining tasks
    create_table= PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgre_sql',
        # Using SQL queries to create SQL table
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

    # Calling play_history as task
    t2 = PythonOperator(
        task_id='spotify_etl',
        python_callable=play_history,
        dag=dag,
    )

    # Calling playlist_generator as task
    t3 = PythonOperator(
        task_id='playlist_generator',
        python_callable=playlist_generator,
        dag=dag
    )

    # Calling delay as task
    t4 = PythonOperator(
        task_id='delay',
        python_callable=my_task_func,
        dag=dag
    )

    # Creating flowchart
    create_table >> t2 >> t3 >> t4