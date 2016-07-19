#! /usr/bin/env python

"""
Author: Phuc Tran Truong, Marcus Ding
Date: 19.07.2016

What it is supposed to do:
1. chop up the user input (tokenize)
2. extract location (NERTagger), datetime and type of request (check in dictionary), get a default argument if something is missing
3. send back the arguments
"""

import nltk
from nltk.tag import StanfordNERTagger  # Named Entity Recognizer
from nltk.tokenize import word_tokenize # chopping up the user input
import datetime # Montag = 0, Sonntag = 6
import requests

# calculates the datetime object for the weekday
def get_weekday(x):
    now = datetime.date.today()
    weekday = now.weekday()
    i = 0
    while x != (weekday + i) % 7:
        i += 1
    return now + datetime.timedelta(days=i)

# date expressions
date_ex = {'montag': get_weekday(0), 'dienstag': get_weekday(1), 'mittwoch': get_weekday(2), 'donnerstag': get_weekday(3), 'freitag': get_weekday(4), 'samstag': get_weekday(5), 'sonntag': get_weekday(6), 'heute': datetime.datetime.today(), 'morgen': datetime.datetime.today()+datetime.timedelta(days=1), 'übermorgen': datetime.datetime.today()+datetime.timedelta(days=2)}

# time expressions
time_ex = {'früh': datetime.time(8, 0, 0, 0), 'morgen': datetime.time(8, 0, 0, 0), 'mittag': datetime.time(12, 0, 0, 0), 'abend': datetime.time(18, 0, 0, 0), 'nacht': datetime.time(23, 0, 0, 0)}
# '18:30 Uhr' ?

# Types of queries
query_ex = {'wetter': "weather", 'regen': "rain", 'wind': "wind", 'windig': "wind", 'temperatur': "temperature", 'regnen': "rainy", 'regnet': "rainy", 'regenschirm': "rainy", 'sonne': "sunny", 'sonnig': "sunny", 'luftfeuchtigkeit': "humidity", 'sonnenaufgang': "sunrise", 'sonnenuntergang': "sunset", 'warm': "temperature", 'kalt': "temperature", 'bewölkt': "cloudy", 'wolke': "cloudy", 'nebel': "foggy", 'benebelt': "foggy", 'hurricane': "hurricane", 'schnee': "snowy", 'schneit': "snowy", 'schneien': "snowy", 'sturm': "stormy", 'stürmisch': "stormy", 'unwetter': "stormy", 'schön': "weather", 'schlecht': "weather", 'grillen': "bbq", 'segeln': "sailing", 'fahrrad': "bike", 'fahrradfahren': "bike", 'schwimmen': "swim", 'surfen': "surfing", 'jacke': "temperature"}

# interprets specific time of day
def get_spec_time(clock):
    # split into hour and minute, ignore seconds etc.
    hm_clock = clock.split(':', maxsplit=2)
    # check for invalid values, return the max/min possible value
    if int(hm_clock[0]) > 23:
        return datetime.time(23, 59, 0, 0)
    if int(hm_clock[0]) < 0:
        return datetime.time(0, 0, 0, 0)
    # if the minutes are specified
    if len(hm_clock) > 1:
        if int(hm_clock[1]) > 59:
            return datetime.time(int(hm_clock[0]), 59, 0, 0)
        elif int(hm_clock[1]) < 0:
            return datetime.time(int(hm_clock[0]), 0, 0, 0)
        else:
            # everything went ok
            return datetime.time(int(hm_clock[0]), int(hm_clock[1]), 0, 0)
    else:
        # only the hour was spcified
        return datetime.time(int(hm_clock[0]), 0, 0, 0)

# takes the user input and checks for date/time expressions from date_ex
def get_time(time):
    # default
    the_date = datetime.date.today()
    # check for date expression
    for d in time:
        if d in date_ex.keys():
            the_date = date_ex[d]
    # default
    the_time = datetime.datetime.now().time()
    # check for specific time of day
    try:
        # search for 'um'
        the_time = get_spec_time(time[time.index("um")+1])
    except (TypeError, ValueError) as e:
        try:
            # search for 'uhr' instead
            the_time = get_spec_time(time[time.index("uhr")-1])
        except (TypeError, ValueError) as e:
            # no specific time of day: check for time expression
            print("Error")
            for t in time:
                if t in time_ex.keys():
                    the_time = time_ex[t]
    return datetime.datetime.combine(the_date, the_time)

# locate User for default location/if the location is not specified
def locate():
    r = requests.get('http://ipinfo.io/city')
    return r.text

# extracting Location from the user input
def get_location(loc):
    """
    currently working only on my computer
    english Model
        english.muc.7class.distsim.crf.ser.gz
    german Models
        german.dewac_175m_600.crf.ser.gz
        german.hgc_175m_600.crf.ser.gz
    """
    # Named Entity Recognizer: recognizes named entities and assigns types like location, person, organization to the entity
    st = StanfordNERTagger('/Users/Phuc/Desktop/stanford-ner-2015-12-09/classifiers/english.muc.7class.distsim.crf.ser.gz', '/Users/Phuc/Desktop/stanford-ner-2015-12-09/stanford-ner-3.6.0.jar')
    loc_ner = st.tag(loc)
    """
    might be faster starting from back to front
        'LOCATION' for English
        'I-LOC' for German
    """
    # code that glues named entities like 'New York' back together
    loc_tuples = [item[0] for item in loc_ner if 'LOCATION' in item]
    try:
        location = loc_tuples[0]
        if len(loc_tuples) > 1:
            for i in range(1,len(loc_tuples)):
                location += ' ' + loc_tuples[i]
    except IndexError:
        # if no location is specified
        return None
    return location

# takes the user input and checks for query expressions from query_ex
def get_query(query):
    for e in query:
        if e in query_ex.keys():
            return query_ex[e]
    return None

def unknown_reply(args):
    reply = ""
    if(not args[0]):
        reply += "Deine Abfrage habe ich nicht verstanden. Schicke sie bitte an meine Schöpfer auf https://github.com/phucdev/weatherbot"
        return 1,reply
    if(not args[1]):
        reply += "Ich nehme an, dass du den aktuellen Zeitpunkt meinst.\n"
    if(not args[2]):
        reply += "Ich habe den Ort nicht verstanden, welchen Ort meinst du? 😓\n"
        return 2,reply
    return 3, reply

# extracts arguments from the input
def get_args(request):
    # NERTagger only works with proper capitalization
    request_tokens = word_tokenize(request)
    p = get_location(request_tokens)
    # the rest will be dealt with in lowercase which eliminates problems with incorrect capitalization
    request_tokens = [item.lower() for item in request_tokens]
    t = get_time(request_tokens)
    q = get_query(request_tokens)
    return [q,t,p,]
