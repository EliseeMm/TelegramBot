import requests
import http.client
import json
conn = http.client.HTTPSConnection("developer.sepush.co.za")
payload = ''
headers = {"token" : "55015410-617D4AFD-8FFBA538-428E48F9"}

def response_loadshedding(message,bot):

    area_ids = {
        "Home": "ethekwini2-14-glenwood",
        "Work" : "ethekwini2-23-umbilo",
        "Lique" : "ethekwini2-13-umbiloeast",
    }
    bot.send_message(message.chat.id,"* indicates current loadshedding times")
    current_stage = get_stage()
    for key,value in area_ids.items():

        conn.request("GET", f"/business/2.0/area?id={value}&test=current", payload, headers)
        res = conn.getresponse()
        data = res.read()

        lis = data.decode("utf-8")
        datas = json.loads(lis)
        print(key)
        with open("load.json","w") as file:
            json.dump(datas,file,indent=4)      

        stage = 0 
        response = f"Location: {key}\nCurrent stage:{current_stage}\n"
        for date_ in datas["schedule"]["days"][0]["stages"]:
            currently = ""
            stage += 1
            times = ""
            if stage == current_stage:
                currently += "*"

            if len(date_) == 0:
                times = "Not affected"
            elif len(date_) == 1:
                times += date_[0]
            else:
                for i in date_:
                    times += f"{i} "
            response += f"{currently}Stage: {stage} ,Times: {times}\n\n"
        bot.send_message(message.chat.id,response)


def get_stage():
    print("Getting Current Load Shedding Stage")
    URL = "http://loadshedding.eskom.co.za/LoadShedding/GetStatus"
    r = requests.get(URL)
    data = r.json()
    stage = data -1
    return stage


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

