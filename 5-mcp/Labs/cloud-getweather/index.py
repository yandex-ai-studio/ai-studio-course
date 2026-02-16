import requests
import os

def get_weather(event, context):
    city = event['city']
    api_key = os.environ['api_key'] 
    #res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
    geo = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}").json()
    lat = geo[0]['lat']
    lon = geo[0]['lon']
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric")
    return {
        'statusCode': 200,
        'body': res.json(),
    }