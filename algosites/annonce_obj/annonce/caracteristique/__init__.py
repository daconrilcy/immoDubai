class CaractAnnonce:
    id_annonce = None
    nb_sdb = 0
    nb_piece = 0
    nb_chambre = 0
    vue = ''

    def __init__(self, id_annonce):
        self.id_annonce = id_annonce

    def add_attributes(self, attr=None):
        if attr is None:
            attr = []
        for at in attr:
            self.__setattr__(at,'')
