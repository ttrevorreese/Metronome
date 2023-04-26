import pandas as pd 
import requests
from datetime import datetime
import datetime


USER_ID = "reesespieces07" 
TOKEN = "BQBXIU8q-Lqq7W6SHh_ggqQ0SHH78Q5CFPErXAnEHLF8spZ16YDtQoQVLfCT1J60yW4onoJERIL3L60rJmbzdgwM2kQmb8wOug7ffFfLXhu7z00GheRBhziB4iiJV6sVzipdexyns3MgDxgWnUz0J62JDniVWeW1G3nMaFgWk4-1pPE9Zw835r1gSkw"


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
