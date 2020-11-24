
from items import Wikitem

class Inventaire():
    def __init__(self,nb_x,nb_y):
        self.nb_x = nb_x
        self.nb_y = nb_y
        self.nb_items = 0
        self.backpack = dict()

        for i in range(0,nb_x*nb_y+1):
            self.backpack[i] = None

    def ajouteritems(self,perso,piece):
        
        if(self.nb_items >= (self.nb_x*self.nb_y) or (perso.poid_actuel + piece.wheight ) > perso.poid_max):
            return
        else:
            i=0
            while self.backpack[i] != None:
                i += 1
            last_moove = i
            self.backpack[last_moove] = Wikitem[piece]
            perso.poid_actuel += piece.wheight
            self.nb_items += 1

    def enleveritems(self,perso,piece):
        for i in range(len(self.backpack)):
            if self.backpack[i] == piece:
                self.backpack[i] = None
                self.nb_items -=1
                perso.poid_actuel -= piece.wheight
      





