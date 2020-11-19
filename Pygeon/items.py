
import pygame,os

Wikitem = {}
# https://stackoverflow.com/questions/54503270/how-to-load-a-large-number-of-images-in-pygame-by-a-simple-way
class Items():
    def __init__(self,value,wheight,wpn_type,wpn_name,wpn_img):
        self.value = value
        self.wpn_img = wpn_img
        self.wpn_name = wpn_name
        self.wpn_type = wpn_type
        self.wheight= wheight
        if (self not in Wikitem):
            Wikitem[self] = len(Wikitem)

class Consomable(Items):
    def __init__(self,value,wheight,wpn_type,wpn_name,wpn_img,hp_gain=0,dmg=0,element=0):
        Items.__init__(self,value,wheight,wpn_type,wpn_name,wpn_img)
        self.hp_gain = hp_gain
        self.dmg = dmg


class Weapon(Items):
    def __init__(self,prix,wheight,dmg,wpn_name,wpn_type,wpn_img):
        Items.__init__(self,prix,wheight,wpn_type,wpn_name,wpn_img)
        self.dmg = dmg

class Armor(Items):
    def __init__(self,value,defense,wheight,armor_name,wpn_type,armor_img):
        Items.__init__(self,value,wheight,wpn_type,armor_name,armor_img)
        self.defense = defense
        

#  REFERENCE : https://www.d20pfsrd.com/equipmenT/weapons/#weapons-simple
#  REFERENCE : WEAPON(PRIX,POID,DOMMAGE,TYPE,NOM)

# PATH RESOLUTION : 
first_path = "Pygeon/Addon/Sprite/Items/" # INSERER PATH VERS LE DOSSIER ITEMS

def image_loader(path) -> str:
    for i in os.listdir(path):
        yield (i,pygame.image.load(path + i))

image = dict(image_loader(first_path))
for x in image:
    image[x] = pygame.transform.scale(image[x],(50,50))

# WEAPON : INDEX 4 / 5
item_index = 4
    # UNARMED


    # LIGHT MELEE WEAPON


    # SWORD SECTION

Sword1 = Weapon(15,8,6,"ONE_HANDED",item_index ,image['W_Sword001.png'])
Sword2 = Weapon(15,8,6,"ONE_HANDED",item_index ,image['W_Sword002.png'] )
Sword3  = Weapon(15,8,6,"ONE_HANDED",item_index ,image['W_Sword003.png'])
Sword4  = Weapon(15,8,6,"ONE_HANDED",item_index ,image['W_Sword004.png'] )
Sword5 = Weapon(15,8,6,"ONE_HANDED",item_index ,image['W_Sword005.png'])
Sword6 = Weapon(15,8,6,"ONE_HANDED",item_index ,image['W_Sword006.png'])
Sword7  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword007.png'])
Sword8  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword008.png'] )
Sword9  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword009.png'] )
Sword10  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword010.png'] )
Sword11  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword011.png'] )
Sword12  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword012.png'] )
Sword13  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword013.png'] )
Sword14  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword014.png'] )
Sword15  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword015.png'] )
Sword16  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword016.png'] )
Sword17  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword017.png'] )
Sword18  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword018.png'] )
Sword19  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword019.png'] )
Sword20  = Weapon(15,8,6,"ONE_HANDED",item_index,image['W_Sword020.png'] )

    # SPEAR

Spear1 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear001.png'])
Spear2 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear002.png'])
Spear3 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear003.png'])
Spear4 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear004.png'])
Spear5 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear005.png'])
Spear6 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear006.png'])
Spear7 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear007.png'])
Spear8 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear008.png'])
Spear9 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear009.png'])
Spear10 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear010.png'])
Spear11 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear011.png'])
Spear12 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear012.png'])
Spear13 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear013.png'])
Spear14 = Weapon(2,6,6,"TWO_HANDED",item_index,image['W_Spear014.png'])

    # MACE

Mace1 = Weapon(1,1,1,"Mace",item_index,image['W_Mace001.png'])
Mace2 = Weapon(1,1,1,"Mace",item_index,image['W_Mace002.png'])
Mace3 = Weapon(1,1,1,"Mace",item_index,image['W_Mace003.png'])
Mace4 = Weapon(1,1,1,"Mace",item_index,image['W_Mace004.png'])
Mace5 = Weapon(1,1,1,"Mace",item_index,image['W_Mace005.png'])
Mace6 = Weapon(1,1,1,"Mace",item_index,image['W_Mace006.png'])
Mace7 = Weapon(1,1,1,"Mace",item_index,image['W_Mace007.png'])
Mace8 = Weapon(1,1,1,"Mace",item_index,image['W_Mace008.png'])
Mace9 = Weapon(1,1,1,"Mace",item_index,image['W_Mace009.png'])
Mace10 = Weapon(1,1,1,"Mace",item_index,image['W_Mace010.png'])
Mace11 = Weapon(1,1,1,"Mace",item_index,image['W_Mace011.png'])
Mace12 = Weapon(1,1,1,"Mace",item_index,image['W_Mace012.png'])
Mace13 = Weapon(1,1,1,"Mace",item_index,image['W_Mace013.png'])
Mace14 = Weapon(1,1,1,"Mace",item_index,image['W_Mace014.png'])

    # GUN

