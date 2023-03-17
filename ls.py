import requests
import http.client
from pprint import pprint

conn = http.client.HTTPSConnection("developer.sepush.co.za")
payload = 'eThekwini'
headers = {"token" : "55015410-617D4AFD-8FFBA538-428E48F9"}
conn.request("GET", "/business/2.0/areas_search?text=glenwood", payload, headers) # search by text
res = conn.getresponse()
data = res.read()
pprint(data.decode("utf-8"))
