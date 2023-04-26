import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime 
import sqlite3
#TOKEN LINK - https://developer.spotify.com/
USER_ID = "reesespieces07" 
TOKEN = "BQCRWvjv_-trzxW02y3UaJkcf5EUFf7FANWiyJx8rI1Gw8qoS9yAWkpRd0_tKP0jq-RwAnVQRTlyhazU1sq4-aAUyxneVvjWXtHtvqT0RoA02GGWQ5UEENjzlwwSW0cBMevVziCmqOrCIYqkgJeCxfSushl8psM-aFeVfhIx0WcTQnRwfnyxwbbL_gkCRrQbEsblCh2XDGBAj_5pbNWxTQM6i-vG76Ykq3mVH_DgxLk09RZEY05jrQkDlV1GmQrdjtsLPwuyjkYWqQPCVW85LNulJYrubUxhtzqdzDoBNoMcgilqFdEraLI54Il--6DkJxXk8nLsqUKxNwsLUkX9vGfb91FEAZJT"
limit = 50

# Creating an function to be used in other python files
def get_songs():
    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
        
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=10)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit={limit}&after={time}".format(time=yesterday_unix_timestamp, limit = limit), headers = input_variables)

    data = r.json()
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []
    artistid = []
    songid = []

    # Extracting only the relevant bits of data from the json object 
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        artistid.append(song["track"]["album"]['artists'][0]['id'])
        songid.append(song["track"]["id"])

    # Prepare a dictionary in order to turn it into a pandas dataframe below
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps,
        'artistid' : artistid,
        'songid' : songid
    }
    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp", "artistid", 'songid'])
    make_db(song_df)

    #Applying transformation logic
    Transformed_df=song_df.groupby(['timestamp','artist_name'],as_index = False).count()
    Transformed_df.rename(columns ={'played_at':'count'}, inplace=True)
    #Creating a Primary Key based on Timestamp and artist name
    Transformed_df["ID"] = Transformed_df['timestamp'].astype(str) +"-"+ Transformed_df["artist_name"]

    return Transformed_df[['ID','timestamp','artist_name','count']]

def make_db(Transformed_df):
    # Create a connection to the SQLite database
    conn = sqlite3.connect('song_history.db')

    # Write the DataFrame to an SQLite table
    Transformed_df.to_sql('song_history', conn, if_exists='replace', index=False)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

get_songs()