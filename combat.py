import pygame
import os
from settings.screen import *
from settings.police import *
from settings.load_img import *
from settings.color import *
from fonction import *
from case import *
from DiceEvent import *
from monstre import *  # a remplacer plus tard
from personnage import *
from text import *
from settings.load_img import *
from script import list_mooving_entity, list_static_entity

# Message pour Christine: 
#   Pour print sur le log: 
# self.chat_box.write_log(("combat", "You play an attack!"))
# gardes le mot "combat", change le message ("You play an attack")
# Il faut que l'argument soit un tuple

class Combat:

    def __init__(self, game, list_monstre):
        self.game = game
        self.chat_box = self.game.chat_box
        self.texts = pygame.sprite.Group()
        self.score = 0  # pour le dice
        self.diceevt = DiceEvent(self, self.game)
        self.pause = False
        self.tourm = True  # cette valeur est a True si c'est le tour du monstre de jouer
        self.perso1 = Perso( name="Perso 1")
        self.perso2 = Perso(name="Perso 2")
        # a modifier quand on definit sur la map 3 joueurs
        self.perso3 = Perso(name="Perso 3")
        self.stop = False  # pour la generation du nombre aleatoire
        self.actdamage = False  # pour activer le calcul des degats
        self.fincombat = False
        self.liste_monstre = list_monstre  # a modifier
        self.monstre = Monstre(18)  # a remplacer plus tard
        self.angle = 0
        self.message_hp = "perso 1 hp:" + \
            str(self.perso1.hp)+" perso 2 hp:"+str(self.perso2.hp) + \
            " perso 3 hp:"+str(self.perso3.hp)
        self.player = self.game.player
        self.n_entrees = 0
        self.liste_tours = []  # liste de listes
        # pour faire le parcours des tours
        self.compteur_tour, self.compteur_mouvement = 0, 0
        self.text = "Score: "
        self.text_tour = "Tour: "
        self.message = Text(self, text="Generation des tours ...", size_font=30, pos=[
                            image_box.get_width()+50, 20], life_time=5000)
        self.texts.add(self.message)
        self.diceevt.all_dices.add(self.diceevt.dice)
        self.next_dice, self.next_text, self.player_mvt, self.player_nbmvt = False, False, False, False
        self.clic, self.bloc = False, False  # pour les bouttons
        self.temps = pygame.time.get_ticks()
        self.message_final = Text(self, life_time=0)
        self.player.nbre_direct = 0
        self.get_num = False

    def affichage(self):
        global n, list_case
        self.afficheoptions, self.first_Entry, self.activate, self.entered = False, True, False, False
        running = True
        click = True
        pixel_mask = pygame.mask.from_surface(pixel_red)
        souris_surf = pygame.Surface((1, 1))
        souris_surf.fill(RED)
        souris_surf.set_colorkey(BLACK)

        souris_mask = pygame.mask.from_surface(souris_surf)
        # pixel_red.set_alpha(0)
        pixel_red.set_colorkey(BLACK)
        Map = [['a', 'a', 'a'], ['a', 'a', 'a']]
        case.set_colorkey(WHITE)
        display = pygame.Surface((screen.get_width(), screen.get_height()))
        display.set_colorkey(BLACK)
        l = load_map('map2.txt')
        # case_select.set_alpha(100)
        list_case = []
        transition = pygame.Surface((screen.get_width(), screen.get_height()))
        transition.set_colorkey(BLACK)
        transition.fill((0, 0, 0))
        f = 0
        current_selec = None
        i, j = 0, 0

        for h in l:
            j = 0
            for g in h:
                if l[i][j] == 'w':
                    list_case.append(Case(i, j))
                j += 1
            i += 1
        i = 0
        for x in self.liste_monstre:
            list_case[i].in_case = x
            i += 1
        #self.game.player.transform_display_for_combat()
        list_case[self.game.player.n_case].in_case = self.game.player
        list_case[65].in_case = self.game.player.crew_mate[0]
        list_case[51].in_case = self.game.player.crew_mate[1]

        while running:
            
            self.angle += 10

            for text in self.texts:
                text.update()
            for dice in self.diceevt.all_dices:
                dice.update()

            mx, my = pygame.mouse.get_pos()
            screen.fill(BLACK)
            screen.blit(fond, (0, 0))
            screen.blit(souris_surf, (mx, my))
            i = 0

            for x in list_case:
                screen.blit(x.display, x.cordo())
                if x.in_case != None :
                    x.in_case.type_animation = "idle"
                if x.in_case != None and x.is_select:
                    x.in_case.type_animation = "idle"  # attack
                if x.in_case != None:
                    x.in_case.animate()
            """
            for x in list_case:
                x.checkIfSelected()"""

            
            
            i, j = 0, 0
            for h in l:
                j = 0
                for g in h:
                    if l[i][j] == 'w':
                        if pixel_mask.overlap(souris_mask, ((mx-((j-i)*(pixel_red.get_width()+45)//2+screen.get_width()//2-pixel_red.get_width()//2), my-((j+i)*(pixel_red.get_width()+45)//4-100)))):
                            if self.game.click:
                                for x in list_case:
                                    if x.i == i and x.j == j:
                                        if current_selec != None and current_selec.in_case != None:
                                            if x.is_select and x.in_case == None:
                                                x.in_case = current_selec.in_case
                                                current_selec.in_case = None
                                        current_selec = x

                    j += 1
                i += 1
            
            screen.blit(image_box, (850, 0))
            for text in self.texts:
                text.print_text()

            for dice in self.diceevt.all_dices:
                if not self.pause:
                    dice.rotate(dice.image, self.angle, screen)
                    n = dice.numero
                else:
                    done = True  # pour signaler que le de a termine de tourner

            bouton1_cliqué = creation_img_text_click(
                image_boutton, "Choose what to do", ColderWeather_small, WHITE, screen, click, 300, 50)
            #print("compteur tour: "+str(self.compteur_tour))

            if (bouton1_cliqué and pygame.mouse.get_pressed()[0] and not self.first_Entry and self.checkIfTourPerso(self.compteur_tour) and not self.bloc):
                self.clic = True
            elif (not self.first_Entry and not self.checkIfTourPerso(self.compteur_tour) and not self.entered):
                self.monstre_attack()

            # myfont = pygame.font.SysFont('Comic Sans MS', 70)
            # textsurface = myfont.render("{}".format(self.game.clock.get_fps()), False, (0, 0, 0))
            # screen.blit(textsurface, (300, 500))
            if (self.clic):
                bouton2_cliqué = creation_img_text_click(
                    image_boutton, "Attack", ColderWeather_small, WHITE, screen, click, 300, 150)
                bouton3_cliqué = creation_img_text_click(
                    image_boutton, "Mouvement", ColderWeather_small, WHITE, screen, click, 300, 250)
                bouton4_cliqué = creation_img_text_click(
                    image_boutton, "Bonus action", ColderWeather_small, WHITE, screen, click, 300, 350)
                bouton5_cliqué = creation_img_text_click(
                    image_boutton, "Contre attack", ColderWeather_small, WHITE, screen, click, 300, 450)
                bouton6_cliqué = creation_img_text_click(
                    image_boutton, "Nothing", ColderWeather_small, WHITE, screen, click, 300, 550)
                self.check_bouttons(
                    bouton2_cliqué, bouton3_cliqué, bouton4_cliqué, bouton5_cliqué, bouton6_cliqué)

            self.check_bouttons_mvt()

            #if not fin: #pour ne plus afficher le de une fois qu'il a terminé de tourner
            self.essai()

            if current_selec != None:
                current_selec.select(True)
                current_selec.select_neighbour(list_case)
                #current_selec.print_effect(list_case)

            for x in list_case:
                x.print_contains()

            running, self.game.click = basic_checkevent(self.game.click)

            # if f != 255:
            #     for x in range(255):
            #         f+=0.008
            #         transition.set_alpha(int(255-f))
            #     screen.blit(transition,(0,0))

            if (self.message_final.update() and self.activate):
                print("message final")
                self.entered = False
                self.compteur_tour += 1
                self.activate = False
                self.reset_compteur()

                list_case[self.game.player.n_case].is_select = False
                for i in range(5):
                    list_case[i].is_select = False

                if self.checkIfTourPerso(self.compteur_tour):
                    self.bloc = False
            self.reset_compteur()

            # """ FPS
            draw_text("FPS: %i" % (self.game.clock.get_fps()),
                      ColderWeather, WHITE, screen, 100, 100)
            
            # update + draw chatbox
            self.game.chat_box.update()
            self.game.chat_box.draw()

            # print(self.log)
            pygame.display.update()
            self.game.clock.tick(64)
                
    def check_conditions(self):
        if self.n_entrees == 1:
            self.diceevt.resume(20, i=500)
            self.liste_tours.append(
                [self.monstre.name, self.monstre.resultat, self.monstre])
            a = self.monstre.tour
            self.monstre.tour, self.perso1.tour = self.perso1.tour, a
        elif self.n_entrees == 2:
            self.diceevt.resume(20, i=500)
            self.liste_tours.append(
                [self.perso1.name, self.perso1.resultat, self.perso1])
            a = self.perso1.tour
            self.perso1.tour, self.perso2.tour = self.perso2.tour, a
        elif self.n_entrees == 3:
            self.diceevt.resume(20, i=500)
            self.liste_tours.append(
                [self.perso2.name, self.perso2.resultat, self.perso2])
            a = self.perso2.tour
            self.perso2.tour, self.perso3.tour = self.perso3.tour, a
        else:
            if self.first_Entry:
                self.liste_tours.append(
                    [self.perso3.name, self.perso3.resultat, self.perso3])
                self.pause = True
                print(self.liste_tours)
                self.trier(self.liste_tours)
                print(self.liste_tours)
                for liste in self.liste_tours:
                    self.text_tour = self.text_tour + liste[0]+"\n"
                self.first_Entry = False
                self.message = Text(self, text=self.text, size_font=30, pos=[
                                    image_box.get_width(), 20], life_time=5000)
                print(self.message.spawn_time)
                self.message_tour = Text(self, text=self.text_tour, size_font=30, pos=[
                                         image_box.get_width(), 50], life_time=5000)
                self.texts.add(self.message, self.message_tour)
                self.next_text = False

    def degats(self):
        if (not self.checkIfTourPerso(self.compteur_tour)):
            self.diceevt.resume(self.monstre.n_de, i=12000,
                                birthday_time=10000)
            self.message = Text(self, text="generation des degats...", size_font=30, pos=[
                                image_box.get_width(), 20], life_time=13000, born=10000)
            self.texts.add(self.message)
            self.next_dice = False
            self.diceevt.resultat_degats = random.randint(
                1, self.monstre.n_de)
        #print("damage "+str(self.diceevt.resultat_degats))
            self.text, self.text_tour = "Score: " + \
                str(self.diceevt.resultat_degats), ""

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
            self.actdamage = False
            self.text_tour += " Perso 1 hp="+str(self.perso1.hp)+" "+" Perso 2 hp="+str(
                self.perso2.hp)+" "+" Perso 3 hp="+str(self.perso3.hp)+" "
            self.message = Text(self, text=self.text, size_font=30, pos=[
                                image_box.get_width(), 20], life_time=19000, born=13000)
            self.message_tour = Text(self, text=self.text_tour, size_font=30, pos=[
                                     image_box.get_width(), 50], life_time=19000, born=13000)
            self.texts.add(self.message, self.message_tour)

        if (self.next_dice and self.checkIfTourPerso(self.compteur_tour)):
            self.diceevt.resume(
                self.liste_tours[self.compteur_tour][2].n_de, i=14000, birthday_time=10000)
            self.message = Text(self, text="generation des degats...", size_font=30, pos=[
                                image_box.get_width(), 20], life_time=14000, born=10000)
            self.texts.add(self.message)
            self.diceevt.resultat_degats = random.randint(
                1, self.liste_tours[self.compteur_tour][2].n_de)
            self.text, self.text_tour = "Score: " + \
                str(self.diceevt.resultat_degats), ""
        if (self.actdamage and self.checkIfTourPerso(self.compteur_tour)):
            if self.monstre.hit:
                self.monstre.hp -= self.diceevt.resultat_degats
                self.monstre.hit = False
                self.text_tour = "Monstre hp: "+str(self.monstre.hp)
            self.actdamage = False
            self.message = Text(self, text=self.text, size_font=30, pos=[
                                image_box.get_width(), 20], life_time=18000, born=14000)
            self.message_tour = Text(self, text=self.text_tour, size_font=30, pos=[
                                     image_box.get_width(), 50], life_time=18000, born=14000)
            print("dernier self.message "+str(self.message.spawn_time))
            self.texts.add(self.message, self.message_tour)

    def essai(self):  # fonction responsable de l'affichage du de
        if not self.fincombat:
            if self.monstre.tour:
                self.tour = "Monstre"
            elif self.perso1.tour:
                self.tour = "Perso 1"
            elif self.perso2.tour:
                self.tour = "Perso 2"
            elif self.perso3.tour:
                self.tour = "Perso 3"

            if self.stop:  # pour generer un entier aleatoire quand le de finit de tourner
                self.n_entrees += 1  # represente le nbre d'entrees a cette boucle
                self.diceevt.resultat = random.randint(1, n)
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
                    self.text = self.text + "\t"+self.tour+": " + \
                        str(self.diceevt.resultat)  # self.message
                #draw_text(self.message, ColderWeather_small, WHITE,screen, 100, 800)
                self.check_conditions()

                print(self.perso1.hp, self.perso2.hp, self.perso3.hp)

    #trier la liste des resultats
    def trier(self, l):
        self.afficheoptions = True
        for j in range(len(l)):
            iMax = 0
            i = 0
            while i < len(l)-j:
                if l[i][1] < l[iMax][1]:
                    iMax = i
                i = i+1
            l[iMax], l[len(l)-1-j] = l[len(l)-j-1], l[iMax]

    # ajouter une condition pour le click sur la map (qd les cases deviennent rouge)
    def check_bouttons(self, b1, b2, b3, b4, b5):
        global click
        click = True
        # if((b1 or b2 or b3 or b4 or b5) and pygame.mouse.get_pressed()[0]):
        #     print("OKKKKKKKKKK "+str(type(self.liste_tours[self.compteur_tour][2]) == Perso)+'b1 '+str(b1))
        #     self.clic = False #pour annuler l affichage de ces 5 bouttons
        #     self.attack()

        # if (b1 and pygame.mouse.get_pressed()[0] and (type(self.liste_tours[0][2]) == Perso)):
        if (b1 and pygame.mouse.get_pressed()[0]):
            print("attack")
            self.chat_box.write_log(("combat", "You play an attack!"))
            self.clic = False
            self.attack()
        elif (b2 and pygame.mouse.get_pressed()[0]):
            self.player_nbmvt = True
            self.player_mvt = True
        elif (b3 and pygame.mouse.get_pressed()[0]):
            self.bonus_action()
        elif(b4 and pygame.mouse.get_pressed()[0]):
            self.contre_attack()
        elif(b5 and pygame.mouse.get_pressed()[0]):
            self.nothing()

    def check_bouttons_mvt(self):
        if self.player_nbmvt:
            self.get_num = False
            self.bouton1_nbmvt_cliqué = creation_img_text_click(
                image_boutton1, "1 move", ColderWeather_small, WHITE, screen, click, 550, 250)
            self.bouton2_nbmvt_cliqué = creation_img_text_click(
                image_boutton1, "2 moves", ColderWeather_small, WHITE, screen, click, 550, 300)
            self.bouton3_nbmvt_cliqué = creation_img_text_click(
                image_boutton1, "3 moves", ColderWeather_small, WHITE, screen, click, 550, 350)
            self.bouton4_nbmvt_cliqué = creation_img_text_click(
                image_boutton1, "4 moves", ColderWeather_small, WHITE, screen, click, 550, 400)
            self.bouton5_nbmvt_cliqué = creation_img_text_click(
                image_boutton1, "5 moves", ColderWeather_small, WHITE, screen, click, 550, 450)
            self.nbre_mvt()

        if (self.player_mvt and self.get_num):
            self.bouton1_mvt_cliqué = creation_img_text_click(
                image_boutton, "Haut", ColderWeather_small, WHITE, screen, click, 550, 1000)
            self.bouton2_mvt_cliqué = creation_img_text_click(
                image_boutton, "Direct", ColderWeather_small, WHITE, screen, click, 750, 1000)
            self.bouton3_mvt_cliqué = creation_img_text_click(
                image_boutton, "Bas", ColderWeather_small, WHITE, screen, click, 950, 1000)
            self.mouvement()

    def checkIfTourPerso(self, i):
        return type(self.liste_tours[i][2]) == Perso

    def attack(self):
        global list_case
        self.bloc = True
        list_case[self.game.player.n_case].is_select = True
        self.diceevt.resume(20, i=4000)
        self.diceevt.resultat = random.randint(1, 20)
        self.text = "Score du de: "+str(self.diceevt.resultat)+" et bonus DEX: "+str(bonus(
            self.liste_tours[self.compteur_tour][2].DEX)) + " Score: "+str(self.diceevt.resultat+bonus(self.liste_tours[self.compteur_tour][2].DEX))
        if self.diceevt.resultat + bonus(self.liste_tours[self.compteur_tour][2].DEX) >= self.monstre.ac:
            self.text_tour = "Monster hit"
            self.monstre.hit = True
            self.actdamage = True
            self.message_final = Text(self, text="", life_time=18000)
        else:
            self.text_tour = "Monster missed"
            self.message_final = Text(self, text="", life_time=11000)
        self.message = Text(self, text=self.text, size_font=30, pos=[
                            image_box.get_width(), 20], life_time=10000, born=5000)
        self.message_tour = Text(self, text=self.text_tour, size_font=30, pos=[
                                 image_box.get_width(), 50], life_time=10000, born=5000)
        self.texts.add(self.message, self.message_tour)

        if self.actdamage:
            self.degats()

        self.activate = True

    def nbre_mvt(self):
        self.compteur_mouvement = 0
        if(self.bouton1_nbmvt_cliqué and pygame.mouse.get_pressed()[0]):
            self.player.n_mvt = 1
            self.player_nbmvt, self.clic, self.get_num = False, False, True
        elif(self.bouton2_nbmvt_cliqué and pygame.mouse.get_pressed()[0]):
            self.player.n_mvt = 2
            self.player_nbmvt, self.clic, self.get_num = False, False, True
        elif(self.bouton3_nbmvt_cliqué and pygame.mouse.get_pressed()[0]):
            self.player.n_mvt = 3
            self.player_nbmvt, self.clic, self.get_num = False, False, True
        elif(self.bouton4_nbmvt_cliqué and pygame.mouse.get_pressed()[0]):
            self.player.n_mvt = 4
            self.player_nbmvt, self.clic, self.get_num = False, False, True
        elif(self.bouton5_nbmvt_cliqué and pygame.mouse.get_pressed()[0]):
            self.player.n_mvt = 5
            self.player_nbmvt, self.clic, self.get_num = False, False, True

    def mouvement(self):
        print("compteur mouvement "+str(self.compteur_mouvement))
        self.chat_box.write_log("compteur mouvement "+str(self.compteur_mouvement))
        if (self.bouton1_mvt_cliqué and pygame.mouse.get_pressed()[0]):
            while self.compteur_mouvement < self.player.n_mvt:
                self.mouvement_haut()
        elif (self.bouton2_mvt_cliqué and pygame.mouse.get_pressed()[0]):
            while self.compteur_mouvement < self.player.n_mvt:
                self.mouvement_direct()
        elif (self.bouton3_mvt_cliqué and pygame.mouse.get_pressed()[0]):
            while self.compteur_mouvement < self.player.n_mvt:
                self.mouvement_bas()

        if (self.compteur_mouvement >= self.player.n_mvt):
            self.player_mvt = False

    def mouvement_direct(self):
        global list_case
        # print(list_case)
        self.bloc = True
        self.compteur_mouvement += 1
        i, j = list_case[self.game.player.n_case].i + \
            1, list_case[self.game.player.n_case].j - 1
        print(list_case[self.game.player.n_case].j,
              list_case[self.game.player.n_case].i)
        # list_case[self.game.player.n_case].in_case = None
        # self.game.player.n_case -= 6
        # list_case[self.game.player.n_case].in_case = self.game.player
        # list_case[self.game.player.n_case].is_select = True
        if (self.player.nbre_direct < 6):
            if self.check_case(list_case[self.game.player.n_case].i-1, list_case[self.game.player.n_case].j+1):
                self.player.nbre_direct += 1
                
                list_case[self.game.player.n_case].j += 1
                list_case[self.game.player.n_case].i -= 1
                list_case[self.game.player.n_case].in_case = self.game.player
                list_case[self.game.player.n_case].is_select = True
            else:
                print("erreur mvt direct")
                self.message = Text(self, text="Erreur quelqu'un se trouve deja dans cette case",
                                    color=RED, size_font=30, pos=[image_box.get_width()+50, 20], life_time=4000)
                self.texts.add(self.message)
                list_case[self.game.player.n_case].is_select = True
        else:
            print("erreur mvt direct")
            self.message = Text(self, text="Erreur vous avez depasse la limite", color=RED, size_font=30, pos=[
                                image_box.get_width()+50, 20], life_time=4000)
            self.texts.add(self.message)
            list_case[self.game.player.n_case].is_select = True
        self.message_final = Text(self, text="", life_time=4000)
        self.activate = True

    def mouvement_bas(self):
        global list_case
        self.bloc = True
        self.compteur_mouvement += 1
        print("nbre_direct "+str(self.player.nbre_direct))
        print("mvt bas ", list_case[self.game.player.n_case].j,
              list_case[self.game.player.n_case].i)
        if ((list_case[self.game.player.n_case].j == 4 + self.player.nbre_direct) and ((list_case[self.game.player.n_case].i == 12-self.player.nbre_direct) or (list_case[self.game.player.n_case].i == 10 - self.player.nbre_direct))):  # pour ne pas depasser la carte
            print("erreur mvt bas")
            self.message = Text(self, text="Erreur vous avez depasse la limite", color=RED, size_font=30, pos=[
                                image_box.get_width()+50, 20], life_time=4000)
            self.texts.add(self.message)
            list_case[self.game.player.n_case].is_select = True
        else:
            if self.check_case(list_case[self.game.player.n_case].i+1, list_case[self.game.player.n_case].j+1):
                list_case[self.game.player.n_case].j += 1
                list_case[self.game.player.n_case].i += 1
                list_case[self.game.player.n_case].in_case = self.game.player
                list_case[self.game.player.n_case].is_select = True
            else:
                self.message = Text(self, text="Erreur quelqu'un se trouve deja dans cette case",
                                    color=RED, size_font=30, pos=[image_box.get_width()+50, 20], life_time=4000)
                self.texts.add(self.message)
                list_case[self.game.player.n_case].is_select = True
        self.message_final = Text(self, text="", life_time=4000)
        # print(list_case[self.game.player.n_case].i, list_case[self.game.player.n_case].j)
        self.activate = True

    def mouvement_haut(self):
        global list_case
        self.bloc = True
        self.compteur_mouvement += 1
        print("mvt haut ", list_case[self.game.player.n_case].j,
              list_case[self.game.player.n_case].i)
        print("nbre_direct "+str(self.player.nbre_direct))
        if ((list_case[self.game.player.n_case].i == 6-self.player.nbre_direct) and ((list_case[self.game.player.n_case].j == self.player.nbre_direct) or (list_case[self.game.player.n_case].j == self.player.nbre_direct-2))):  # pour ne pas depasser la carte
            print("erreur mvt haut")
            self.message = Text(self, text="Erreur vous avez depasse la limite", color=RED, size_font=30, pos=[
                                image_box.get_width()+50, 20], life_time=2000)
            self.texts.add(self.message)
            list_case[self.game.player.n_case].is_select = True

        else:
            if self.check_case(list_case[self.game.player.n_case].i-1, list_case[self.game.player.n_case].j-1):
                list_case[self.game.player.n_case].i -= 1
                list_case[self.game.player.n_case].j -= 1
                list_case[self.game.player.n_case].in_case = self.game.player
                list_case[self.game.player.n_case].is_select = True
            else:
                self.message = Text(self, text="Erreur quelqu'un se trouve deja dans cette case",
                                    color=RED, size_font=30, pos=[image_box.get_width()+50, 20], life_time=4000)
                self.texts.add(self.message)
                list_case[self.game.player.n_case].is_select = True
        self.message_final = Text(self, text="", life_time=4000)
        self.activate = True

    #voir si la case se trouvant dans une ligne et une colonne precises contient un monstre ou un perso
    def check_case(self, ligne, colonne):
        global list_case

        for case in list_case:
            if (case.i == ligne and case.j == colonne):
                if case.in_case != None:
                    return False
                return True
        return False

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
        self.diceevt.resume(20, i=7000, birthday_time=3000)
        self.perso1.hit, self.perso2.hit, self.perso3.hit = False, False, False
        self.diceevt.resultat_monstreatk = random.randint(1, 20)
        self.bloc = True
        self.text = "Score du dice= "+str(self.diceevt.resultat_monstreatk) + " et bonus dex = "+str(
            bonus(self.monstre.DEX))+"->Score =  "+str(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX))
        self.done_tourner = True
        print("resultat monstreatk "+str(self.diceevt.resultat_monstreatk))

        if(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX) < self.perso1.armor_class and self.done_tourner):
            self.text_tour += " Perso1 missed,"
        elif(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX) >= self.perso1.armor_class and self.done_tourner):
            self.text_tour += " Perso1 hit,"
            self.perso1.hit = True

        if(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX) < self.perso2.armor_class and self.done_tourner):
            self.text_tour += " Perso2 missed,"
        elif(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX) >= self.perso2.armor_class and self.done_tourner):
            self.text_tour += " Perso2 hit,"
            self.perso2.hit = True

        if(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX) < self.perso3.armor_class and self.done_tourner):
            self.text_tour += " Perso3 missed."
        elif(self.diceevt.resultat_monstreatk+bonus(self.monstre.DEX) >= self.perso3.armor_class and self.done_tourner):
            self.text_tour += " Perso3 hit."
            self.perso3.hit = True

        self.message = Text(self, text=self.text, size_font=30, pos=[
                            image_box.get_width(), 20], life_time=10000, born=5000)
        self.message_tour = Text(self, text=self.text_tour, size_font=30, pos=[
                                 image_box.get_width(), 50], life_time=10000, born=5000)
        self.texts.add(self.message, self.message_tour)

        if ((self.perso1.hit or self.perso2.hit or self.perso3.hit) and self.done_tourner):
            self.actdamage = True
            self.message_final = Text(self, text='', life_time=20000)
            self.degats()
        elif(not(self.perso1.hit or self.perso2.hit or self.perso3.hit) and self.done_tourner):
            self.message_final = Text(self, text='', life_time=11000)

        print("self.message "+str(self.message.spawn_time))
        self.next_text = False
        self.activate = True

    def reset_compteur(self):
        if self.compteur_tour >= len(self.liste_tours):
            self.compteur_tour = 0


#j ai ajoute un attribut ac au perso et un dex au monstre
