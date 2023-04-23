import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime 
import sqlite3

USER_ID = "reesespieces07" 
<<<<<<< HEAD
TOKEN = "BQC9vQeypOtEkQvXOWlPWaq1y136iG3PTlURzhxaP3F-ALDGe2wnO23paN9CdlLak93gGjNFQ8T1g519A03BVDGsOvGr9nsRB50ainZzg_l5zUPqKyNOZipnQ7jYf8yizvyT4kZvTdeJ0K3swE1-BAxW_Z0xsdxes_2m9iFEBCgFb8GC6Pz-_G544cwsM4v_ses4sz7mxA7tSU86Yp6fVRXU8iSbwdqSJkGk9g6o2zWprIGhISq_XiySSJglttzDpEWP1X4q0tc7lVD1x3BbUaLNmgd-NsX3TM2mOoozY-1tNLNl3rV_c16FuWE4pJ87qE9VnAQVjJj1ZGpNZd2z9NPuUY2xZLxQ" #TOKEN LINK - https://developer.spotify.com/
=======
TOKEN = "BQC7NHaIwubN2-oPpxbK5zBMQVg5uqGE8U1TTcWIbtEA2I9lEJwGhjz4BE9vcgD3SK_oVI-n_uR3a_h9D1XoZghKw_KiJlRO-XhHPEeZ994wIh6EhmG6DldOY7Z7B1qYu5VLp-HrV_36YNAmW0nJVt9HY1Dg8cQbWkMoZFWqgjUfNZIyvtTdrrYpHrI_yQ8VrreQdZ9Efozf7FR45UYk_g-9GV4QoU-p1VMNuXzADlbW1GNxQ0Og1PicIIs1dsy1VSMCdBdSLxXUifWuDkA2mFIJLJMaWzSRjS_Pojep6-5khpK-fgR2cmw4HjncPl68NZT8AfuCeoifMfexLKmYGj5J1eXMjYny" #TOKEN LINK - https://developer.spotify.com/
>>>>>>> 061a6bf5bd1b7736764e4ccec10ed01212c79c80
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
    import sqlite3
    import pandas as pd

    # Create a connection to the SQLite database
    conn = sqlite3.connect('song_history.db')

    # Write the DataFrame to an SQLite table
    Transformed_df.to_sql('song_history', conn, if_exists='replace', index=False)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

get_songs()