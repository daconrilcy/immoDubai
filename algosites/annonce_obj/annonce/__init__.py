import datetime

from algosites.annonce_obj.building import BuildingDubai


class Annonce:
    id_globale = None
    
    def __init__(self, id_annonce_site='', title='', link_annonce='', caract=None, photos_links=None, building=None):
        if photos_links is None:
            photos_links = []
        self.id_site = id_annonce_site
        self.title = title
        self.link = link_annonce
        self.photos_link = photos_links
        self.caract = caract
        if building is None:
            self.building = BuildingDubai()
        self.date_down = datetime.datetime.now()
        self.off_line = False
        self.date_off_line = None
