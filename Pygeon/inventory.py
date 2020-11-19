
from items import Wikitem

class Inventaire():
    def __init__(self,nb_x,nb_y):
        self.nb_x = nb_x
        self.nb_y = nb_y
        self.nb_items = 0
        self.backpack = dict()

        for i in range(0,nb_x*nb_y+1):
            self.backpack[i] = None

    def ajouteritems(self,piece):
        if(self.nb_items >= (self.nb_x*self.nb_y)):
            return
        else:
            self.backpack[self.nb_items] = Wikitem[piece]
            self.nb_items += 1

    def enleveritems(self,piece):
        i = 0
        while self.backpack[i] != piece :
            i += 1
        self.backpack[i] = None
        self.nb_items -=1