Gun1 = Weapon(1,1,1,"Gun",item_index,image['W_Gun001.png'])
Gun2 = Weapon(1,1,1,"Gun",item_index,image['W_Gun002.png'])
Gun3 = Weapon(1,1,1,"Gun",item_index,image['W_Gun003.png'])

    # FIST

Fist1 = Weapon(1,1,1,"Fist",item_index,image['W_Fist001.png'])
Fist2 = Weapon(1,1,1,"Fist",item_index,image['W_Fist002.png'])
Fist3 = Weapon(1,1,1,"Fist",item_index,image['W_Fist003.png'])
Fist4 = Weapon(1,1,1,"Fist",item_index,image['W_Fist004.png'])
Fist5 = Weapon(1,1,1,"Fist",item_index,image['W_Fist005.png'])

    # DAGGER

Dagger1 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger001.png'])
Dagger2 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger002.png'])
Dagger3 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger003.png'])
Dagger4 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger004.png'])
Dagger5 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger005.png'])
Dagger6 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger006.png'])
Dagger7 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger007.png'])
Dagger8 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger008.png'])
Dagger9 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger009.png'])
Dagger10 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger010.png'])
Dagger11 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger011.png'])
Dagger12 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger012.png'])
Dagger13 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger013.png'])
Dagger14 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger014.png'])
Dagger15 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger015.png'])
Dagger16 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger016.png'])
Dagger17 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger017.png'])
Dagger18 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger018.png'])
Dagger19 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger019.png'])
Dagger20 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger020.png'])
Dagger21 = Weapon(1,1,1,"Dagger",item_index,image['W_Dagger021.png'])

    # BOW

Bow1 = Weapon(1,1,1,"Bow",item_index,image['W_Bow01.png'])
Bow2 = Weapon(1,1,1,"Bow",item_index,image['W_Bow02.png'])
Bow3 = Weapon(1,1,1,"Bow",item_index,image['W_Bow03.png'])
Bow4 = Weapon(1,1,1,"Bow",item_index,image['W_Bow04.png'])
Bow5 = Weapon(1,1,1,"Bow",item_index,image['W_Bow05.png'])
Bow6 = Weapon(1,1,1,"Bow",item_index,image['W_Bow06.png'])
Bow7 = Weapon(1,1,1,"Bow",item_index,image['W_Bow07.png'])
Bow8 = Weapon(1,1,1,"Bow",item_index,image['W_Bow08.png'])
Bow9 = Weapon(1,1,1,"Bow",item_index,image['W_Bow09.png'])
Bow10 = Weapon(1,1,1,"Bow",item_index,image['W_Bow10.png'])
Bow11 = Weapon(1,1,1,"Bow",item_index,image['W_Bow11.png'])
Bow12 = Weapon(1,1,1,"Bow",item_index,image['W_Bow12.png'])
Bow13 = Weapon(1,1,1,"Bow",item_index,image['W_Bow13.png'])
Bow14 = Weapon(1,1,1,"Bow",item_index,image['W_Bow14.png'])

    # AXE

Axe1 = Weapon(1,1,1,"Axe",item_index,image['W_Axe001.png'])
Axe2 = Weapon(1,1,1,"Axe",item_index,image['W_Axe002.png'])
Axe3 = Weapon(1,1,1,"Axe",item_index,image['W_Axe003.png'])
Axe4 = Weapon(1,1,1,"Axe",item_index,image['W_Axe004.png'])
Axe5 = Weapon(1,1,1,"Axe",item_index,image['W_Axe005.png'])
Axe6 = Weapon(1,1,1,"Axe",item_index,image['W_Axe006.png'])
Axe7 = Weapon(1,1,1,"Axe",item_index,image['W_Axe007.png'])
Axe8 = Weapon(1,1,1,"Axe",item_index,image['W_Axe008.png'])
Axe9 = Weapon(1,1,1,"Axe",item_index,image['W_Axe009.png'])
Axe10 = Weapon(1,1,1,"Axe",item_index,image['W_Axe010.png'])
Axe11 = Weapon(1,1,1,"Axe",item_index,image['W_Axe011.png'])
Axe12 = Weapon(1,1,1,"Axe",item_index,image['W_Axe012.png'])
Axe13 = Weapon(1,1,1,"Axe",item_index,image['W_Axe013.png'])
Axe14 = Weapon(1,1,1,"Axe",item_index,image['W_Axe014.png'])

