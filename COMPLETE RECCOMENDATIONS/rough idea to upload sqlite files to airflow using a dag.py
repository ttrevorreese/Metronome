from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import sqlite3

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 18),
    'retries': 1,
}

dag = DAG(
    'upload_sqlite_to_s3',
    default_args=default_args,
    description='Upload SQLite file to S3',
    schedule_interval='@once',
)

def upload_sqlite_to_s3():
    # Get the connection details for the S3 bucket
    s3_conn_id = 's3_conn_id'
    s3_bucket = 'my-bucket-name'
    s3_prefix = 'my-folder'

    # Get the file path and database name for the SQLite file
    db_path = '/path/to/sqlite/file.db'
    db_name = 'file.db'

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Create a cursor to execute SQL commands
    c = conn.cursor()

    # Export the SQLite database to a file-like object using the SQLite shell command
    shell_command = f".output | gzip > /dev/stdout | base64 -w 0 {db_name}"
    sqlite_shell = c.shell()
    sqlite_shell.execute(shell_command)
    sql_output = sqlite_shell.fetchone()[0]

    # Connect to the S3 bucket using the S3Hook
    hook = S3Hook(s3_conn_id)
    hook.load_bytes(
        bytes_data=sql_output,
        key=f'{s3_prefix}/{db_name}.gz.b64',
        bucket_name=s3_bucket,
        replace=True
    )

    # Close the database connection
    conn.close()

upload_task = PythonOperator(
    task_id='upload_sqlite_to_s3',
    python_callable=upload_sqlite_to_s3,
    dag=dag,
)

upload_task



def description():
  """
  
  
  This code defines an Airflow DAG named upload_sqlite_to_s3, with a single task named upload_sqlite_to_s3. The task calls a Python function with the same name, which performs the following steps:

  1. Gets the connection details for the S3 bucket using the s3_conn_id, s3_bucket, and s3_prefix variables.
  
  2. Gets the file path and database name for the SQLite file using the db_path and db_name variables.
  
  3. Connects to the SQLite database using the sqlite3 module.
  
  4. Creates a cursor to execute SQL commands on the database.
  
  5. Exports the SQLite database to a file-like object using the SQLite shell command. The | gzip > /dev/stdout | base64 -w 0 part of the command gzips the output, sends it to stdout, and base64-encodes it. This makes it easier to upload to S3 as a single file.
  
  6. Connects to the S3 bucket using the S3Hook and uploads the file-like object to S3 using the load_bytes() method.
  
  7. Closes the database connection.
  
  Note that this code assumes that you have set up a connection to S3 in Airflow with the ID s3_conn_id, and that you have specified the correct S3 bucket and folder name. Also note that the replace=True argument in the load_bytes() method specifies that the file should be overwritten if it already exists in the S3 bucket.

  """
