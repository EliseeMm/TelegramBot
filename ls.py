import requests
import http.client
from pprint import pprint
conn = http.client.HTTPSConnection("developer.sepush.co.za")
payload = ''
headers = {"token" : "55015410-617D4AFD-8FFBA538-428E48F9"}
conn.request("GET", "/business/2.0/area?id=ethekwini2-14-glenwood&test=current", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

import requests

url = "https://developer.sepush.co.za/business/2.0/areas_nearby?lat=-29.8708&lon=30.9905"

# payload={}
# headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

import requests

url = "https://developer.sepush.co.za/business/2.0/status"

# payload={}
# headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