# BOOK

Book1 = Items(1,1,item_index,"Book",image['W_Book01.png'])
Book2 = Items(1,1,item_index,"Book",image['W_Book02.png'])
Book3 = Items(1,1,item_index,"Book",image['W_Book03.png'])
Book4 = Items(1,1,item_index,"Book",image['W_Book04.png'])
Book5 = Items(1,1,item_index,"Book",image['W_Book05.png'])
Book6 = Items(1,1,item_index,"Book",image['W_Book06.png'])
Book7 = Items(1,1,item_index,"Book",image['W_Book07.png'])

# SORT 
    # WIND 
Wind1 = Consomable(1,1,item_index,"Wind",image['S_Wind01.png'])
Wind2 = Consomable(1,1,item_index,"Wind",image['S_Wind02.png'])
Wind3 = Consomable(1,1,item_index,"Wind",image['S_Wind03.png'])
Wind4 = Consomable(1,1,item_index,"Wind",image['S_Wind04.png'])
Wind5 = Consomable(1,1,item_index,"Wind",image['S_Wind05.png'])
Wind6 = Consomable(1,1,item_index,"Wind",image['S_Wind06.png'])
Wind7 = Consomable(1,1,item_index,"Wind",image['S_Wind07.png'])
    # WATER
Water1 = Consomable(1,1,item_index,"Wind",image['S_Water01.png'])
Water2 = Consomable(1,1,item_index,"Wind",image['S_Water02.png'])
Water3 = Consomable(1,1,item_index,"Wind",image['S_Water03.png'])
Water4 = Consomable(1,1,item_index,"Wind",image['S_Water04.png'])
Water5 = Consomable(1,1,item_index,"Wind",image['S_Water05.png'])
Water6 = Consomable(1,1,item_index,"Wind",image['S_Water06.png'])
Water7 = Consomable(1,1,item_index,"Wind",image['S_Water07.png'])
    # THUNDER
Thunder1 = Consomable(1,1,item_index,"Thunder",image['S_Thunder01.png'])
Thunder2 = Consomable(1,1,item_index,"Thunder",image['S_Thunder02.png'])
Thunder3 = Consomable(1,1,item_index,"Thunder",image['S_Thunder03.png'])
Thunder4 = Consomable(1,1,item_index,"Thunder",image['S_Thunder04.png'])
Thunder5 = Consomable(1,1,item_index,"Thunder",image['S_Thunder05.png'])
Thunder6 = Consomable(1,1,item_index,"Thunder",image['S_Thunder06.png'])
Thunder7 = Consomable(1,1,item_index,"Thunder",image['S_Thunder07.png'])
    # SWORD EFFECT
Sword_effect1 = Consomable(1,1,item_index,"Sort",image['S_Sword01.png'])
Sword_effect2 = Consomable(1,1,item_index,"Sort",image['S_Sword02.png'])
Sword_effect3 = Consomable(1,1,item_index,"Sort",image['S_Sword03.png'])
Sword_effect4 = Consomable(1,1,item_index,"Sort",image['S_Sword04.png'])
Sword_effect5 = Consomable(1,1,item_index,"Sort",image['S_Sword05.png'])
Sword_effect6 = Consomable(1,1,item_index,"Sort",image['S_Sword06.png'])
Sword_effect7 = Consomable(1,1,item_index,"Sort",image['S_Sword07.png'])
Sword_effect8 = Consomable(1,1,item_index,"Sort",image['S_Sword08.png'])
Sword_effect9 = Consomable(1,1,item_index,"Sort",image['S_Sword09.png'])
Sword_effect10 = Consomable(1,1,item_index,"Sort",image['S_Sword10.png'])
    # SHADOW
Shadow1 = Consomable(1,1,item_index,"Sort",image['S_Shadow01.png'])
Shadow2 = Consomable(1,1,item_index,"Sort",image['S_Shadow02.png'])
Shadow3 = Consomable(1,1,item_index,"Sort",image['S_Shadow03.png'])
Shadow4 = Consomable(1,1,item_index,"Sort",image['S_Shadow04.png'])
Shadow5 = Consomable(1,1,item_index,"Sort",image['S_Shadow05.png'])
Shadow6 = Consomable(1,1,item_index,"Sort",image['S_Shadow06.png'])
Shadow7 = Consomable(1,1,item_index,"Sort",image['S_Shadow07.png'])
    # POISON
Poison1 = Consomable(1,1,item_index,"Sort",image['S_Poison01.png'])
Poison2 = Consomable(1,1,item_index,"Sort",image['S_Poison02.png'])
Poison3 = Consomable(1,1,item_index,"Sort",image['S_Poison03.png'])
Poison4 = Consomable(1,1,item_index,"Sort",image['S_Poison04.png'])
Poison5 = Consomable(1,1,item_index,"Sort",image['S_Poison05.png'])
Poison6 = Consomable(1,1,item_index,"Sort",image['S_Poison06.png'])
Poison7 = Consomable(1,1,item_index,"Sort",image['S_Poison07.png'])
    # PHYSIC
