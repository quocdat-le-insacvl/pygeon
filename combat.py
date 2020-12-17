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
from settings.load_img import *
from script import list_mooving_entity,list_static_entity,entity_2

class Combat:

    def __init__(self,game,list_monstre):
        self.game = game
        self.score = 0 #pour le dice
        self.diceevt = DiceEvent(self,self.game)
        self.pause = False
        self.tourm = True #cette valeur est a True si c'est le tour du monstre de jouer
        self.perso1 = Perso(0,0,0,0,0,0,100,100,0,name = "Perso 1")
        self.perso2 = Perso(0,0,0,0,0,0,100,100,0,name = "Perso 2")
        self.perso3 = Perso(0,0,0,0,0,0,100,100,0,name = "Perso 3") # a modifier quand on definit sur la map 3 joueurs
        self.lancer = False #pr savoir si le de a ete lance
        self.stop = False #pour la generation du nombre aleatoire
        self.actdamage = False #pour activer le calcul des degats
        self.fincombat  = False
        self.liste_monstre = list_monstre ## a modifier 
        self.monstre = Monstre() #a remplacer plus tard
        self.angle = 0
        self.message = 'Score: '
        self.message_tour = 'Tour: '
        self.compteur = 0
        self.player = self.game.player
        self.n_entrees = 0
        self.liste_tours = [] #liste de listes

    def affichage(self):
        global afficheoptions, fin, clic, firstEntry
        global bouton2_cliqué, bouton3_cliqué, bouton4_cliqué, bouton5_cliqué, bouton6_cliqué
        afficheoptions, fin, clic, firstEntry = False, False, False, True
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
                    x.in_case.type_animation = "attack"
                if x.in_case != None:
                    x.in_case.animate()
                
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
    
            screen.blit(image_box,(700,100))
            draw_text(self.message_tour, ColderWeather_small,WHITE,screen,750,150 )
            draw_text(self.message, ColderWeather_small,WHITE,screen,750,120)
            
            bouton1_cliqué = creation_img_text_click(image_boutton,"Choose what to do",ColderWeather_small, WHITE, screen,click,300,150)
            if (bouton1_cliqué and pygame.mouse.get_pressed()[0] and not firstEntry):
                clic = True

        
            if clic:
                bouton2_cliqué = creation_img_text_click(image_boutton,"Attack",ColderWeather_small, WHITE, screen,click,300,250)
                bouton3_cliqué = creation_img_text_click(image_boutton,"Mouvement",ColderWeather_small, WHITE, screen,click,300,350)
                bouton4_cliqué = creation_img_text_click(image_boutton,"Bonus action",ColderWeather_small, WHITE, screen,click,300,450)
                bouton5_cliqué = creation_img_text_click(image_boutton,"Contre attack",ColderWeather_small, WHITE, screen,click,300,550)
                bouton6_cliqué = creation_img_text_click(image_boutton,"Nothing",ColderWeather_small, WHITE, screen,click,300,650)
                self.check_bouttons(bouton2_cliqué,bouton3_cliqué,bouton4_cliqué,bouton5_cliqué,bouton6_cliqué)
            

            if not fin: #pour ne plus afficher le de une fois qu'il a terminé de tourner
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

    def conditions(self):
        if not self.fincombat:
            #print(self.game.compteur)
            global n, resultat
            self.diceevt.load_dice()
            if self.diceevt.start:
                self.message = "Surprise Attack"
            self.diceevt.start = False 
            #cet attribut est pour afficher Surprise Attack uniquement a la premiere entree a la fonction 
            #vu que la fonction s'execute plusieurs fois
            done = False
            for dice in self.diceevt.all_dices:
                if not self.pause:
                    dice.rotate(dice.image,self.angle,screen)
                    self.diceevt.compter()
                    self.diceevt.check()
                    print(self.pause)
                    n = dice.numero
                
                else:
                    self.diceevt.pause()
                    self.diceevt.all_dices.draw(screen)
                    done = True #pour signaler que le de a termine de tourner

            if self.stop: #pour generer un entier aleatoire quand le de finit de tourner
                self.diceevt.resultat = generate_randint(1,n)
                print("::"+str(self.diceevt.resultat))
                self.stop = False
                print(self.diceevt.resultat+self.spider.stealth <self.player.ac, done, self.diceevt.actdamage, self.tourm)
            
            if ((self.diceevt.resultat  + self.spider.stealth < self.player.ac) and \
                done and not self.diceevt.actdamage and self.tourm):
                print("hi")
                self.message = "Monster: Miss."
                self.diceevt.damage = 0
        
            elif ((self.diceevt.resultat  + self.spider.stealth >= self.player.ac) and done \
                and self.tourm): ###
                self.message = "Hit. Generating damage..."
                self.diceevt.damage = 0
                for i in range(100): 
                    #pour laisser un temps entre l'affichage du premier resultat du de et le second
                    self.diceevt.pause()
                self.diceevt.resume(6)
                print(self.diceevt.dice.numero)
                self.diceevt.check()
            elif self.actdamage and self.tourm: # a changer 
                    self.diceevt.damage = self.diceevt.resultat
                    self.player.hp = self.player.hp - self.diceevt.damage #100
                    self.actdamage = False
                    self.message = "Your next step?"
                    #print("self.player.hp: "+str(self.player.hp))

            ##########################tour du joueur
            if((self.diceevt.resultat + self.player.dex < self.spider.ac) and done \
                and self.tourj and not self.diceevt.actdamage):
                self.message = "You missed."
                self.diceevt.damage = 0
                for i in range(200): 
                    #pour laisser un temps entre l'affichage du premier resultat du de et le second
                    self.diceevt.pause()
                self.tourm, self.tourj = True, False
                self.diceevt.resume(20)
                self.diceevt.check()

            elif((self.diceevt.resultat + self.player.dex >= self.spider.ac) and done \
                and self.tourj and not self.diceevt.actdamage): ##modifier la condition
                self.message = "You hitted the monster.Generating damage..."
                for i in range(100): 
                    #pour laisser un temps entre l'affichage du premier resultat du de et le second
                    self.diceevt.pause()
                self.diceevt.resume(6)
                self.diceevt.check()

            elif self.actdamage and self.tourj: # a changer 
                    self.diceevt.damage = self.diceevt.resultat
                    self.spider.hp = self.spider.hp - self.diceevt.damage #100
                    self.actdamage = False
                    self.diceevt.actdamage = False
                    if self.spider.hp <= 0:
                        self.objects.remove(self.spider)
                        self.message = "Monster beaten"
                        self.fincombat = True
                    else:
                        self.tourm, self.tourj = True, False
                        self.message = "-"
                        for i in range(100): 
                        #pour laisser un temps entre l'affichage du premier resultat du de et le second
                            self.diceevt.pause()
                        self.diceevt.resume(20)
                        self.diceevt.check()
                    print("Spider hp: "+str(self.spider.hp))

    def check_conditions(self):
        global firstEntry
        if self.n_entrees == 1:
            self.diceevt.resume(20)
            self.liste_tours.append([self.monstre.name, self.monstre.resultat])
            a = self.tourm
            self.monstre.tour, self.perso1.tour = self.perso1.tour, a
            self.essai()
        elif self.n_entrees == 2:
            self.diceevt.resume(20)
            self.liste_tours.append([self.perso1.name, self.perso1.resultat])
            a = self.perso1.tour
            self.perso1.tour, self.perso2.tour = self.perso2.tour, a
            self.essai()
        elif self.n_entrees == 3:
            self.diceevt.resume(20)
            self.liste_tours.append([self.perso2.name, self.perso2.resultat])
            a = self.perso2.tour
            self.perso2.tour, self.perso3.tour = self.perso3.tour, a
            self.essai()
        else:
            if firstEntry:
                self.liste_tours.append([self.perso3.name, self.perso3.resultat])
                self.pause = True
                print(self.liste_tours)
                self.trier(self.liste_tours)
                print(self.liste_tours)
                for liste in self.liste_tours:
                    self.message_tour = self.message_tour + liste[0]+"\n"
                firstEntry = False


    def essai(self): #fonction responsable de l'affichage du de
        global done
        if not self.fincombat:
            global n
            self.diceevt.load_dice()
            if self.monstre.tour:
                self.tour = "Monstre" 
            elif self.perso1.tour:
                self.tour = "Perso 1" 
            elif self.perso2.tour:
                self.tour = "Perso 2"
            elif self.perso3.tour:
                self.tour = "Perso 3"
    
            for dice in self.diceevt.all_dices:
                if not self.pause:
                    dice.rotate(dice.image,self.angle,screen)
                    self.diceevt.compter()
                    self.diceevt.check()
                    n = dice.numero
                else:
                    done = True #pour signaler que le de a termine de tourner

            if self.stop: #pour generer un entier aleatoire quand le de finit de tourner
                self.n_entrees += 1 #represente le nbre d'entrees a cette boucle
                self.diceevt.resultat = generate_randint(1,n)
                if self.monstre.tour:
                    self.monstre.resultat = self.diceevt.resultat
                elif self.perso1.tour:
                    self.perso1.resultat = self.diceevt.resultat
                elif self.perso2.tour:
                    self.perso2.resultat = self.diceevt.resultat
                elif self.perso3.tour:
                    self.perso3.tour = self.diceevt.resultat

                print("::"+str(self.diceevt.resultat))
                self.stop = False
                self.message = self.message + "\t"+self.tour+": "+str(self.diceevt.resultat)
                #draw_text(self.message, ColderWeather_small, WHITE,screen, 100, 800)
                self.check_conditions()

    #trier la liste des resultats
    def trier(self,l):
        global afficheoptions
        afficheoptions = True
        for j in range(len(l)):
            iMax=0
            i=0
            while i<len(l)-j:
                if l[i][1]<l[iMax][1]:
                    iMax=i
                i=i+1
            l[iMax],l[len(l)-1-j]=l[len(l)-j-1],l[iMax]

    def check_bouttons(self,b1,b2,b3,b4,b5): #ajouter une condition pour le click sur la map (qd les cases deviennent rouge)
        global clic
        if ((b1 or b2 or b3 or b4 or b5) and pygame.mouse.get_pressed()[0]):
            clic = False
        if (b1 and pygame.mouse.get_pressed()[0]):
            clic = False
            self.attack()
        elif (b2 and pygame.mouse.get_pressed()[0]):
            self.mouvement()
        elif (b3 and pygame.mouse.get_pressed()[0]):
            self.bonus_action()
        elif(b4 and pygame.mouse.get_pressed()[0]):
            self.contre_attack()
        elif(b5 and pygame.mouse.get_pressed()[0]):
            self.nothing()
            
    def attack(self):
        global fin
        fin = False
        self.message, self.message_tour = '',''
        self.diceevt.resume(20)
        print("attack")

    def mouvement(self):
        print("mouvement")

    def bonus_action(self):
        print("bonus action")

    def nothing(self):
        print("nothing")

    def contre_attack(self):
        print("contre attack")