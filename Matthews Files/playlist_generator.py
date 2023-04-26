import requests

import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime 
import sqlite3





def get_seed():
  import random
  import pandas as pd

  # Open the file and read its contents into a list of strings
  # Read the two columns from the text file into a DataFrame
  df = pd.read_csv('filename.txt', sep=' ', header=None, names=['col1', 'col2'])

  # Choose a random row from the DataFrame
  random_row = df.sample(n=1)

  # Save the items in col1 and col2 to two separate variables
  random_song = random_row['col1'].values[0]
  random_artist = random_row['col2'].values[0]
  
  get_reccomendations(random_song,random_artist)
  


def get_reccomendations(random_song, random_artist):
  
  endpoint_url = "https://api.spotify.com/v1/recommendations?"
  user_id = "7gau3mfurpamvofd00ej790p9" 
  TOKEN = "BQC0-M6U5ALe83lvnVJ9eJpi_4Gb1rXjAWUcWT_YsDm9yYEWogmSZ-DZobb8hdnMgpZVqh_UqYm1oPuyckokx-kv3rc_05FlOODeJxpJjhuqNpjLUpV8zSQWjlTCM7PN_voodJ73dIbdxayVAZOSYtPUK3lMrKMfL9THuyYCovXGmH7R54ZTF38w8jqqr_AFtXQ3-_yTW82g2t2M85Dl0FQPYL5n_oDwr0BXjN8aC4q9TJlsIECTD5B0NMZBnHaAqvBXlaCk_Pgbemy64enP0Mq3OGq_uVjZlIJUsKBQzWVfvSOX3AotSrE7qyNsJ3ncfrdrrwBj3PaV7GhEPoIohTp1N_nZqY1A9bBFSzqjdGxr0_Q"
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
  recc_df = pd.DataFrame(song_dict)
  make_db(recc_df)
  make_playlist(user_id, TOKEN,uris, random_artist) 



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
            
           

def make_playlist(user_id, TOKEN,uris,random_artist):
  
  #MAKING THE PLAYLIST
  endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
  request_body = json.dumps({
            "name": "{artist} style playlist".format(artist = random_artist),
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

  print(response.status_code)
  
get_seed()
