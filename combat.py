import pygame, os 
from settings.screen import *
from settings.police import *
from settings.load_img import *
from settings.color import *
from fonction import *
from case import *
from DiceEvent import *
from monstre import * #a remplacer plus tard
from personnage import *
from text import *
from settings.load_img import *
from script import list_mooving_entity,list_static_entity,entity_2

class Combat:

    def __init__(self,game,list_monstre):
        self.game = game
        self.texts = pygame.sprite.Group()####
        self.score = 0 #pour le dice
        self.diceevt = DiceEvent(self,self.game)
        self.pause = False
        self.tourm = True #cette valeur est a True si c'est le tour du monstre de jouer
        self.perso1 = Perso(13,0,14,0,0,0,0,100,100,0,name = "Perso 1")
        self.perso2 = Perso(8,0,15,0,0,0,0,100,100,0,name = "Perso 2")
        self.perso3 = Perso(18,0,16,0,0,0,0,100,100,0,name = "Perso 3") # a modifier quand on definit sur la map 3 joueurs
        self.stop = False #pour la generation du nombre aleatoire
        self.actdamage = False #pour activer le calcul des degats
        self.fincombat  = False
        self.liste_monstre = list_monstre ## a modifier 
        self.monstre = Monstre(18) #a remplacer plus tard
        self.angle = 0
        self.message_hp = "perso 1 hp:"+str(self.perso1.hp)+" perso 2 hp:"+str(self.perso2.hp)+" perso 3 hp:"+str(self.perso3.hp)
        self.player = self.game.player
        self.n_entrees = 0
        self.liste_tours = [] #liste de listes
        self.compteur_tour = 0 #pour faire le parcours des tours
        self.text="Score: "
        self.text_tour = "Tour: "
        self.message = Text(self,text="Generation des tours ...",size_font=30,pos=[image_box.get_width()+50,20],life_time=5000)
        self.texts.add(self.message)
        self.diceevt.all_dices.add(self.diceevt.dice)
        self.next_dice, self.next_text= False, False
        self.clic, self.bloc = False, False #pour les bouttons
        self.temps = pygame.time.get_ticks()
        self.message_final = Text(self,life_time = 0)

    def affichage(self):
        global n,list_case
        self.afficheoptions,self.first_Entry, self.activate, self.entered = False,True, False, False
        running = True
        click = True
        pixel_mask = pygame.mask.from_surface(pixel_red)
        souris_surf= pygame.Surface((1,1))
        souris_surf.fill(RED)
        souris_mask = pygame.mask.from_surface(souris_surf)
        pixel_red.set_alpha(0)
        Map = [['a','a','a'],['a','a','a']]
        case.set_colorkey(WHITE)
        display = pygame.Surface((screen.get_width(),screen.get_height()))
        display.set_colorkey(BLACK)
        l=load_map('map2.txt')
        case_select.set_alpha(100)
        list_case = []
        transition = pygame.Surface((screen.get_width(),screen.get_height()))
        transition.fill((0,0,0))
        f=0
        current_selec = None
        i,j= 0,0

        for h in l:
            j=0
            for g in h:
                if l[i][j] == 'w':
                    list_case.append(Case(i,j))
                j +=1
            i+=1
        i=0
        for x in self.liste_monstre:
            list_case[i].in_case = x
            i+=1
        self.game.player.transform_display_for_combat()
        list_case[59].in_case = self.game.player

        #VOIR TOUT LES MONSTRES
        list_case[0].in_case = list_mooving_entity[0]
        list_case[1].in_case = list_mooving_entity[1]
        list_case[2].in_case = list_mooving_entity[2]
        list_case[3].in_case = list_mooving_entity[3]
        list_case[4].in_case = list_mooving_entity[4]

        while running:
            self.angle += 10


            for text in self.texts:
                text.update()
            for dice in self.diceevt.all_dices:
                dice.update()

            mx,my = pygame.mouse.get_pos()
            screen.fill(LIGHT_GREY)
            screen.blit(fond,(0,0))
            screen.blit(souris_surf,(mx,my))
            i=0
            
            for x in list_case:
                screen.blit(x.display,x.cordo())
                if x.in_case != None and not x.is_select:
                    x.in_case.type_animation = "idle"
                if x.in_case != None and x.is_select:
                    x.in_case.type_animation = "idle"  ###attack
                if x.in_case != None:
                    x.in_case.animate()
            
            for x in list_case:
                x.checkIfSelected()
                
            for x in list_case:
                x.print_contains()
            i,j= 0,0
            for h in l:
                j=0
                for g in h:
                    if l[i][j] =='w':
                        if pixel_mask.overlap(souris_mask,((mx-((j-i)*(pixel_red.get_width()+45)//2+screen.get_width()//2-pixel_red.get_width()//2),my-((j+i)*(pixel_red.get_width()+45)//4-100)))):
                            if self.game.click:
                                for x in list_case:
                                    if x.i == i and x.j == j:
                                        if current_selec != None and current_selec.in_case != None:
                                            if x.is_select and x.in_case == None:
                                                x.in_case = current_selec.in_case 
                                                current_selec.in_case = None
                                        current_selec = x
                                        
                                    
                    j +=1
                i+=1

            screen.blit(image_box,(850,0))  
            for text in self.texts:
                text.print_text() 

            for dice in self.diceevt.all_dices:
                if not self.pause:
                    dice.rotate(dice.image,self.angle,screen)
                    n = dice.numero
                else:
                    done = True #pour signaler que le de a termine de tourner

            self.bouton1_cliqué = creation_img_text_click(image_boutton,"Choose what to do",ColderWeather_small, WHITE, screen,click,300,50)
            #print("compteur tour: "+str(self.compteur_tour))
            
            if (self.bouton1_cliqué and pygame.mouse.get_pressed()[0] and not self.first_Entry and self.checkIfTourPerso(self.compteur_tour) and not self.bloc):
                self.clic = True
            elif (not self.first_Entry and not self.checkIfTourPerso(self.compteur_tour) and not self.entered):
                self.monstre_attack()

            myfont = pygame.font.SysFont('Comic Sans MS', 70)
            textsurface = myfont.render("{}".format(self.game.clock.get_fps()), False, (0, 0, 0))
            screen.blit(textsurface, (300, 500))
            if (self.clic):
                self.bouton2_cliqué = creation_img_text_click(image_boutton,"Attack",ColderWeather_small, WHITE, screen,click,300,150)
                self.bouton3_cliqué = creation_img_text_click(image_boutton,"Mouvement",ColderWeather_small, WHITE, screen,click,300,250)
                self.bouton4_cliqué = creation_img_text_click(image_boutton,"Bonus action",ColderWeather_small, WHITE, screen,click,300,350)
                self.bouton5_cliqué = creation_img_text_click(image_boutton,"Contre attack",ColderWeather_small, WHITE, screen,click,300,450)
                self.bouton6_cliqué = creation_img_text_click(image_boutton,"Nothing",ColderWeather_small, WHITE, screen,click,300,550)
                self.check_bouttons(self.bouton2_cliqué,self.bouton3_cliqué,self.bouton4_cliqué,self.bouton5_cliqué,self.bouton6_cliqué)
            

            #if not fin: #pour ne plus afficher le de une fois qu'il a terminé de tourner
            self.essai()

            if current_selec != None:
                current_selec.select(True)
                current_selec.select_neighbour(list_case)
            pygame.display.update()
            running,self.game.click = basic_checkevent(self.game.click)

            if f != 255:
                for x in range(255):
                    f+=0.008
                    transition.set_alpha(int(255-f))
                screen.blit(transition,(0,0))

            pygame.display.update()
            running, self.game.click = basic_checkevent(self.game.click)
            
            if (self.message_final.update() and self.activate):
                print("message final")
                self.entered = False
                self.compteur_tour += 1
                self.activate = False
                self.reset_compteur()

                list_case[59].is_select = False
                for i in range(5):
                    list_case[i].is_select = False

                if self.checkIfTourPerso(self.compteur_tour):
                    self.bloc = False #######################
            self.reset_compteur()
  

    def check_conditions(self):
        if self.n_entrees == 1:
            self.diceevt.resume(20,i=500)
            self.liste_tours.append([self.monstre.name, self.monstre.resultat,self.monstre])
            a = self.monstre.tour
            self.monstre.tour, self.perso1.tour = self.perso1.tour, a
        elif self.n_entrees == 2:
            self.diceevt.resume(20,i=500)
            self.liste_tours.append([self.perso1.name, self.perso1.resultat,self.perso1])
            a = self.perso1.tour
            self.perso1.tour, self.perso2.tour = self.perso2.tour, a
        elif self.n_entrees == 3:   
            self.diceevt.resume(20,i=500)
            self.liste_tours.append([self.perso2.name, self.perso2.resultat,self.perso2])
            a = self.perso2.tour
            self.perso2.tour, self.perso3.tour = self.perso3.tour, a
        else:
            if self.first_Entry:
                self.liste_tours.append([self.perso3.name, self.perso3.resultat,self.perso3])
                self.pause = True
                print(self.liste_tours)
                self.trier(self.liste_tours)
                print(self.liste_tours)
                for liste in self.liste_tours:
                    self.text_tour = self.text_tour + liste[0]+"\n"
                self.first_Entry = False
                self.message = Text(self,text=self.text,size_font=30,pos=[image_box.get_width(),20], life_time = 5000)
                print(self.message.spawn_time)
                self.message_tour = Text(self,text=self.text_tour,size_font=30,pos=[image_box.get_width(),50],life_time= 5000)
                self.texts.add(self.message,self.message_tour) #####
                self.next_text = False
     

    def degats(self):
        print("degatsssss")
        if (not self.checkIfTourPerso(self.compteur_tour)):
            self.diceevt.resume(self.monstre.n_de,i= 12000,birthday_time= 10000)
            self.message = Text(self,text="generation des degats...",size_font=30,pos=[image_box.get_width(),20], life_time = 13000, born = 10000)
            self.texts.add(self.message)
            self.next_dice = False
            self.diceevt.resultat_degats = generate_randint(1,self.monstre.n_de)
        #print("damage "+str(self.diceevt.resultat_degats))
            self.text,self.text_tour = "Score: "+str(self.diceevt.resultat_degats),""
        
        if (self.actdamage and not self.checkIfTourPerso(self.compteur_tour)):
            if self.perso1.hit:
                self.perso1.hp -= self.diceevt.resultat_degats
                self.perso1.hit = False
            if self.perso2.hit:
                self.perso2.hp -= self.diceevt.resultat_degats
                self.perso2.hit = False
            if self.perso3.hit:
                self.perso3.hp -= self.diceevt.resultat_degats
                self.perso3.hit = False
            self.actdamage = False ###
            self.text_tour += " Perso 1 hp="+str(self.perso1.hp)+" "+" Perso 2 hp="+str(self.perso2.hp)+" "+" Perso 3 hp="+str(self.perso3.hp)+" "
            self.message = Text(self,text=self.text,size_font=30,pos=[image_box.get_width(),20], life_time = 19000, born = 13000)
            self.message_tour = Text(self,text=self.text_tour,size_font=30,pos=[image_box.get_width(),50],life_time= 19000, born = 13000)
            print("dernier self.message "+str(self.message.spawn_time))
            self.texts.add(self.message,self.message_tour) #####

  

        if (self.next_dice and self.checkIfTourPerso(self.compteur_tour)):
                self.diceevt.resume(self.liste_tours[self.compteur_tour][2].n_de,i= 14000,birthday_time= 10000)
                self.message = Text(self,text="generation des degats...",size_font=30,pos=[image_box.get_width(),20], life_time = 14000, born = 10000)
                self.texts.add(self.message)
                self.diceevt.resultat_degats = generate_randint(1,self.liste_tours[self.compteur_tour][2].n_de) 
                self.text,self.text_tour = "Score: "+str(self.diceevt.resultat_degats),""  
        if (self.actdamage and self.checkIfTourPerso(self.compteur_tour)):
            if self.monstre.hit:
                self.monstre.hp -= self.diceevt.resultat_degats
                self.monstre.hit = False
                self.text_tour = "Monstre hp: "+str(self.monstre.hp)
            self.actdamage = False
            self.message = Text(self,text=self.text,size_font=30,pos=[image_box.get_width(),20], life_time = 18000, born = 14000)
            self.message_tour = Text(self,text=self.text_tour,size_font=30,pos=[image_box.get_width(),50],life_time= 18000, born = 14000)
            print("dernier self.message "+str(self.message.spawn_time))
            self.texts.add(self.message,self.message_tour) #####
        print(type(self.liste_tours[self.compteur_tour][2]))


    def essai(self): #fonction responsable de l'affichage du de
        if not self.fincombat:
            if self.monstre.tour:
                self.tour = "Monstre" 
            elif self.perso1.tour:
                self.tour = "Perso 1" 
            elif self.perso2.tour:
                self.tour = "Perso 2"
            elif self.perso3.tour:
                self.tour = "Perso 3"
    

            if self.stop: #pour generer un entier aleatoire quand le de finit de tourner
                self.n_entrees += 1 #represente le nbre d'entrees a cette boucle
                self.diceevt.resultat = generate_randint(1,n)
                if self.monstre.tour:
                    self.monstre.resultat = self.diceevt.resultat
                    #self.monstre.resultat = 20
                elif self.perso1.tour:
                    self.perso1.resultat = self.diceevt.resultat
                elif self.perso2.tour:
                    self.perso2.resultat = self.diceevt.resultat
                elif self.perso3.tour:
                    self.perso3.resultat = self.diceevt.resultat

                print("::"+str(self.diceevt.resultat))
                self.stop = False
                if self.first_Entry:
                    self.text = self.text + "\t"+self.tour+": "+str(self.diceevt.resultat) #self.message
                #draw_text(self.message, ColderWeather_small, WHITE,screen, 100, 800)
                self.check_conditions()

                print(self.perso1.hp, self.perso2.hp, self.perso3.hp)

    #trier la liste des resultats
    def trier(self,l):
        self.afficheoptions = True
        for j in range(len(l)):
            iMax=0
            i=0
            while i<len(l)-j:
                if l[i][1]<l[iMax][1]:
                    iMax=i
                i=i+1
            l[iMax],l[len(l)-1-j]=l[len(l)-j-1],l[iMax]

    def check_bouttons(self,b1,b2,b3,b4,b5): #ajouter une condition pour le click sur la map (qd les cases deviennent rouge)
        # if((b1 or b2 or b3 or b4 or b5) and pygame.mouse.get_pressed()[0]):
        #     print("OKKKKKKKKKK "+str(type(self.liste_tours[self.compteur_tour][2]) == Perso)+'b1 '+str(b1))
        #     self.clic = False #pour annuler l affichage de ces 5 bouttons
        #     self.attack()

        # if (b1 and pygame.mouse.get_pressed()[0] and (type(self.liste_tours[0][2]) == Perso)):
        if (b1 and pygame.mouse.get_pressed()[0]):
            print("attack")
            self.clic = False
            self.attack()
        elif (b2 and pygame.mouse.get_pressed()[0]):
            self.mouvement()
        elif (b3 and pygame.mouse.get_pressed()[0]):
            self.bonus_action()
        elif(b4 and pygame.mouse.get_pressed()[0]):
            self.contre_attack()
        elif(b5 and pygame.mouse.get_pressed()[0]):
            self.nothing()

    def checkIfTourPerso(self,i):
        return type(self.liste_tours[i][2]) == Perso
            
    def attack(self):
        global list_case
        self.bloc = True #######
        list_case[59].is_select=True
        print("attack")
        self.diceevt.resume(20,i=4000)
        self.diceevt.resultat = generate_randint(1,20)
        self.text = "Score du de: "+str(self.diceevt.resultat)+" et bonus DEX: "+str(bonus(self.liste_tours[self.compteur_tour][2].DEX)) + " Score: "+str(self.diceevt.resultat+bonus(self.liste_tours[self.compteur_tour][2].DEX))
        if self.diceevt.resultat + bonus(self.liste_tours[self.compteur_tour][2].DEX) >= self.monstre.ac:
            self.text_tour ="Monster hit"
            self.monstre.hit = True
            self.actdamage = True
            self.message_final = Text(self,text="",life_time=18000) 
        else:
            self.text_tour = "Monster missed"
            self.message_final = Text(self,text="",life_time=11000)
        self.message = Text(self,text=self.text,size_font=30,pos=[image_box.get_width(),20], life_time = 10000, born = 5000)
        self.message_tour = Text(self,text=self.text_tour,size_font=30,pos=[image_box.get_width(),50],life_time= 10000, born = 5000)
        self.texts.add(self.message,self.message_tour)

        if self.actdamage:
            print("in")
            self.degats()

        self.activate = True

    def mouvement(self):
        print("mouvement")

    def bonus_action(self):
        print("bonus action")

    def nothing(self):
        print("nothing")

    def contre_attack(self):
        print("contre attack")

    def monstre_attack(self):
        global list_case

        for i in range(5):
            list_case[i].is_select = True

        self.entered = True
        self.text_tour = "Tour des monstres:"
        # print("dice resultat "+str(self.diceevt.resultat_monstreatk))
        # print(str(self.perso1.hit)+str(self.perso2.hit)+str(self.perso3.hit))
        self.done_tourner = False

        print("entrer"+str(self.stop))
        self.next_dice = False
        self.diceevt.resume(20,i=7000,birthday_time=3000)
        self.perso1.hit, self.perso2.hit, self.perso3.hit = False, False, False
        self.diceevt.resultat_monstreatk = generate_randint(1,20)
        self.bloc = True
        self.text = "Score du dice= "+str(self.diceevt.resultat_monstreatk) +" et bonus dex = "+str(bonus(self.monstre.DEX))+"->Score =  "+str(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX))
        self.done_tourner = True
        print("resultat monstreatk "+str(self.diceevt.resultat_monstreatk))

        if(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX) < self.perso1.ac and self.done_tourner):
            self.text_tour += " Perso1 missed,"
        elif(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX) >= self.perso1.ac and self.done_tourner):
            self.text_tour += " Perso1 hit,"
            self.perso1.hit = True
            
        if(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX) < self.perso2.ac and self.done_tourner):
            self.text_tour += " Perso2 missed,"
        elif(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX) >= self.perso2.ac and self.done_tourner):
            self.text_tour += " Perso2 hit,"
            self.perso2.hit = True
            
        if(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX) < self.perso3.ac and self.done_tourner):
            self.text_tour += " Perso3 missed."
        elif(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX) >= self.perso3.ac and self.done_tourner):
            self.text_tour += " Perso3 hit."
            self.perso3.hit = True

        self.message = Text(self,text=self.text,size_font=30,pos=[image_box.get_width(),20], life_time = 10000, born = 5000)
        self.message_tour = Text(self,text=self.text_tour,size_font=30,pos=[image_box.get_width(),50],life_time= 10000, born = 5000)
        self.texts.add(self.message,self.message_tour) #####

        if ((self.perso1.hit or self.perso2.hit or self.perso3.hit) and self.done_tourner):
            self.actdamage = True
            self.message_final = Text(self,text='',life_time=20000)
            self.degats()
        elif(not(self.perso1.hit or self.perso2.hit or self.perso3.hit) and self.done_tourner):
            self.message_final = Text(self,text='',life_time=11000)

        print("self.message "+str(self.message.spawn_time))
        self.next_text = False
        self.activate = True


    def reset_compteur(self):
        if self.compteur_tour >= len(self.liste_tours):
            self.compteur_tour = 0
                        

#j ai ajoute un attribut ac au perso et un dex au monstre

