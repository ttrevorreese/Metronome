import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime 
import sqlite3
import random
#TOKEN LINK - https://developer.spotify.com/
TOKEN = "BQCrRerfaKzBaaUpIdGWywP_Vmk1UyszOxiG6bkyqD-0lCXZV4sDHQMt1CvKE9Ze_orQsMQEHz9ca1B7Rv-q69LvpNBS35brrtXQNMaVUvZNqKHl0zbFgx01AFgxZjbOitRkcw4L_Tb4aGyXop1iwJAcrh5r5TnYd63wjUsGuiAo9R-iLyJRC8YbZOew4gPkpZydV96wtmRTc0qnWu-qZVTDxp2QZu24mB-uFgyTz465kpza61wKK5Yoc9Yful9JCdofQXZo_fJzheg3YTnFwJXC0c1dMOdjsk2MTHGaRQhuFfZjU6phTUNXBkSZwuEOn9KRPoX0TO5YG9LJd_DD3B2MMW0bRUs"
def read_db():
    # Create a connection to the SQLite database
    conn = sqlite3.connect('song_history.db')
    # Read the contents of the "song_history" table into a DataFrame
    song_df = pd.read_sql_query("SELECT * from song_history", conn)
    # Close the database connection
    conn.close()
    # Print the DataFrame
    make_rec(song_df)
    
def make_rec(song_df):
    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    limit=50
    market="GB"
    seed_genres="hip-hop"
    target_danceability=0.9
    # Select a random row from the song_df DataFrame
    random_row = song_df.sample()
    # Get the artistid from the selected row
    artist_id = random_row['artistid'].values[0]
    # Look up the corresponding artist name from the artist_name column
    artist_name = song_df.loc[song_df['artistid'] == artist_id, 'artist_name'].values[0]
    # Print the artist name
    print(f"Randomly selected artist: {artist_name}")

    seed_artists = artist_id
    query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}'
    query += f'&seed_artists={seed_artists}'
    response =requests.get(query, 
                headers={"Content-Type":"application/json", 
                            "Authorization":"Bearer {token}".format(token = TOKEN)})
    json_response = response.json()
    # Uncomment to see output of json_response variable
    #print(json_response)
    uris = []
    song_name = []
    name = []

    for i in json_response['tracks']:
        uris.append(i)
        print(f"\"{i['name']}\" by {i['artists'][0]['name']}")
        song_name.append(i['name'])
        name.append(i['artists'][0]['name'])

    # Create a dictionary from the song_name and name lists
    song_dict = {"Artist Name": name, "Song Name": song_name}
    # Convert the dictionary into a DataFrame
    rec_df = pd.DataFrame(song_dict)
    # Print the resulting DataFrame
    print(rec_df)
    make_db(rec_df)

def make_db(rec_df): 
    # Define the file path and database name
    db_path = "recommendations.db"
    # Create a SQLite database connection
    conn = sqlite3.connect(db_path)
    # Create the recommendations table in the database
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recommendations
            (song_name text, name text)''')
    # Insert the DataFrame into the recommendations table
    rec_df.to_sql('recommendations', conn, if_exists='replace', index=False)
    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

read_db()