Physic1 = Consomable(1,1,item_index,"Sort",image['S_Physic01.png'])
Physic2 = Consomable(1,1,item_index,"Sort",image['S_Physic02.png'])
    # MAGIC
Magic1 = Consomable(1,1,item_index,"Sort",image['S_Magic01.png'])
Magic2 = Consomable(1,1,item_index,"Sort",image['S_Magic02.png'])
Magic3 = Consomable(1,1,item_index,"Sort",image['S_Magic03.png'])
Magic4 = Consomable(1,1,item_index,"Sort",image['S_Magic04.png'])
    # LIGHT
Light1 = Consomable(1,1,item_index,"Sort",image['S_Light01.png'])
Light2 = Consomable(1,1,item_index,"Sort",image['S_Light02.png'])
Light3 = Consomable(1,1,item_index,"Sort",image['S_Light03.png'])
    # ICE
Ice1 = Consomable(1,1,item_index,"Sort",image['S_Ice01.png'])
Ice2 = Consomable(1,1,item_index,"Sort",image['S_Ice02.png'])
Ice3 = Consomable(1,1,item_index,"Sort",image['S_Ice03.png'])
Ice4 = Consomable(1,1,item_index,"Sort",image['S_Ice04.png'])
Ice5 = Consomable(1,1,item_index,"Sort",image['S_Ice05.png'])
Ice6 = Consomable(1,1,item_index,"Sort",image['S_Ice06.png'])
Ice7 = Consomable(1,1,item_index,"Sort",image['S_Ice07.png'])
    # HOLY
holy1 = Consomable(1,1,item_index,"Sort",image['S_Holy01.png'])
holy2 = Consomable(1,1,item_index,"Sort",image['S_Holy02.png'])
holy3 = Consomable(1,1,item_index,"Sort",image['S_Holy03.png'])
holy4 = Consomable(1,1,item_index,"Sort",image['S_Holy04.png'])
holy5 = Consomable(1,1,item_index,"Sort",image['S_Holy05.png'])
holy6 = Consomable(1,1,item_index,"Sort",image['S_Holy06.png'])
holy7 = Consomable(1,1,item_index,"Sort",image['S_Holy07.png'])
    # FIRE
fire1 = Consomable(1,1,item_index,"Sort",image['S_Fire01.png'])
fire2 = Consomable(1,1,item_index,"Sort",image['S_Fire02.png'])
fire3 = Consomable(1,1,item_index,"Sort",image['S_Fire03.png'])
fire4 = Consomable(1,1,item_index,"Sort",image['S_Fire04.png'])
fire5 = Consomable(1,1,item_index,"Sort",image['S_Fire05.png'])
fire6 = Consomable(1,1,item_index,"Sort",image['S_Fire06.png'])
fire7 = Consomable(1,1,item_index,"Sort",image['S_Fire07.png'])
    # EARTH
Earth1 = Consomable(1,1,item_index,"Sort",image['S_Earth01.png'])
Earth2 = Consomable(1,1,item_index,"Sort",image['S_Earth02.png'])
Earth3 = Consomable(1,1,item_index,"Sort",image['S_Earth03.png'])
Earth4 = Consomable(1,1,item_index,"Sort",image['S_Earth04.png'])
Earth5 = Consomable(1,1,item_index,"Sort",image['S_Earth05.png'])
Earth6 = Consomable(1,1,item_index,"Sort",image['S_Earth06.png'])
Earth7 = Consomable(1,1,item_index,"Sort",image['S_Earth07.png'])
    # DEATH
Death1 = Consomable(1,1,item_index,"Sort",image['S_Death01.png'])
Death2 = Consomable(1,1,item_index,"Sort",image['S_Death02.png'])
    # BUFF
Buff1 = Consomable(1,1,item_index,"Sort",image['S_Buff01.png'])
Buff2 = Consomable(1,1,item_index,"Sort",image['S_Buff02.png'])
Buff3 = Consomable(1,1,item_index,"Sort",image['S_Buff03.png'])
Buff4 = Consomable(1,1,item_index,"Sort",image['S_Buff04.png'])
Buff5 = Consomable(1,1,item_index,"Sort",image['S_Buff05.png'])
Buff6 = Consomable(1,1,item_index,"Sort",image['S_Buff06.png'])
Buff7 = Consomable(1,1,item_index,"Sort",image['S_Buff07.png'])
Buff8 = Consomable(1,1,item_index,"Sort",image['S_Buff08.png'])
Buff9 = Consomable(1,1,item_index,"Sort",image['S_Buff09.png'])
Buff10 = Consomable(1,1,item_index,"Sort",image['S_Buff10.png'])
Buff11 = Consomable(1,1,item_index,"Sort",image['S_Buff11.png'])
Buff12 = Consomable(1,1,item_index,"Sort",image['S_Buff12.png'])
Buff13 = Consomable(1,1,item_index,"Sort",image['S_Buff13.png'])
Buff14 = Consomable(1,1,item_index,"Sort",image['S_Buff14.png'])
    # BOW EFFECT
