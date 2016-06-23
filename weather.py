#! /usr/bin/env python

# Autor: Phuc Tran Truong
# Datum: 22.06.2016
# Stellt die Wetterdaten als String bereit

# Ort, Zeit und Wetter/Temperatur/rainy/sunny sollen an dieses Modul übergeben werden

from nltk.tokenize import word_tokenize
import math
import pyowm

owm = pyowm.OWM('0ce70d38fc4aaade9c6f004e226e8a61')

def temperature(w):
    temp = w.get_temperature('celsius')
    s = "Die Höchsttemparatur wird tagsüber bei " + str(round(w.get_temperature('celsius')['temp_max'], 1))+"° und die Tiefsttemperatur heute Nacht bei " + str(round(w.get_temperature('celsius')['temp_min'], 1))+"° liegen. Momentan sind es " + str(round(w.get_temperature('celsius')['temp'], 1))+"°. "
    return s

def rainy(forecast,time):
    if forecast.will_be_rainy_at(time):
        return "Es regnet. "
    else:
        return ''

def sunny(forecast,time):
    if forecast.will_be_sunny_at(time):
        return "Es ist sonnig. "
    else:
        return ''

def wind(w):
    return "Wind: " + getDirection(w.get_wind()['deg']) + " " + str(w.get_wind()['speed']) + "km/h. "

def getDirection(deg):
  direction = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
  if deg == None or deg == False:
      return ""
  return direction[math.floor(deg/45)];

def humidity(w):
    return str(w.get_humidity()) + "%% Luftfeuchtigkeit. "

def weather(w,forecast,time):
    return sunny(forecast,time)+rainy(forecast,time)+temperature(w)+wind(w)+humidity(w)

def deliver(p, t, q):
    observation = owm.weather_at_place(p)
    forecast = owm.daily_forecast(p)
    w = observation.get_weather()
    if t.lower() == 'morgen':
        when = pyowm.timeutils.now()
    else:
        when = pyowm.timeutils.tomorrow()
    if q.lower() == 'temperatur':
        return temperature(w)
    else:
        return weather(w,forecast,when)
