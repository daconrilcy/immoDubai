import datetime


class PrixAnnonce:
    id_annonce = ''
    prix = []

    def __init__(self, id_annonce):
        self.id_annonce = id_annonce
        self.get_prix_from_file(id_annonce)

    def add_prix(self, prix_obj=None):
        if prix_obj is not None:
            self.prix.append(prix_obj)

    def get_prix_from_file(self, id_annonce):
        pass


class PrixObj:
    valeur = 0
    currency = None
    date_add = None

    def __init__(self, valeur=0, currencyname="AED", date_prix=None):
        self.valeur = valeur
        self.currency = currencyname
        if date_prix is None:
            date_prix = datetime.datetime.now()
        self.date_add = date_prix