Bow_effect1 = Consomable(1,1,item_index,"Sort",image['S_Bow01.png'])
Bow_effect2 = Consomable(1,1,item_index,"Sort",image['S_Bow02.png'])
Bow_effect3 = Consomable(1,1,item_index,"Sort",image['S_Bow03.png'])
Bow_effect4 = Consomable(1,1,item_index,"Sort",image['S_Bow04.png'])
Bow_effect5 = Consomable(1,1,item_index,"Sort",image['S_Bow05.png'])
Bow_effect6 = Consomable(1,1,item_index,"Sort",image['S_Bow06.png'])
Bow_effect7 = Consomable(1,1,item_index,"Sort",image['S_Bow07.png'])
Bow_effect8 = Consomable(1,1,item_index,"Sort",image['S_Bow08.png'])
Bow_effect9 = Consomable(1,1,item_index,"Sort",image['S_Bow09.png'])
Bow_effect10 = Consomable(1,1,item_index,"Sort",image['S_Bow10.png'])
Bow_effect11 = Consomable(1,1,item_index,"Sort",image['S_Bow11.png'])
Bow_effect12 = Consomable(1,1,item_index,"Sort",image['S_Bow12.png'])
Bow_effect13 = Consomable(1,1,item_index,"Sort",image['S_Bow13.png'])
Bow_effect14 = Consomable(1,1,item_index,"Sort",image['S_Bow14.png'])

# POTION
    # YELLOW
P_Yellow1 = Consomable(1,1,item_index,"Potion",image['P_Yellow01.png'])
P_Yellow2 = Consomable(1,1,item_index,"Potion",image['P_Yellow02.png'])
P_Yellow3 = Consomable(1,1,item_index,"Potion",image['P_Yellow03.png'])
P_Yellow4 = Consomable(1,1,item_index,"Potion",image['P_Yellow04.png'])
    # WHITE
P_White1 = Consomable(1,1,item_index,"Potion",image['P_White01.png'])
P_White2 = Consomable(1,1,item_index,"Potion",image['P_White02.png'])
P_White3 = Consomable(1,1,item_index,"Potion",image['P_White03.png'])
P_White4 = Consomable(1,1,item_index,"Potion",image['P_White04.png'])
    # RED
P_Red1 = Consomable(1,1,item_index,"Potion",image['P_Red01.png'])
P_Red2 = Consomable(1,1,item_index,"Potion",image['P_Red02.png'])
P_Red3 = Consomable(1,1,item_index,"Potion",image['P_Red03.png'])
P_Red4 = Consomable(1,1,item_index,"Potion",image['P_Red04.png'])
    # PINK
P_Pink1 = Consomable(1,1,item_index,"Potion",image['P_Pink01.png'])
P_Pink2 = Consomable(1,1,item_index,"Potion",image['P_Pink02.png'])
P_Pink3 = Consomable(1,1,item_index,"Potion",image['P_Pink03.png'])
P_Pink4 = Consomable(1,1,item_index,"Potion",image['P_Pink04.png'])
    # ORANGE
P_Orange1 = Consomable(1,1,item_index,"Potion",image['P_Orange01.png'])
P_Orange2 = Consomable(1,1,item_index,"Potion",image['P_Orange02.png'])
P_Orange3 = Consomable(1,1,item_index,"Potion",image['P_Orange03.png'])
P_Orange4 = Consomable(1,1,item_index,"Potion",image['P_Orange04.png'])
    # GREEN
P_Green1 = Consomable(1,1,item_index,"Potion",image['P_Green01.png'])
P_Green2 = Consomable(1,1,item_index,"Potion",image['P_Green02.png'])
P_Green3 = Consomable(1,1,item_index,"Potion",image['P_Green03.png'])
P_Green4 = Consomable(1,1,item_index,"Potion",image['P_Green04.png'])
    # BLUE
P_Blue1 = Consomable(1,1,item_index,"Potion",image['P_Blue01.png'])
P_Blue2 = Consomable(1,1,item_index,"Potion",image['P_Blue02.png'])
P_Blue3 = Consomable(1,1,item_index,"Potion",image['P_Blue03.png'])
P_Blue4 = Consomable(1,1,item_index,"Potion",image['P_Blue04.png'])
    # MEDECINE
