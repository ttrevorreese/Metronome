import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime 
import sqlite3

USER_ID = "reesespieces07" 
TOKEN = "BQC3mPPu7x9gK8Caq1HIvR6tIHHiEWs7Dt1eL2sbgQaoPYzcSA70GPFqUfTcf_5yN-Nd-BqHSGBSla9zMglQ1gaRAcktRRfbFVRdCol_ggNx5FSzOgrGMPWkl0ocmMebef5LSZJcu-fpTg2jlrlHogQoMkoj2vfG0XK4b1mQhvRZXGJamBo-7lT3SPfliCgja2NLc_GACYKlE9XhYjx7lmIepPyZfGDvZ6MqyghWZ8FeqAIQBK_BpLOdKyHvuMxZL9X9bQVeMkLcNGlQKZSme8IP1cco98V0JzdXgn0CiJtuKg78ChR3pJbW8M5aL5tHCTWYtcd10_Q6VKR95kWLQjEbkQpz-G8A" #TOKEN LINK - https://developer.spotify.com/
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

    # Extracting only the relevant bits of data from the json object      
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        artistid.append(song["track"]["album"]['artists'][0]['id'])

    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps,
        'artistid' : artistid
    }
    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp", "artistid"])
    make_db(song_df)

def make_db(song_df):
    import sqlite3
    import pandas as pd

    # Create a connection to the SQLite database
    conn = sqlite3.connect('song_history.db')

    # Write the DataFrame to an SQLite table
    song_df.to_sql('song_history', conn, if_exists='replace', index=False)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

get_songs()