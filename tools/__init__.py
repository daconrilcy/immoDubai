import requests
import os
from random import randrange

from baseconstants import BASE_HYPERLINK


def get_json_from_url(url):
    return requests.get(url).json()


def randomname(lname=10):
    listv = 'abcdefghijklmnopqrstuvwxyz0123456789'
    llist = len(listv)
    rname = ""
    for n in range(0, lname):
        a = randrange(llist)
        rname += listv[a]
    return rname


def convertionddtodms(val, latlon="lat"):
    card = "N"
    if latlon == 'lat':
        if val < 0:
            card = "S"
    elif val >= 0:
        card = "E"
    elif val < 0:
        card = "O"

    deg = str(int(val))
    minu = str(int((val - int(val)) * 60))
    sec = str(round((((val - int(val)) * 60) - int((val - int(val)) * 60)) * 60, 2))

    return deg + "°" + minu + "'" + sec + "\"" + card


def creategooglemaplink(lat, lng):
    googlecleartext = ';"google map")'
    base_ggle_url = 'https://www.google.com/maps/place/'
    new_lat = convertionddtodms(lat, "lat")
    new_lng = convertionddtodms(lng, "lng")
    hypelinkgoog = BASE_HYPERLINK + base_ggle_url + new_lat + "+" + new_lng + "/@" + str(lat) + "," + str(
        lng) + ',17z"' + googlecleartext
    return hypelinkgoog


def liste_file_in_rep(rep):
    listefichiers = []
    for (repertoire, sousRepertoires, fichiers) in os.walk(rep):
        listefichiers.extend(fichiers)
    return listefichiers
