import requests
import http.client
import json
conn = http.client.HTTPSConnection("developer.sepush.co.za")
payload = ''
headers = {"token" : "55015410-617D4AFD-8FFBA538-428E48F9"}

def response_loadshedding(message,bot):
    """
    The response_loadshedding function is used to get the loadshedding schedule for a specific area.
    The function takes in two parameters, message and bot. The message parameter is used to send the response back to 
    the user who sent the request and bot is used as an instance of telebot which allows us to use its methods such as 
    send_message()

    :param message: Get the message sent by the user
    :param bot: Send messages to the user
    :return: The loadshedding times for the current day
    """

    area_ids = {
        "Home": "ethekwini3-14a-glenwood",
        "Lique" : "ethekwini3-13a-umbiloeast",
    }
    current_stage = get_stage()
    for key,value in area_ids.items():

        conn.request("GET", f"/business/2.0/area?id={value}&test=current", payload, headers)
        res = conn.getresponse()
        data = res.read()

        lis = data.decode("utf-8")
        datas = json.loads(lis)
        with open("load.json","w") as file:
            json.dump(datas,file,indent=4)      

        stage = 0 
        response = f"Location: {key}\nCurrent stage:{current_stage}\n* indicates current loadshedding times\n\n"
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
    """
    The get_stage function returns the current stage of loadshedding.

    :return: The current stage of loadshedding
    """

    URL = "http://loadshedding.eskom.co.za/LoadShedding/GetStatus"
    r = requests.get(URL)
    data = r.json()
    stage = data -1
    return stage

def get_area():
    """
    The get_area function is used to get the area of a business.
        It takes no arguments and returns nothing.
    
    :return: A json file with the area information
    """
    conn.request("GET",'https://developer.sepush.co.za/business/2.0/areas_search?text=umbilo',payload,headers)
    res = conn.getresponse()
    data = res.read()

    lis = data.decode("utf-8")
    datas = json.loads(lis)
    with open("area.json","w") as file:
        json.dump(datas,file,indent=4)   
    

