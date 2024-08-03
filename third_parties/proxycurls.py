import requests

api_key = "KK5oiKHin6XzILl-ggcBig"
headers = {"Authorization": "Bearer " + api_key}
api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
params = {
    "url": url
}
response = requests.get(api_endpoint, params=params, headers=headers)
import json

with open("data2.json", "w") as f:
    json.dump(response.json(), f)
print(response.text)
