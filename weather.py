#! /usr/bin/env python

# Author: Phuc Tran Truong
# Date: 03.07.2016
# Delivers weather data as a string

# arguments: place, time and type of query

from nltk.tokenize import word_tokenize
import math
import requests
import pyowm

owm = pyowm.OWM('0ce70d38fc4aaade9c6f004e226e8a61')

def humidity(w_data):
    return "Die Luftfeuchtigkeit beträgt " + str(w_data['humidity']) + " %. "

def temperature(w_data):
    # "Die Höchsttemparatur wird tagsüber bei " + str(round(w.get_temperature('celsius')['temp_max'], 1))+"° und die Tiefsttemperatur heute Nacht bei " + str(round(w.get_temperature('celsius')['temp_min'], 1))+"° liegen.
    s = "Es sind " + str(round(w_data['temperature']['temp'], 1))+" °C. "
    return s

def rainy(w_data):
    if w_data['rainy']:
        return "Es regnet. "
    else:
        return "Es regnet nicht. "

def sunny(w_data):
    if w_data['sunny']:
        return "Es ist sonnig. "
    else:
        return "Es ist nicht sonnig. "

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

def weather(w,forecast,time):
    weather_data = {}
    # int: GMT UNIX time of weather measurement
    weather_data['reference'] = w.get_reference_time()
    # int: GMT UNIX time of sunrise
    weather_data['sunrise'] = w.get_sunrise_time()
    # int: GMT UNIX time of sunset
    weather_data['sunset'] = w.get_sunset_time()
    # pyowm.utils.timeformatutils.to_ISO8601() converts to readable date time format
    # int: cloud coverage percentage
    weather_data['clouds'] = w.get_clouds()
    # dict: precipitation info
    weather_data['rain'] = w.get_rain()
    # dict: snow info
    weather_data['snow'] = w.get_snow()
    # dict: wind info 'deg', 'speed'
    weather_data['wind'] = w.get_wind()
    # int: atmospheric humidity percentage
    weather_data['humidity'] = w.get_humidity()
    # int: atmospheric pressure info
    weather_data['pressure'] = w.get_pressure()
    # dict: temperature info 'temp', 'temp_min', 'temp_max'
    weather_data['temperature'] = w.get_temperature('celsius')
    # Unicode: short weather status
    weather_data['status'] = w.get_status()
    # Unicode: detailed weather status
    weather_data['detailed_status'] = w.get_detailed_status()
    # int: OWM weather condiction code
    weather_data['code'] = w.get_weather_code()
    # Unicode: weather-related icon name
    weather_data['icon'] = w.get_weather_icon_name()
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

def deliver(t='aktuell', p=locate(), q='wetter'):
    forecast = owm.daily_forecast(p)
    observation = owm.weather_at_place(p)
    w = observation.get_weather()
    data = weather(w,forecast,t)
    # either temperature or weather
    # add additional functionality please
    if q.lower() == 'temperatur':
        return temperature(data)
    else:
        return forecast.get_forecast().get_location().get_name() + ', ' + forecast.get_forecast().get_location().get_country() + ': ' + temperature(data) + humidity(data) + wind(data) + rainy(data) + sunny(data)
