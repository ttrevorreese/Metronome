import pandas as pd 
import requests
from datetime import datetime
import datetime
import pandas as pd 
import requests
from datetime import datetime
import datetime

USER_ID = "reesespieces07" 
TOKEN = "BQDpd_HeqC6Aa41pQCB_QB9SReweqlfC4kVjgecmNdpb0TH6ujdmcbohjkvkInJ5wBj6pVgq2VdHbFG_k9kxuw35EaJI5aOjhgt4dyMV735XH7w5-6fY7JX1JnCJs0cTq1i30OE6TTSMVCMSloK9H06USO53ueIo9VPnYw58Rn-m7Tf6z1Ic0vZ-x1N4Tg4ZyAoQce7Wc4RIBhf2Ek2eAqhlrwEKgM4m7B5MJ41-xW0Eshy5Y3xs11nYVUL_ZJ2p_cJ5qhOQhWuYNwVS9gyFdhNUXPNKaJ1I9Hb2kij8ianU0NewCYg_gN9DmADSYnTSvIVZJNAFx7tLFM8MhB-IYmsculOBKX3B"
print('started')
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

def Data_Quality(load_df):
    #Checking Whether the DataFrame is empty
    if load_df.empty:
        print('No Songs Extracted')
        return False
    
    #Enforcing Primary keys since we don't need duplicates
    if pd.Series(load_df['played_at']).is_unique:
       pass
    else:
        #The Reason for using exception is to immediately terminate the program and avoid further processing
        raise Exception("Primary Key Exception,Data Might Contain duplicates")
    
    #Checking for Nulls in our data frame 
    if load_df.isnull().values.any():
        raise Exception("Null values found")

# Writing some Transformation Queries to get the count of artist
def Transform_df(load_df):

    #Applying transformation logic
    Transformed_df=load_df.groupby(['timestamp','artist_name'],as_index = False).count()
    Transformed_df.rename(columns ={'played_at':'count'}, inplace=True)
    #Creating a Primary Key based on Timestamp and artist name
    Transformed_df["ID"] = Transformed_df['timestamp'].astype(str) +"-"+ Transformed_df["artist_name"]

    return Transformed_df[['ID','timestamp','artist_name','count']]

def spotify_etl():
    #Importing the songs_df from the Extract.py
    load_df=return_dataframe()
    Data_Quality(load_df)
    #calling the transformation
    Transformed_df=Transform_df(load_df)    
    print(load_df)
    return (load_df)

spotify_etl()

