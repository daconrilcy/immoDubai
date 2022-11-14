import os.path

from baseconstants import PATH_REP_PHOTOS


def foldername_idprop_photo(idprop):
    return PATH_REP_PHOTOS + idprop + "\\"


def is_folder_id_exist(id_prop):
    rep_id = foldername_idprop_photo(id_prop)
    return os.path.exists(rep_id)


def createphotodir(id_propr=None):
    rep_id = ''
    if id_propr is not None:
        rep_id += foldername_idprop_photo(id_propr)
        if not is_folder_id_exist(id_propr):
            os.makedirs(rep_id)
    return rep_id


class TraitementPhotos:

    def __init__(self):
        self.list_files = []
        self.list_rep = []

    def is_photo_already_exist(self, photoname):
        for ph in self.list_files:
            if ph == photoname:
                return True
        return False
