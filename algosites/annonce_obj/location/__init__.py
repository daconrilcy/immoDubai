import pandas as pd

from baseconstants import PATH_FOLDER_DB, DB_GPS_FILE, DB_CITIES_FILE


class Location:
    id_loc = 0
    adress1 = ''
    adress2 = ''
    adress3 = ''
    cp = ''
    district = None
    city = None
    google_map_link = ''
    gps = None

    def __init__(self, id_loc, adress1, adress2='', adress3='', cp='', district=None, city=None, googlelink='', gps=None):
        self.id_loc = id_loc
        self.adress1 = adress1
        self.adress2 = adress2
        self.adress3 = adress3
        self.cp = cp
        self.district = district
        self.city = city
        self.google_map_link = googlelink
        self.gps = gps


class Zone:
    id_zone = 0
    name_zone = ''
    gps = None

    def __init__(self, id_zone, name, gps=None):
        self.id_zone = id_zone
        self.name_zone = name
        self.gps = gps


class District(Zone):
    pass


class City(Zone):
    pass


class GPS:
    lat = ''
    lon = ''

    def __init__(self, lon='', lat=''):
        self.lon = lon
        self.lat = lat

    def parse(self):
        return str(self.lon)+','+str(self.lat)


def mem_locations():
    gps = pd.read_csv(PATH_FOLDER_DB + DB_GPS_FILE, index_col="n")
    gps_obj = []
    cities = pd.read_csv(PATH_FOLDER_DB + DB_CITIES_FILE, index_col="n")
    cities_obj = []
    for n in range(gps.__len__()):
        gps_obj.append(GPS(gps.lon[n], gps.lat[n]))
    for n in range(cities.__len__()):
        cities_obj.append(City(cities.index[n], cities.name_city[n], gps_obj[cities.gp_id[n]]))
