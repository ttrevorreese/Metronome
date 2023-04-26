import requests
import pandas as pd            
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
  get_recommendations(random_song)
  
def get_recommendations(random_song):
  
  endpoint_url = "https://api.spotify.com/v1/recommendations?"
  user_id = "reesespieces07" 
  TOKEN = "BQCRWvjv_-trzxW02y3UaJkcf5EUFf7FANWiyJx8rI1Gw8qoS9yAWkpRd0_tKP0jq-RwAnVQRTlyhazU1sq4-aAUyxneVvjWXtHtvqT0RoA02GGWQ5UEENjzlwwSW0cBMevVziCmqOrCIYqkgJeCxfSushl8psM-aFeVfhIx0WcTQnRwfnyxwbbL_gkCRrQbEsblCh2XDGBAj_5pbNWxTQM6i-vG76Ykq3mVH_DgxLk09RZEY05jrQkDlV1GmQrdjtsLPwuyjkYWqQPCVW85LNulJYrubUxhtzqdzDoBNoMcgilqFdEraLI54Il--6DkJxXk8nLsqUKxNwsLUkX9vGfb91FEAZJT"
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
  make_playlist(user_id, TOKEN,uris) 

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
              
def make_playlist(user_id, TOKEN,uris):
  endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
  request_body = json.dumps({
            "name": "Metronome",
            "description": "This playlist was created using a data pipeline!",
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