P_Medecine1 = Consomable(1,1,item_index,"Potion",image['P_Medicine01.png'])
P_Medecine2 = Consomable(1,1,item_index,"Potion",image['P_Medicine02.png'])
P_Medecine3 = Consomable(1,1,item_index,"Potion",image['P_Medicine03.png'])
P_Medecine4 = Consomable(1,1,item_index,"Potion",image['P_Medicine04.png'])
P_Medecine1 = Consomable(1,1,item_index,"Potion",image['P_Medicine05.png'])
P_Medecine2 = Consomable(1,1,item_index,"Potion",image['P_Medicine06.png'])
P_Medecine3 = Consomable(1,1,item_index,"Potion",image['P_Medicine07.png'])
P_Medecine4 = Consomable(1,1,item_index,"Potion",image['P_Medicine08.png'])
P_Medecine1 = Consomable(1,1,item_index,"Potion",image['P_Medicine09.png'])

# DROPABLE

Wolfur = Items(1,1,item_index,"Drop",image['I_WolfFur.png'])
Water = Items(1,1,item_index,"Drop",image['I_Water.png'])
Torch1 = Items(1,1,item_index,"Drop",image['I_Torch01.png'])
Torch2 = Items(1,1,item_index,"Drop",image['I_Torch02.png'])
Tentacle = Items(1,1,item_index,"Drop",image['I_Tentacle.png'])
Telescope = Items(1,1,item_index,"Drop",image['I_Telescope.png'])
SolidShell = Items(1,1,item_index,"Drop",image['I_SolidShell.png'])
SnailShell = Items(1,1,item_index,"Drop",image['I_SnailShell.png'])
SilverCoin = Items(1,1,item_index,"Drop",image['I_SilverCoin.png'])
SilverBar = Items(1,1,item_index,"Drop",image['I_SilverBar.png'])
Scroll = Items(1,1,item_index,"Drop",image['I_Scroll.png'])
Scroll2 = Items(1,1,item_index,"Drop",image['I_Scroll02.png'])
ScorpionClaw = Items(1,1,item_index,"Drop",image['I_ScorpionClaw.png'])
Saphire = Items(1,1,item_index,"Drop",image['I_Saphire.png'])
Rubi = Items(1,1,item_index,"Drop",image['I_Rubi.png'])
Rock1 = Items(1,1,item_index,"Drop",image['I_Rock01.png'])
Rock2 = Items(1,1,item_index,"Drop",image['I_Rock02.png'])
Rock3 = Items(1,1,item_index,"Drop",image['I_Rock03.png']) 
Rock4 = Items(1,1,item_index,"Drop",image['I_Rock04.png'])
Rock5 = Items(1,1,item_index,"Drop",image['I_Rock05.png'])
Opal = Items(1,1,item_index,"Drop",image['I_Opal.png'])
Mirror = Items(1,1,item_index,"Drop",image['I_Mirror.png'])
Map = Items(1,1,item_index,"Drop",image['I_Map.png'])
Leaf = Items(1,1,item_index,"Drop",image['I_Leaf.png'])
Key1 = Items(1,1,item_index,"Drop",image['I_Key01.png'])
Key2 = Items(1,1,item_index,"Drop",image['I_Key02.png'])
Key3 = Items(1,1,item_index,"Drop",image['I_Key03.png'])
Key4 = Items(1,1,item_index,"Drop",image['I_Key04.png'])
Key5 = Items(1,1,item_index,"Drop",image['I_Key05.png'])
Key6 = Items(1,1,item_index,"Drop",image['I_Key06.png'])
Key7 = Items(1,1,item_index,"Drop",image['I_Key07.png'])
Jade = Items(1,1,item_index,"Drop",image['I_Jade.png'])
IronBall = Items(1,1,item_index,"Drop",image['I_IronBall.png'])
Ink = Items(1,1,item_index,"Drop",image['I_Ink.png'])
GoldCoin = Items(1,1,item_index,"Drop",image['I_GoldCoin.png'])
GoldBar = Items(1,1,item_index,"Drop",image['I_GoldBar.png'])
FrogLeg = Items(1,1,item_index,"Drop",image['I_FrogLeg.png'])
FoxTail = Items(1,1,item_index,"Drop",image['I_FoxTail.png'])
FishTail = Items(1,1,item_index,"Drop",image['I_FishTail.png'])
Feather1 = Items(1,1,item_index,"Drop",image['I_Feather01.png'])
Feather2 = Items(1,1,item_index,"Drop",image['I_Feather02.png'])
Fang = Items(1,1,item_index,"Drop",image['I_Fang.png'])
Fabric = Items(1,1,item_index,"Drop",image['I_Fabric.png'])
Eye = Items(1,1,item_index,"Drop",image['I_Eye.png'])
Diamond = Items(1,1,item_index,"Drop",image['I_Diamond.png'])
Crystal1 = Items(1,1,item_index,"Drop",image['I_Crystal01.png'])
Crystal2 = Items(1,1,item_index,"Drop",image['I_Crystal02.png'])
Crystal3= Items(1,1,item_index,"Drop",image['I_Crystal03.png'])
Coal = Items(1,1,item_index,"Drop",image['I_Coal.png'])
Chest1= Items(1,1,item_index,"Drop",image['I_Chest01.png'])
Chest2= Items(1,1,item_index,"Drop",image['I_Chest02.png'])
Cannon1= Items(1,1,item_index,"Drop",image['I_Cannon01.png'])
Cannon2= Items(1,1,item_index,"Drop",image['I_Cannon02.png'])
Cannon3= Items(1,1,item_index,"Drop",image['I_Cannon03.png'])
Cannon4= Items(1,1,item_index,"Drop",image['I_Cannon04.png'])
Cannon5= Items(1,1,item_index,"Drop",image['I_Cannon05.png'])

