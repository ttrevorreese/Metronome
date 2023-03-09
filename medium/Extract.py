import pandas as pd 
import requests
from datetime import datetime
import datetime


USER_ID = "YOUR_USER_ID" 
TOKEN = "BQCYlJMwalTfuiKswEXtcKtQrN70_LEx6vmsC3qwmXAQQkeCUVIbE42MBZ13ALSfWkLYx-Rwu9Ks27y5eZwX4xri7Zx9_ZLfYKxAZI_KBypi0ZCKXG7PGY4_ta3Qg1A6A2cU4Qk-WkdqpurdKZxkqpqvD6oI_XVxCa4pNu0Hg27419zEAW3IZ7s5RRQlGqpD9ISzRAry3g"


# Creating an function to be used in other python files
def return_dataframe(): 
    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
     
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix_timestamp), headers = input_variables)

    data = r.json()
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Extracting only the relevant bits of data from the json object      
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        
    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }
    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])
    return song_df
