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
  with open('songids.txt', 'r') as file:
      lines = file.readlines()
      # Strip the newline character from each line
      lines = [line.strip() for line in lines]

  # Choose a random line from the list
  #this choses a random track to use as a seed track
  random_song = random.choice(lines)
  get_reccomendations(random_song)
  


def get_reccomendations(random_song):
  
  endpoint_url = "https://api.spotify.com/v1/recommendations?"
  user_id = "7gau3mfurpamvofd00ej790p9" 
  TOKEN = "BQCuvxjON0t65E_8IR4e1TBzB4nPOAeHJN1v0PBIALtUDwHLmCeWYDBPlQdyyC8wJDC3FukRHzaBnorZf0y-COuUMUcPrpvMxvc6fte_ysSodWz1HkRwKgHtq-0mZRoxeLwcD6-v26csQksEpzUAtBY6XdOA6y_JeDf0i4dGwZ_TcqrDuV65jw9eQQdx_-lxTr4tLq0TDcjQW7mVT2BgFmoSVFD7sJ8y2yPh2JR9bUcMZe0rhyZrHKnpr0kDK8yzpDUIcM8QOxUBcPmTw2l37Z7o7WBjGORp51mNUWM4T1lcGNNiDVCodp8AU21sb6EpH1QHWSmFB_Nvx9VYP2vsHGS6A2Cer5oZj_uFBqeI1M9U_BI"
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
  make_playlist(user_id, TOKEN,uris) 



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
            
           

def make_playlist(user_id, TOKEN,uris):
  endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
  request_body = json.dumps({
            "name": "Indie bands like Franz Ferdinand but using Python",
            "description": "My first programmatic playlist, yooo!",
            "public": False # let's keep it between us - for now
          })
  response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                          "Authorization":"Bearer {TOKEN}".format(TOKEN=TOKEN)})



  playlist_id = response.json()['id']


  last_endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

  request_body = json.dumps({
            "uris" : uris
          })
  response = requests.post(url = last_endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                          "Authorization":"Bearer {TOKEN}".format(TOKEN=TOKEN)})

  print(response.status_code)
  
get_seed()
