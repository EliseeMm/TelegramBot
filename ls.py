import requests
import http.client
import json
conn = http.client.HTTPSConnection("developer.sepush.co.za")

payload = ''
headers = {"token" : "55015410-617D4AFD-8FFBA538-428E48F9"}
id = "ethekwini2-14-glenwood"
conn.request("GET", f"/business/2.0/area?id={id}", payload, headers)
res = conn.getresponse()
data = res.read()

lis = data.decode("utf-8")
datas = json.loads(lis)

with open("load.json","w") as file:
    json.dump(datas,file,indent=4)

print(type(datas))
stage = 0 
for date_ in datas["schedule"]["days"][0]["stages"]:
    stage += 1
    times = ""
    if len(date_) == 0:
        times = "No affected"
    elif len(date_) == 1:
        times += date_[0]
    else:
        for i in date_:
            times += f"{i} "
    print(f"stage: {stage} ,times: {times}")


area_ids = {
    "glenwood 14": "ethekwini2-14-glenwood",
    "umbilo" : "ethekwini2-23-umbilo",
    "umbilo east 13" : "ethekwini2-13-umbiloeast",
}

# for key,value in area_ids.items():
#     print(key,value)
#     conn.request("GET", f"/business/2.0/area?id={value}&test=current", payload, headers)
#     res = conn.getresponse()
#     data = res.read()
#     print(data.decode("utf-8"))
    

# import requests

# url = "https://developer.sepush.co.za/business/2.0/areas_nearby?lat=-29.8842&lon=30.9790"

# # payload={}
# # headers = {}

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

# import requests

# url = "https://developer.sepush.co.za/business/2.0/status"

# # payload={}
# # headers = {}

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

