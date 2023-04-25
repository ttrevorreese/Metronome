import requests

endpoint_url = "https://api.spotify.com/v1/recommendations?"
TOKEN = ''   #TOKEN
user_id = '' #USER ID



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

#THIS IS THE PART WE CAN ADD ON TO OUR PREVIOSU RECCOMENDATION FILE
            
import json

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
                        "Authorization":"Bearer BQDQm4lfi1m11qczHmq7CE2OtE9A22c1cQJoheGAB0Bg3C0eBrwyGGCe7xVZoVHGtHaclraFxJY-ISDbyx78k35iCSwu9bk9_cga5wvt48ZWVTUzUCXPdhpgOnYYMqhKaJ02jIvOQkDJ1ZeYi5npZPNm-DaMENfGj9k6PFBRjU7fS0ZFhaUGyeYtU2mTzQkhqRQH0valpIbMW2cj1Cn-CqAt_woKcErlyMKP9gZXnX4NG7368ZisjiNBeNnRjvrCOpSJ3_Yugm6-E7GiDLI-rSnG0t5QPwCWFlTZaisDf-hLjJqf7fLzT5xyw1WZgzFMYTlq_85c0kW1SH-5jkN9hIitS58kBYKhmkzZhZWZVBllRjw"})

print(response.status_code)     #IF CODE 201 IS DISPLAYED IT MEANS IT WORKS
