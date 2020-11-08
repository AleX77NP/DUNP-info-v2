import requests
import json

TOKEN_PATH = '' # enter local token path
REFRESH_URL='https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token='

with open(TOKEN_PATH, 'r') as token_file:
	old_token = token_file.read()
	refresh_response = requests.get(REFRESH_URL + old_token)
	new_token = json.loads(refresh_response.text)['access_token']

with open(TOKEN_PATH, 'w') as token_file:
	token_file.write(new_token)

