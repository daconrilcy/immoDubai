from tools import get_json_from_url

# Classe de base de requete


class BaseGet:
    def __init__(self, nb_item_to_catch=0, url=None):
        self.base_url = url
        self.extend_url = ''
        self.nb_item_to_catch = nb_item_to_catch
        self.json_file = None
        self.datas = []
        self.currency = None
        self.update()
        self.ndatas = 0

    def update(self):
        pass

    def set_nb_item(self, nb_item=0):
        if nb_item > 0:
            self.nb_item_to_catch = nb_item

    def set_extend_url(self, e_url=None):
        if e_url is not None:
            self.extend_url = e_url

    def limit_to_nb_item_by_url(self):
        if self.nb_item_to_catch > 0:
            self.base_url += self.extend_url + str(self.nb_item_to_catch)

    def set_url_base(self, url=None):
        if url is not None:
            self.base_url = url

    def getjson(self, url=None, nb_item=0):
        self.set_url_base(url)
        self.set_nb_item(nb_item)
        self.limit_to_nb_item_by_url()
        self.json_file = get_json_from_url(self.base_url)

    def getdatas(self):
        pass
