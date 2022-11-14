import requests
import re
import os
import urllib.request
import pandas as pd
from baseconstants import PATH_PHOTOS_FOLDER_BG, DEFAULT_FOLDER, PHOTOS_FOLDER, PATH_FOLDER_BG, \
    AED_IN_EURO, BASE_URL_BLUEGROUND, BASE_HYPERLINK, BLUEGROUND_FOLDER
from baserequest import BaseGet
from tools import randomname, creategooglemaplink

props = []


def listephotorep(rep):
    listefichiers = []
    for (repertoire, sousRepertoires, fichiers) in os.walk(rep):
        listefichiers.extend(fichiers)
    return listefichiers


def photo_is_already_in(photoname, listphoto):
    result = False
    for ph in listphoto:
        if ph == photoname:
            result = True
            break
    return result


def is_folder_id_exist(id_prop):
    rep_id = PATH_PHOTOS_FOLDER_BG + id_prop + "\\"
    return os.path.exists(rep_id)


def foldername_idprop_photo(idprop):
    return PATH_PHOTOS_FOLDER_BG + idprop + "\\"


def createphotodir(id_propr=None):
    rep_id = ''
    if id_propr is not None:
        rep_id += foldername_idprop_photo(id_propr)
        if not is_folder_id_exist(id_propr):
            os.makedirs(rep_id)
    else:
        rep_id += PATH_PHOTOS_FOLDER_BG + "\\"
    return rep_id


def download_photos(linkphotos=None, id_propri=None):
    if linkphotos is not None and id_propri is not None:
        rep_id = createphotodir(id_propri)
        for phlink in linkphotos:
            phname = obtainphotoname(phlink)
            phname = rep_id + phname
            urllib.request.urlretrieve(phlink, phname)


def suppr_photos_name_non_original():
    reps = []
    folder = PATH_PHOTOS_FOLDER_BG
    for (repertoire, sousRepertoires, fichiers) in os.walk(folder):
        reps.append(repertoire)

    photos = []
    for rep in reps:
        ptps = listephotorep(rep)
        for ptp in ptps:
            if rep[-1] != '\\':
                photos.append(rep + "\\" + ptp)
            else:
                photos.append(rep + ptp)
    for photo in photos:
        if os.path.exists(photo):
            if not re.search('\w+-o-\w+-\w+-\w+-\w+-\w+\.avif$', photo):
                os.remove(photo)


def obtainphotoname(linkphoto):
    res = '\w+-o-\w+-\w+-\w+-\w+-\w+\.jpg$'
    val = re.search(res, linkphoto)
    if val:
        i_a = int(val.span(0)[0])
        i_b = int(val.span(0)[1]) - 4
        namephoto = linkphoto[i_a:i_b] + ".avif"
    else:
        namephoto = randomname(15) + ".avif"
    return namephoto


class CatchData(BaseGet):
    def __init__(self, nb_item_to_catch=0, url=None):
        super().__init__(nb_item_to_catch, url)
        self.photos = []

    def update(self):
        self.base_url = BASE_URL_BLUEGROUND
        self.extend_url = "&items="
        self.getjson()
        self.getdatas()

    def getdatas(self):
        self.datas = self.json_file['properties']['main']
        self.ndatas = len(self.datas)


def mainfunction(aedval=AED_IN_EURO, nbitem=0, update_photo="mid"):
    search_url = BASE_URL_BLUEGROUND
    # recherche limitée a x item
    # on modifies l'URL en précisant le nombre d'item passé en objet
    if nbitem > 0:
        search_url += "&items=" + str(nbitem)

    datas = requests.get(search_url).json()
    properties = datas['properties']['main']
    phts = []
    eadconv = aedval
    exclfct = BASE_HYPERLINK + '..\\'
    lastid = ''
    n = 1
    nprop = len(properties)
    suppr_photos_name_non_original()
    for prop in properties:
        idprop = str(prop['id'])
        if idprop != lastid:
            print(idprop, str(n) + " sur " + str(nprop), end="\n")
            lastid = idprop
        vals = {
            'id': idprop,
            'nom': prop['name'],
            'lien_photos': exclfct + DEFAULT_FOLDER + '\\' + BLUEGROUND_FOLDER + '\\' + PHOTOS_FOLDER + '\\' + idprop + '";"photos")',
            'dispo': prop['availableFrom'],
            'adresse_1': prop['address']['area'],
            'building': prop['address']['building'],
            'quartier': prop['address']['level2'],
            'ville': prop['address']['city'],
            'sdb': prop['bathrooms'],
            'pieces': int(prop['bedrooms']) + 1,
            'surface_m²': round(float(prop['lotSize']) * 0.092903),
            'etage': prop['highestFloor'],
            'vue_mer': 0,
            'prix_normal_AED': int(prop['baseRent']['amount']),
            'prix_normal_EUR': 0,
            'loc_remise_AED': prop['rent']['amount'],
            'loc_remise_EUR': 0,
            'duree_mini': prop['rent']['minDuration']['months'],
            'google_map': "",
            'lien': BASE_URL_BLUEGROUND + "/" + prop['path'],
            'pos_long': prop['address']['lng'],
            'pos_lat': prop['address']['lat'],
        }
        vals['prix_normal_EUR'] = int(float(vals.__getitem__('prix_normal_AED') * eadconv))
        vals['loc_remise_EUR'] = int(float(vals.__getitem__('loc_remise_AED') * eadconv))
        for am in prop['amenities']:
            if am['key'] == "seaView":
                vals['vue_mer'] = 1
        tmpphoto = {'id': idprop, 'links': []}
        for ph in prop['photos']:
            tmpphoto['links'].append(ph['url'])
        phts.append(tmpphoto)
        vals['google_map'] = creategooglemaplink(vals['pos_lat'], vals['pos_long'])
        props.append(vals)
        n += 1
    if update_photo == "full":
        for ph in phts:
            download_photos(ph['links'], ph['id'])
    if update_photo == "mid":
        n = 1
        for ph in phts:
            if not is_folder_id_exist(ph['id']):
                download_photos(ph['links'], ph['id'])
            else:
                foldername = foldername_idprop_photo(ph['id'])
                listphotos = listephotorep(foldername)
                for linkphoto in ph['links']:
                    photoname = obtainphotoname(linkphoto)
                    if not photo_is_already_in(photoname, listphotos):
                        phname = foldername + photoname
                        urllib.request.urlretrieve(linkphoto, phname)
            n += 1
            if n % 5 == 0:
                print(ph['id'] + ' - ' + str(n) + " sur " + str(nprop), end="\n")

    df = pd.DataFrame(props)
    file_path = PATH_FOLDER_BG + "blueground.csv"
    df.to_csv(file_path)
