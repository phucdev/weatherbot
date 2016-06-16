#! /usr/bin/env python

# Autor: Phuc Tran Truong
# Datum: 14.06.2016
# Stellt die Wetterdaten als String bereit

# Ort, Zeit und Wetter/Temperatur/rainy/sunny sollen an dieses Modul übergeben werden

from nltk.tokenize import word_tokenize
import pyowm

owm = pyowm.OWM('0ce70d38fc4aaade9c6f004e226e8a61')

def temperature(w):
    temp = w.get_temperature('celsius')
    s = "Die Höchsttemparatur wird tagsüber bei " + str(w.get_temperature('celsius')['temp_max'])+"° und die Tiefsttemperatur heute Nacht bei " + str(w.get_temperature('celsius')['temp_min'])+"° liegen. Momentan sind es " + str(w.get_temperature('celsius')['temp'])+"°."
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

def weather(w,forecast,time):
    return sunny(forecast,time)+rainy(forecast,time)+temperature(w)

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
