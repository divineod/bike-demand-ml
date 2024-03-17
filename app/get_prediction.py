import requests
import json

# URL of the Flask endpoint
url = 'http://127.0.0.1:5555/prediction'

# Data to be sent to the endpoint, change the date as necessary
data = {'date': '2025-06-17'}

# Send a POST request
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    print('Success:')
    print(response.json())
else:
    print('Failed:', response.status_code)
