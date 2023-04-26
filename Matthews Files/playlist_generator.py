import requests

endpoint_url = "https://api.spotify.com/v1/recommendations?"
TOKEN = "BQCRWvjv_-trzxW02y3UaJkcf5EUFf7FANWiyJx8rI1Gw8qoS9yAWkpRd0_tKP0jq-RwAnVQRTlyhazU1sq4-aAUyxneVvjWXtHtvqT0RoA02GGWQ5UEENjzlwwSW0cBMevVziCmqOrCIYqkgJeCxfSushl8psM-aFeVfhIx0WcTQnRwfnyxwbbL_gkCRrQbEsblCh2XDGBAj_5pbNWxTQM6i-vG76Ykq3mVH_DgxLk09RZEY05jrQkDlV1GmQrdjtsLPwuyjkYWqQPCVW85LNulJYrubUxhtzqdzDoBNoMcgilqFdEraLI54Il--6DkJxXk8nLsqUKxNwsLUkX9vGfb91FEAZJT"
user_id = 'reesespieces07' #USER ID

########################################################################################################


# I MADE A NEW RECCOMENDATION ENGINE FOR THE TEST BUT THIS SHOULD BE ABLE TO EB DELETED FROM THIS FILE

# OUR FILTERS
limit= 50
market="GB"
seed_genres="hip-hop"
target_danceability=0.9
seed_artists = '2jku7tDXc6XoB6MO2hFuqg'
seed_tracks='7n0lXKEOaFxrAU0R93fIQh'
query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}'
query += f'&seed_artists={seed_artists}'
query += f'&seed_tracks={seed_tracks}'

query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}'

response =requests.get(query, 
               headers={"Content-Type":"application/json", 
                        "Authorization":"Bearer {TOKEN}".format(TOKEN=TOKEN)})

json_response = response.json()

uris = [] 

for i in json_response['tracks']:
            uris.append(i['uri'])
            print(f"\"{i['name']}\" by {i['artists'][0]['name']}")
            
############################################################

#THIS IS THE PART WE CAN ADD ON TO OUR PREVIOUS RECCOMENDATION FILE
            
import json

endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
request_body = json.dumps({
          "name": "Metronome",
          "description": "This playlist was generated in a data pipeline!",
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
                        "Authorization":"Bearer {token}".format(token=TOKEN)})

print(response.status_code)  # IF CODE 201 IS DISPLAYED IT MEANS IT WORKS