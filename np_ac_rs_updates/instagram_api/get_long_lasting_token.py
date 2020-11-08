import requests
import json

LONG_LIVED_TOKEN_URL = 'https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token='

short_token = input('Enter your short-lived token:')
token_response = requests.get(LONG_LIVED_TOKEN_URL + short_token)
print(token_response)
token = json.loads(token_response.text)['access_token']
print('Long-lived access token is:')
print(token)
