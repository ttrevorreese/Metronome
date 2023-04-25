import requests

endpoint_url = "https://api.spotify.com/v1/recommendations?"
TOKEN = 'BQC5uC4I5YtM__ke3gkmLeJlYYaWjqMQT2aDU6Eqi1TmBft73rRn8rFuUb8bfz6ufyFmrs-a38rhjmRzKIp7bdGknSTd1DhoCQqpVbP1NJJYVxYqt5BuvRRj_jzBCiE8fQs3Bi4ordAar5z5WVJCZTkDvEGnjXMOeDBTBc5fSxVXyCeRqZ6-3quEYhjH64paJmWriCdz9R2ri8qOO6Hv_f9g3TkPiGacJtNfqSxfwED3_4_lABdiode7kpgVjBJzu2vw8-vNPK3RC-KL_Z2DwP_QcUyNQCIIriP9KK7-wlMyK4Q-L0GiKPCvfQ-HG0EkPXOqTgBTqYIDChfrfOD4xPE5vrZOvyOV'   #TOKEN
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
          "description": "This playlist was generated",
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