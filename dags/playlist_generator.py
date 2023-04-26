import requests
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime 
import sqlite3
import random
import time

def get_seed():
  # Open the file and read its contents into a list of strings
  # Read the two columns from the text file into a DataFrame
  df = pd.read_csv('filename.txt', sep=' ', header=None, names=['col1', 'col2'])

  # Choose a random row from the DataFrame
  random_row = df.sample(n=1)

  # Save the items in col1 and col2 to two separate variables
  random_song = random_row['col1'].values[0]
  random_artist = random_row['col2'].values[0]
  
  get_recommendations(random_song,random_artist)

def get_recommendations(random_song, random_artist):
  #TOKEN LINK - https://developer.spotify.com/
  endpoint_url = "https://api.spotify.com/v1/recommendations?"
  user_id = "reesespieces07" 
  TOKEN = "BQDp67zDwWtHKVeQ8tJKKLaTJkM1NQ_LhBWSm8rlKWBETd8G9QgTzx9gNOPIevPxFPYJGkWxOpWfCAiorNK9z1yGQ8gdY_BG4bO7C7h0tNHvDZXv85kScplrXFuCU-9PqdJh6QeY4cDadhTaMMPWYo80dTpP0MHa-hT_2lHwkvhbzTgq_ySgfOKZQvK33QZ1GosM_X6r-J9go14jAO9Jh1TRqiThnNi_Td4wNzzDQn8NWEC2N9KGPIZx46jFVDfm_xhGXgEPUP3ziKG9PYfjY-EghtsiirbsDScWLsXMniicFlJ3Xu56FjPeNhN3eM8rKUYd1L4HCiYeQb8aU0BjsZd3shQ-b3n5"
  # OUR FILTERS
  limit= 50
  market="US"
  seed_genres="hip-hop"
  seed_artists = ''
  target_danceability=0.9
  seed_tracks= random_song # ID for Cassius by Foals
  query = f'{endpoint_url}limit={limit}&market={market}&target_danceability={target_danceability}'
  #query += f'&seed_artists={seed_artists}'
  query += f'&seed_tracks={seed_tracks}'

  response =requests.get(query, 
                headers={"Content-Type":"application/json", 
                          "Authorization":"Bearer {TOKEN}".format(TOKEN=TOKEN)})

  json_response = response.json()

  uris = []
  name = []
  song_name = []
  song_uri=[]

  for i in json_response['tracks']:
              uris.append(i['uri'])
              print(f"\"{i['name']}\" by {i['artists'][0]['name']}")
              song_name = []
              name = []
              song_uri = []
              
  song_dict = {"Artist Name": name, "Song Name": song_name, 'uris' : song_uri}

  # Convert the dictionary into a DataFrame
  rec_df = pd.DataFrame(song_dict)
  make_db(rec_df)
  make_playlist(user_id, TOKEN,uris, random_artist) 

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
            
def make_playlist(user_id, TOKEN,uris,random_artist):
  
  #MAKING THE PLAYLIST
  endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
  request_body = json.dumps({
            "name": "{artist} Style Playlist".format(artist = random_artist),
            "description": "Playlist created by Metronome",
            "public": False # let's keep it between us - for now
          })
  response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                          "Authorization":"Bearer {TOKEN}".format(TOKEN=TOKEN)})
  
  playlist_id = response.json()['id']

  #FILLING OUT THE PLAYLIST
  last_endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

  request_body = json.dumps({
            "uris" : uris
          })
  response = requests.post(url = last_endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                          "Authorization":"Bearer {TOKEN}".format(TOKEN=TOKEN)})

  if response.status_code == 201:
      print("Run successful - Code: {code}".format(code=response.status_code))
  else:
      print("Unsuccessful run - Error Code: {code}".format(code=response.status_code))
  
def start():
    from datetime import datetime
    Time = datetime.now()
    print("Starting program at: {time}".format(time=Time))
    time.sleep(5)
    while True:
        print("Executing playlist generator at: {time}".format(time=Time))
        get_seed()
        time.sleep(10)
start()