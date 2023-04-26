import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
from datetime import datetime
import sqlite3
import datetime 
### REPLACE USERNAME WITH YOURS
USER_ID = "mandevseahra_" 
### REPLACE TOKEN WITH YOURS FROM THE LINK BELOW
### TOKEN LINK - https://developer.spotify.com/
TOKEN = "BQBpcrX66xe_xXS0PI-Sza2zuZMv9WjPzR8ASlb4O_y0E8ZMYFcial1sixLXIr49Dgb2laqn3cc-ffg4f_Z8QnHV9HpYseAbFPdSBldNUFDxG9ofN3TVcjz96-qoUbucK2t-FN1MxpAt1Y9BJkfUsVrpov0GB6Sa2MlrfMK8DKN3d3JNsyhdeTBdC7dYcK0wrMBKMzdUo9wDoNkCgnWgno7kVzD_xa9VtUw1BGYqVizYoioA2tyezc9ECYMjRdYuhTprD4nHrSzIzRxLcrXHzDUh8vrx6wVetoIACqc71jCaBQ_vrX5HHSHCP2AfHG95_LRU3DjWTKAH7hyG3VqDucud5D_swgk"
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

    #Creating an array for each parameter from the Spotify API
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
    #The structure of the output using pandas
    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp", "artistid", 'songid'])
    
    #making text files woth the song id and artist name
    song_df[['songid', 'artist_name']].to_csv('filename.txt', sep=' ', index=False, header=False)
    with open('songids.txt', 'w') as f:
            for song_uri in song_df['songid']:
                f.write("%s\n" % song_uri)
    print(song_df)
    make_db(song_df)

#Function to create the SQLite database - holding 1 parameter
def make_db(song_df):
    # Create a connection to the SQLite database
    conn = sqlite3.connect('song_history.db')

    # Write the DataFrame to an SQLite table
    song_df.to_sql('song_history', conn, if_exists='replace', index=False)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

#Call the get_songs function
get_songs()