# BOUFFE
I_C_YellowPepper = Consomable(1,1,item_index,"FOOD",image['I_C_YellowPepper.png'])
Watermellon = Consomable(1,1,item_index,"FOOD",image['I_C_Watermellon.png'])
Strawberry = Consomable(1,1,item_index,"FOOD",image['I_C_Strawberry.png'])
RedPepper = Consomable(1,1,item_index,"FOOD",image['I_C_RedPepper.png'])
RawMeat = Consomable(1,1,item_index,"FOOD",image['I_C_RawMeat.png'])
RawFish = Consomable(1,1,item_index,"FOOD",image['I_C_RawFish.png'])
Radish= Consomable(1,1,item_index,"FOOD",image['I_C_Radish.png'])
Pineapple= Consomable(1,1,item_index,"FOOD",image['I_C_Pineapple.png'])
Pie= Consomable(1,1,item_index,"FOOD",image['I_C_Pie.png'])
Pear = Consomable(1,1,item_index,"FOOD",image['I_C_Pear.png'])
Orange = Consomable(1,1,item_index,"FOOD",image['I_C_Orange.png'])
Nut= Consomable(1,1,item_index,"FOOD",image['I_C_Nut.png'])
Mushroom= Consomable(1,1,item_index,"FOOD",image['I_C_Mushroom.png'])
Mulberry= Consomable(1,1,item_index,"FOOD",image['I_C_Mulberry.png'])
Meat= Consomable(1,1,item_index,"FOOD",image['I_C_Meat.png'])
Lemon= Consomable(1,1,item_index,"FOOD",image['I_C_Lemon.png'])
GreenPepper= Consomable(1,1,item_index,"FOOD",image['I_C_GreenPepper.png'])
GreenGrapes= Consomable(1,1,item_index,"FOOD",image['I_C_GreenGrapes.png'])
Grapes = Consomable(1,1,item_index,"FOOD",image['I_C_Grapes.png'])
Fish = Consomable(1,1,item_index,"FOOD",image['I_C_Fish.png'])
Cherry= Consomable(1,1,item_index,"FOOD",image['I_C_Cherry.png'])
Cheese= Consomable(1,1,item_index,"FOOD",image['I_C_Cheese.png'])
Carrot= Consomable(1,1,item_index,"FOOD",image['I_C_Carrot.png'])
Bread= Consomable(1,1,item_index,"FOOD",image['I_C_Bread.png'])
Banana= Consomable(1,1,item_index,"FOOD",image['I_C_Banana.png'])

# OTHER
I_BronzeCoin = Items(1,1,item_index,"Other",image['I_BronzeCoin.png'])
BronzeBar = Items(1,1,item_index,"Other",image['I_BronzeBar.png'])
Bottle1= Items(1,1,item_index,"Other",image['I_Bottle01.png'])
Bottle2= Items(1,1,item_index,"Other",image['I_Bottle02.png'])
Bottle3= Items(1,1,item_index,"Other",image['I_Bottle03.png'])
Bottle4= Items(1,1,item_index,"Other",image['I_Bottle04.png'])
Book = Items(1,1,item_index,"Other",image['I_Book.png'])
Bone = Items(1,1,item_index,"Other",image['I_Bone.png'])
BirdsBeak= Items(1,1,item_index,"Other",image['I_BirdsBeak.png'])
BatWing= Items(1,1,item_index,"Other",image['I_BatWing.png'])
Antidote= Items(1,1,item_index,"Other",image['I_Antidote.png'])
Amethist= Items(1,1,item_index,"Other",image['I_Amethist.png'])
Agate= Items(1,1,item_index,"Other",image['I_Agate.png'])

# SHIELD : INDEX -> 5
item_index = 5

    # WOOD
E_Wood01  = Armor(1,1,1,"Chestplate",item_index,image['E_Wood01.png'])
E_Wood02  = Armor(1,1,1,"Chestplate",item_index,image['E_Wood02.png'])
E_Wood03  = Armor(1,1,1,"Chestplate",item_index,image['E_Wood03.png'])
E_Wood04  = Armor(1,1,1,"Chestplate",item_index,image['E_Wood04.png'])
    # METAL
