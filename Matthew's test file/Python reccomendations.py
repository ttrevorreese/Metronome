import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3
from tabulate import tabulate

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER_ID = "reesespieces07" # your Spotify username 
TOKEN = "BQBjgqUK1zcXifI1-nNM9YL_YeRnN8bEj72SSqk-G69sG136p0PfIp4iSrFT1bRs9TNGyaafxTJVrhtGfLlZSRqT1e5HDghoff1jwE61ZAs6WywFnLDH4MINrB11a033Wyuq7gFWOv8QclxEVYAdzgGO7l7qrZuXwiLhw-trNXzzbIFy1xKU1l6r6VDag9DCiA9kLC8fKl11MtpXiuyLN7qFjVuFeJWiUPEAl-ltfjM39WqBcOohzBAZDaTTU8SUSD0CRtKDFcf_GTHVKFzkMuQbXfbx7nf5T4RRrBYlmDrswpobd3Nmwp7Y7SPed_t4j2K4WtRlThQ2-p2V0R_lAD3Ig-n-Kielhk7V61GliD1HmYk" # your Spotify API token

# Generate your token here:  https://developer.spotify.com/console/get-recently-played/
# Note: You need a Spotify account (can be easily created for free)


if __name__ == "__main__":

    # Extract part of the ETL process
 
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
    
    # Convert time to Unix timestamp in miliseconds      
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=15)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix_timestamp), headers = headers)

    data = r.json()


    limit=50
    market="GB"
    seed_genres="hip-hop"
    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    target_danceability=0.9
    r = requests.get("{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}".format(endpoint_url = endpoint_url,limit=limit, market = market, seed_genres =seed_genres, target_danceability= target_danceability), headers = headers)

    recc = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

   # print(recc)
    for i in recc['tracks']:
       
        song_names.append(i['name'])
        artist_names.append(i['artists'][0]['name'])

    
   
        
    # # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        
    }

    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name"])
    
   

    print(tabulate(song_df, headers='keys', tablefmt='psql'))
