#! /usr/bin/env python

# Author: Phuc Tran Truong
# Date: 03.07.2016
# Extractor
import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import re
import datetime
import requests

def get_weekday(x):
    now = datetime.datetime.today()
    weekday = now.weekday()
    i = 0
    while x != (weekday + i) % 7:
        i += 1
    return now + datetime.timedelta(days=i)

# Time expressions
time_ex = {'montag': get_weekday(0), 'dienstag': get_weekday(1), 'mittwoch': get_weekday(2), 'donnerstag': get_weekday(3), 'freitag': get_weekday(4), 'samstag': get_weekday(5), 'sonntag': get_weekday(6), 'heute': datetime.datetime.today(), 'morgen': datetime.datetime.today()+datetime.timedelta(days=1), 'übermorgen': datetime.datetime.today()+datetime.timedelta(days=2)}

# Types of queries
query_ex = {'wetter': 'wetter', 'regen': 'regen', 'wind': 'wind', 'temperatur': 'temperatur', 'regnen': 'regen', 'regnet': 'regen', 'regenschirm': 'regen', 'sonne': 'sonne', 'sonnig': 'sonne', 'luftfeuchtigkeit': 'luftfeuchtigkeit', 'sonnenaufgang': 'sonnenaufgang', 'sonnenuntergang': 'sonnenuntergang', 'warm': 'temperatur', 'kalt': 'temperatur'}

def get_time(time):
    for e in time:
        if e in time_ex.keys():
            return time_ex[e]
    return datetime.datetime.today()

# locate User
def locate():
    r = requests.get('http://ipinfo.io/city')
    return r.text

# extracting Location
def get_location(loc):
    # currently working only on my computer
    st = StanfordNERTagger('/Users/Phuc/Desktop/stanford-ner-2015-12-09/classifiers/english.muc.7class.distsim.crf.ser.gz', '/Users/Phuc/Desktop/stanford-ner-2015-12-09/stanford-ner-3.6.0.jar')
    loc_ner = st.tag(loc)
    # control print
    print(loc_ner)
    # might be faster starting from back to front
    loc_tuples = [item[0] for item in loc_ner if 'LOCATION' in item]
    try:
        location = loc_tuples[0]
        if len(loc_tuples) > 1:
            for i in range(1,len(loc_tuples)):
                location += ' ' + loc_tuples[i]
    except IndexError:
        location = locate()
    return location

def get_query(query):
    for e in query:
        if e in query_ex.keys():
            return query_ex[e]
    return 'wetter'

# extracts arguments from the input
def get_args(request):
    request_tokens = word_tokenize(request)
    p = get_location(request_tokens)
    request_tokens = [item.lower() for item in request_tokens]
    t = get_time(request_tokens)
    q = get_query(request_tokens)
    return [t,p,q]
