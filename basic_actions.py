
from random import randrange
class Actions():

    def dice(self,taille):
        if taille == 1:
            return 1
        else:
            return randrange(1,taille)
    
    def disadvantage(self):
        lance1=self.dice(20)
        lance2=self.dice(20)
        return (lance2 if lance1>=lance2 else lance1)
    
    def advantage(self):
        lance1=self.dice(20)
        lance2=self.dice(20)
        return (lance2 if lance1<=lance2 else lance1)

    