E_Metal01  = Armor(1,1,1,"Chestplate",item_index,image['E_Metal01.png'])
E_Metal02  = Armor(1,1,1,"Chestplate",item_index,image['E_Metal02.png'])
E_Metal03  = Armor(1,1,1,"Chestplate",item_index,image['E_Metal03.png'])
E_Metal04  = Armor(1,1,1,"Chestplate",item_index,image['E_Metal04.png'])
E_Metal05  = Armor(1,1,1,"Chestplate",item_index,image['E_Metal05.png'])
    # GOLD
E_Gold01  = Armor(1,1,1,"Chestplate",item_index,image['E_Gold01.png'])
E_Gold02  = Armor(1,1,1,"Chestplate",item_index,image['E_Gold02.png'])
    # OS
E_Bones02  = Armor(1,1,1,"Chestplate",item_index,image['E_Bones02.png'])
E_Bones03  = Armor(1,1,1,"Chestplate",item_index,image['E_Bones03.png'])

# C_Helm : Casque -> INDEX 0
item_index = 0

C_Hat01  = Armor(1,1,1,"Chestplate",item_index,image['C_Hat01.png'] )
C_Hat01  = Armor(1,1,1,"Chestplate",item_index,image['C_Hat02.png'] )
C_Elm01  = Armor(1,1,1,"Chestplate",item_index,image['C_Elm01.png'] )
C_Elm03  = Armor(1,1,1,"Chestplate",item_index,image['C_Elm03.png'] )
C_Elm04  = Armor(1,1,1,"Chestplate",item_index,image['C_Elm04.png'] )

# Ac_Necklace : COUE -> INDEX 2
item_index = 2

Ac_Ring04  = Armor(1,1,1,"Chestplates",item_index,image['Ac_Ring04.png'] )
Ac_Necklace01  = Armor(1,1,1,"Chestplates",item_index,image['Ac_Necklace01.png'] )
Ac_Necklace02  = Armor(1,1,1,"Chestplates",item_index,image['Ac_Necklace02.png'] )
Ac_Necklace03  = Armor(1,1,1,"Chestplates",item_index,image['Ac_Necklace03.png'] )
Ac_Necklace04  = Armor(1,1,1,"Chestplates",item_index,image['Ac_Necklace04.png'] )

Ac_Medal1 = Armor(1,1,1,"Chestplates",item_index,image['Ac_Medal01.png'] )
Ac_Medal2 = Armor(1,1,1,"Chestplates",item_index,image['Ac_Medal02.png'] )
Ac_Medal3 = Armor(1,1,1,"Chestplates",item_index,image['Ac_Medal03.png'] )
Ac_Medal4 = Armor(1,1,1,"Chestplates",item_index,image['Ac_Medal04.png'] )

# A_Shoes : BOTTE -> INDEX 3 
item_index = 3

A_Shoes01  = Armor(1,1,1,"Chestplate",item_index,image['A_Shoes01.png'] )
A_Shoes02  = Armor(1,1,1,"Chestplate",item_index,image['A_Shoes02.png'] )
A_Shoes03  = Armor(1,1,1,"Chestplate",item_index,image['A_Shoes03.png'] )
A_Shoes04  = Armor(1,1,1,"Chestplate",item_index,image['A_Shoes04.png'] )
A_Shoes05  = Armor(1,1,1,"Chestplate",item_index,image['A_Shoes05.png'] )
A_Shoes06  = Armor(1,1,1,"Chestplate",item_index,image['A_Shoes06.png'] )
A_Shoes07  = Armor(1,1,1,"Chestplate",item_index,image['A_Shoes07.png'] )

# A_Armor : TORSE -> INDEX 1
item_index = 1

A_Armor04  = Armor(1,1,1,"Chestplate",item_index,image['A_Armor04.png'] )
A_Armor05  = Armor(1,1,1,"Chestplate",item_index,image['A_Armor05.png'] )
A_Armour01  = Armor(1,1,1,"Chestplate",item_index,image['A_Armour01.png'] )
A_Armour02  = Armor(1,1,1,"Chestplate",item_index,image['A_Armour02.png'] )
A_Armour03  = Armor(1,1,1,"Chestplate",item_index,image['A_Armour03.png'] )
A_Clothing01  = Armor(1,1,1,"Chestplate",item_index,image['A_Clothing01.png'] )
A_Clothing02  = Armor(1,1,1,"Chestplate",item_index,image['A_Clothing02.png'] )

#THROW SECTION

W_Throw001 = Weapon(1,1,1,"W_Throw",item_index,image['W_Throw001.png'])
W_Throw002 = Weapon(1,1,1,"W_Throw",item_index,image['W_Throw002.png'])
W_Throw003 = Weapon(1,1,1,"W_Throw",item_index,image['W_Throw003.png'])
W_Throw004 = Weapon(1,1,1,"W_Throw",item_index,image['W_Throw004.png'])
W_Throw05 = Weapon(1,1,1,"W_Throw",item_index,image['W_Throw05.png'])

