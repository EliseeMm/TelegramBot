import http
import requests
from pprint import pprint
import json

client = requests.get("https://api.open-meteo.com/v1/forecast?latitude=-29.86&longitude=31.03&daily=temperature_2m_max,temperature_2m_min,rain_sum&timezone=auto")
data = client.json()


with open('weatherresults.json', 'w') as fp:
    json.dump(data,fp, indent=4)

def weather(message,bot):
    days= data['daily']['time']
    max_temp = data['daily']['temperature_2m_max']
    min_temp = data['daily']['temperature_2m_min']
    rain = data['daily']['rain_sum']
    bot.reply_to(message,"Getting the next 7 days weather")
    response = f'{"Date".center(30)} {"Min.T".center(15)} {"Max.T".center(10)} {"Rain".center(10)}\n'
    for i in range(len(days)):
        response+=f"{str(days[i]).rjust(10,' ')}{str(min_temp[i]).rjust(12,' ')}{str(max_temp[i]).rjust(15,' ')}{str(rain[i]).rjust(15,' ')}\n"
    print("date".center(20))
    bot.send_message(message.chat.id,response)



def latitude_and_long(city):
    with open('geolocations.json') as file :
        data = json.load(file)
    
    for i in data:
        print(i['city'])
        if i['city'].lower() == city.lower():
            print("here")
            return i["lat"], i["lng"]
    # print(data)


print(latitude_and_long('durban'))