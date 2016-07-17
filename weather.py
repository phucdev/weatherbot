#! /usr/bin/env python

"""
Author: Phuc Tran Truong, Marcus Ding
Date: 17.07.2016

What it is supposed to do:
1. retrieve data from the openweathermap API
2. save it in a dictionary
3. send the information back in a human friendly way as a string

arguments: place, time and type of query
"""

import math     # for rounding values
import requests # kinda self-explanatory, but it's used for the geo location retrieval via ip-adress
import pyowm    # python wrapper for openweathermap api

# replace with your own API-key at openweathermap.org
owm = pyowm.OWM(API_key='0ce70d38fc4aaade9c6f004e226e8a61', language='de')

# all the methods that take data from weather_data and display it in a human friendly way
def weather(w_data):
    # or .capitalize, gotta work on the output of the status
    return w_data['detailed_status'].title() + ". Die Temperatur beträgt " + str(round(w_data['temperature']['temp'], 1))+" °C. "

def temperature(w_data):
    s = "Die Höchsttemparatur wird tagsüber bei " + str(round(w_data['temperature']['temp_max'], 1))+"° und die Tiefsttemperatur in der Nacht bei " + str(round(w_data['temperature']['temp_min'], 1))+"° liegen. Es sind " + str(round(w_data['temperature']['temp'], 1))+" °C. "
    return s

def humidity(w_data):
    return "Die Luftfeuchtigkeit beträgt " + str(w_data['humidity']) + " %. "

def wind(w_data):
    try:
        s = " aus Richtung " + getDirection(w_data['wind']['deg'])
    except KeyError:
        s = ""
    return "Der Wind weht" + s + " mit einer Geschwindigkeit von " + str(w_data['wind']['speed']) + " m/s. "

def getDirection(deg):
  direction = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
  if deg == None or deg == False:
      return ""
  return direction[math.floor(deg/45)];

# boolean section
def rainy(w_data):
    if w_data['rainy']:
        return "Es regnet 🌧 "
    else:
        return "Es regnet nicht. "

def sunny(w_data):
    if w_data['sunny']:
        return "Es ist sonnig 🌞 "
    else:
        return "Es ist nicht sonnig. "

def cloudy(w_data):
    if w_data['cloudy']:
        return "Es ist bewölkt 🌥 "
    else:
        return "Es ist nicht bewölkt. "

def foggy(w_data):
    if w_data['foggy']:
        return "Es ist neblig 🌫. "
    else:
        return "Es ist nicht neblig. "

def hurricane(w_data):
    if w_data['hurricane']:
        return "Es gibt einen Hurricane 🌪. "
    else:
        return "Es gibt keinen Hurricane. "

def snowy(w_data):
    if w_data['snowy']:
        return "Es schneit 🌨. "
    else:
        return "Es schneit nicht. "

def stormy(w_data):
    if w_data['stormy']:
        return "Es ist stürmisch 🌬. "
    else:
        return "Es ist nicht stürmisch. "

# activities
def bbq(w_data):
    s = weather(w_data)
    return s

def sailing(w_data):
    s = weather(w_data)+ wind(w_data)
    return s

def bike(w_data):
    s = weather(w_data)+ wind(w_data)
    return s

def swim(w_data):
    s = weather(w_data)
    return s

def surfing(w_data):
    s = weather(w_data)
    return s

def fetch_weather(w,forecast,time):
    weather_data = {}
    # int: GMT UNIX time of weather measurement
    weather_data['reference'] = pyowm.utils.timeformatutils.to_ISO8601(w.get_reference_time())
    # int: GMT UNIX time of sunrise
    weather_data['sunrise'] = pyowm.utils.timeformatutils.to_ISO8601(w.get_sunrise_time())
    # int: GMT UNIX time of sunset
    weather_data['sunset'] = pyowm.utils.timeformatutils.to_ISO8601(w.get_sunset_time())
    # pyowm.utils.timeformatutils.to_ISO8601() converts to readable date time format
    # int: cloud coverage percentage
    # weather_data['clouds'] = w.get_clouds()
    # dict: precipitation info
    # weather_data['rain'] = w.get_rain()
    # dict: snow info
    # weather_data['snow'] = w.get_snow()
    # dict: wind info 'deg', 'speed'
    weather_data['wind'] = w.get_wind()
    # int: atmospheric humidity percentage
    weather_data['humidity'] = w.get_humidity()
    # int: atmospheric pressure info
    # weather_data['pressure'] = w.get_pressure()
    # dict: temperature info 'temp', 'temp_min', 'temp_max'
    weather_data['temperature'] = w.get_temperature('celsius')
    # Unicode: short weather status
    # weather_data['status'] = w.get_status()
    # Unicode: detailed weather status
    weather_data['detailed_status'] = w.get_detailed_status()
    # int: OWM weather condiction code
    # weather_data['code'] = w.get_weather_code()
    # Unicode: weather-related icon name
    # weather_data['icon'] = w.get_weather_icon_name()
    # float: visibility distance
    # weather_data['vis_distance'] = w.get_visibility_distance()
    # float: dewpoint
    # weather_data['dewpoint'] = w.get_dewpoint()
    # float: Canadian humidex
    # weather_data['humidex'] = w.get_humidex()
    # float: heat index
    # weather_data['heat_index'] = w.get_heat_index()
    # boolean
    weather_data['cloudy'] = forecast.will_be_cloudy_at(time)
    weather_data['foggy'] = forecast.will_be_foggy_at(time)
    weather_data['hurricane'] = forecast.will_be_hurricane_at(time)
    weather_data['rainy'] = forecast.will_be_rainy_at(time)
    weather_data['snowy'] = forecast.will_be_snowy_at(time)
    weather_data['stormy'] = forecast.will_be_stormy_at(time)
    weather_data['sunny'] = forecast.will_be_sunny_at(time)
    return weather_data

def locate():
    r = requests.get('http://ipinfo.io/city')
    return r.text

def deliver(q, t='aktuell', p=locate()):
    forecast = owm.daily_forecast(p)
    observation = owm.weather_at_place(p)
    w = observation.get_weather()
    data = fetch_weather(w,forecast,t)
    info = forecast.get_forecast().get_location().get_name() + ', ' + forecast.get_forecast().get_location().get_country() + '(' + str(t) + '): '
    # add additional functionality please
    try:
        answer = eval(q+"(data)")
        return info + answer
    except (TypeError, NameError, pyowm.exceptions.not_found_error.NotFoundError) as e:
        return 'Deine Abfrage habe ich nicht verstanden. Schicke sie bitte an meine Schöpfer auf https://github.com/phucdev/weatherbot'
