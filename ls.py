import requests
import http.client

conn = http.client.HTTPSConnection("developer.sepush.co.za")
payload = ''
headers = {"token" : "55015410-617D4AFD-8FFBA538-428E48F9"}
conn.request("GET", "/business/2.0/area?id=eskde-10-fourwaysext10cityofjohannesburggauteng&test=current", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
