import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime 
import sqlite3

DATABASE_LOCATION = "sqlite://my_played_tracks.sqlite"
USER_ID = "lowriem"

####  PRINT OF A NEW TOKEN EVERY FEW MINTUES AS THEY EXPIRE AT THE FOLLOWING URL: https://developer.spotify.com/console/get-recently-played/?limit=10&after=1596299315000&before=
TOKEN = "BQCVE69uZ-k19iFPNDg3S6z1uDaNrHZmzY7_Css4uCUplt011I3z9uPwbfrzjplBMuITR9bnqlT8Erx4uVeKZ_W0yqIATyo8g_3onXMAJ48yuGYfNCCs1sSzSp45ve9EmC0kaUDLdHYXzkZpjl1psKBo7FyQENHlUJ7KeomMSvl2kY8mAGjaB5WTVJyvLHcO-WBtkG0_nw"


def check_if_valid_data(df: pd.DataFrame) -> bool:

  if df.empty:
    print("No songs downloaded, finishing process")
    return False


  if pd.Series(df['played_at']).is_unique:
    pass
  else:
    raise Exception("Primary Key check was violated, duplicates detected")


  if df.isnull().values.any():
    raise Exception("Null value found. Terminated")


  yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
  yesterday = yesterday.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

  timestamps = df["timestamp"].tolist()
#  for timestamp in timestamps:
#    if datetime.datetime.strptime(timestamp, "%Y-%m-%d") != yesterday:
#      raise Exception("One of the values was not in the time constraint")

  return True


if __name__ == "__main__":
  headers = {
      "Accept" : "application/json",
      "Content-Type" : "application/json",
      "Authorization" : "Bearer {token}".format(token=TOKEN)
  }


  today = datetime.datetime.now()
  yesterday = today - datetime.timedelta(days=10)
  yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

  r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time = yesterday_unix_timestamp), headers = headers)

  data = r.json()

  song_names =[]
  artist_names = []
  played_at_list = []
  timestamps = []

  for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
  
  song_dict = {
      "song_name" : song_names,
      "artist_names" : artist_names,
      "played_at" : played_at_list,
      "timestamp" : timestamps
  }
  song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_names", "played_at", "timestamp"])



from tabulate import tabulate




print(tabulate(song_df, headers='keys', tablefmt='psql'))


#validate

if check_if_valid_data(song_df):
  print("Data Valid, proceed to loading stage")


#load
engine = sqlalchemy.create_engine(DATABASE_LOCATION)
conn = sqlite3.connect("my_played_traks.sqlite")
cursor = conn.cursor()

sql_query = """
CREATE TABLE IF NOT EXISTS my_played_tracks(
  song_name VARCHAR(200),
  artist_name VARCHAR(200),
  played_at VARCHAR(200),
  timestamp VARCHAR(200),
  CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
)

"""

cursor.execute(sql_query)
print("Opened database successfully")

try:
    song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
except:
    print("Data already exists in the database")

conn.close()
print("Close database successfully")
