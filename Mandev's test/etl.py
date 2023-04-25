import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime 
import sqlite3

#TOKEN LINK - https://developer.spotify.com/
USER_ID = "mandevseahra_" 
TOKEN = "BQCrRerfaKzBaaUpIdGWywP_Vmk1UyszOxiG6bkyqD-0lCXZV4sDHQMt1CvKE9Ze_orQsMQEHz9ca1B7Rv-q69LvpNBS35brrtXQNMaVUvZNqKHl0zbFgx01AFgxZjbOitRkcw4L_Tb4aGyXop1iwJAcrh5r5TnYd63wjUsGuiAo9R-iLyJRC8YbZOew4gPkpZydV96wtmRTc0qnWu-qZVTDxp2QZu24mB-uFgyTz465kpza61wKK5Yoc9Yful9JCdofQXZo_fJzheg3YTnFwJXC0c1dMOdjsk2MTHGaRQhuFfZjU6phTUNXBkSZwuEOn9KRPoX0TO5YG9LJd_DD3B2MMW0bRUs"
print('Started ETL process.')
# Creating an function to be used in other pyrhon files
def return_dataframe(): 
    input_variables = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
     
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    print('Downloading song history.')
    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix_timestamp), headers = input_variables)

    data = r.json()
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []
    artistid = []
    songid = []

    print('Extracting data.')
    # Extracting only the relevant bits of data from the json object      
    for song in data["items"]:
        artistid.append(song["track"]["artists"])
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        songid.append(song["track"]["id"])

    print('Creating dictionary.')    
    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "artistid" : artistid,
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps,
        "songid" : songid
    }
    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp", "artistid", "songid"])
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

    return Transformed_df[['ID','timestamp','artist_name','count','artistid','songid']]

def make_db(load_df):
    # Create a connection to the SQLite database
    conn = sqlite3.connect('song_history.db')

    # Write the DataFrame to an SQLite table
    load_df.to_sql('song_history', conn, if_exists='replace', index=False)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def spotify_etl():
    #Importing the songs_df from the Extract.py
    load_df=return_dataframe()
    Data_Quality(load_df)
    #calling the transformation
    Transformed_df=Transform_df(load_df)    
    print(load_df)
    make_db(Transformed_df)
    return (Transformed_df)

spotify_etl()