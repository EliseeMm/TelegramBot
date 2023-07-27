import requests
import json

client = requests.get("https://api.open-meteo.com/v1/forecast?latitude=-29.86""&longitude=31.03&daily=temperature_2m_max,temperature_2m_min,rain_sum,showers_sum,precipitation_sum&timezone=auto")
data = client.json()


with open('weatherresults.json', 'w') as fp:
    json.dump(data,fp, indent=4)

def weather():
    """
    The weather function returns a string containing the weather forecast for the next 7 days.
    The output is formatted as follows:
    Date                 Min.T    Max.T    Rain
    2020-04-01 00:00:00  -2       10       0 mm/h
    
    :return: A string
    """
    days= data['daily']['time']
    max_temp = data['daily']['temperature_2m_max']
    min_temp = data['daily']['temperature_2m_min']
    rain = data['daily']['precipitation_sum']
    response = f'{"Date".center(30)} {"Min.T".center(15)} {"Max.T".center(10)} {"Rain".center(10)}\n'
    for i in range(len(days)):
        response += f"{str(days[i]).rjust(10,' ')}{str(min_temp[i]).rjust(12,' ')}{str(max_temp[i]).rjust(15,' ')}{str(rain[i]).rjust(15,' ')}\n"
    return response


def latitude_and_long(city):
    """
    The latitude_and_long function takes in a city name as an argument and returns the latitude and longitude of that city.
        The function first opens the geolocations.json file, which contains a list of dictionaries with each dictionary containing 
        information about one city (including its name, latitude, longitude). The function then iterates through this list to find 
        the dictionary whose 'city' key matches the inputted city name. Once it finds this match, it returns both its latitude and 
        longitude.
    
    :param city: Specify the city that you want to find the latitude and longitude for
    :return: A tuple of the latitude and longitude
    """
    with open('geolocations.json') as file :
        data = json.load(file)
    
    for i in data:
        if i['city'].lower() == city.lower():
            return i["lat"], i["lng"]


def selectedweather(city):
    """
    The selectedweather function takes a city name as an argument and returns the weather forecast for that city.
    The function uses the latitude_and_longitude function to get the coordinates of that city, then it uses those 
    coordinates to make a request to open-meteo.com's API and return a string containing information about temperature, rain etc.
    
    :param city: Get the latitude and longitude of the city
    :return: A string
    """
    latitude,longitude = latitude_and_long(city)
    client = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}" 
                            "&daily=temperature_2m_max,temperature_2m_min,rain_sum,showers_sum&timezone=auto")
    data = client.json()
    days= data['daily']['time']
    max_temp = data['daily']['temperature_2m_max']
    min_temp = data['daily']['temperature_2m_min']
    rain = data['daily']['rain_sum']
    response = f'{"Date".center(30)} {"Min.T".center(15)} {"Max.T".center(10)} {"Rain".center(10)}\n'
    for i in range(len(days)):
        response+=f"{str(days[i]).rjust(10,' ')}{str(min_temp[i]).rjust(12,' ')}{str(max_temp[i]).rjust(15,' ')}{str(rain[i]).rjust(15,' ')}\n"

    return response
