import requests

token = ''

headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}

response = requests.get('https://api.genius.com/search?q=bad%20bunny', headers=headers)

data = response.json()