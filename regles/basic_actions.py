from personnage import Perso
from random import randrange
class Combat():
    def __init__(self,attack):
        self.attack=attack


    def dice(self,taille);
        return randrange(1,taille)

    def attack(self,disadv=False, adv=False):
        if disadv:
            lance=self.disadvantage()
        elif adv:
            lance=self.advantage()    
        else:
            lance=self.dice(20)
        return self.perso.attack+lance
    
    def disadvantage(self):
        lance1=self.dice(20)
        lance2=self.dice(20)
        if lance1>=lance2: return lance=lance2 else: return lance=lance1
    
    def advantage(self):
        lance1=self.dice(20)
        lance2=self.dice(20)
        if lance1<=lance2: return lance=lance2 else: return lance=lance1

    