
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime 
import sqlite3
TOKEN = ""  #can be imported from the other file
def read_db():
    import sqlite3
    import pandas as pd

    # Create a connection to the SQLite database
    conn = sqlite3.connect('song_history.db')

    # Read the contents of the "song_history" table into a DataFrame
    song_df = pd.read_sql_query("SELECT * from song_history", conn)

    # Close the database connection
    conn.close()

    # Print the DataFrame
    make_recc(song_df)
    



def make_recc(song_df):
    import requests

    endpoint_url = "https://api.spotify.com/v1/recommendations?"

    limit=50
    market="GB"
    seed_genres="hip-hop"
    target_danceability=0.9

    import random

    # Select a random row from the song_df DataFrame
    random_row = song_df.sample()

    # Get the artistid from the selected row
    artist_id = random_row['artistid'].values[0]

    # Look up the corresponding artist name from the artist_name column
    artist_name = song_df.loc[song_df['artistid'] == artist_id, 'artist_name'].values[0]

    # Print the artist name
    print(f"Randomly selected artist: {artist_name}")

    seed_artists = artist_id # ID for Drake
    query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}'
    query += f'&seed_artists={seed_artists}'
    response =requests.get(query, 
                headers={"Content-Type":"application/json", 
                            "Authorization":"Bearer {token}".format(token = TOKEN)})

    #Put your token after the word bearer in the line above
    json_response = response.json()

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
    recc_df = pd.DataFrame(song_dict)

    # Print the resulting DataFrame
    print(recc_df)
    make_db(recc_df)




def make_db(recc_df):
       
    # Define the file path and database name
    db_path = "reccomendations.db"
    # Create a SQLite database connection
    conn = sqlite3.connect(db_path)

    # Create the recommendations table in the database
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recommendations
            (song_name text, name text)''')
    

    # Insert the DataFrame into the recommendations table
    recc_df.to_sql('recommendations', conn, if_exists='replace', index=False)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

read_db()