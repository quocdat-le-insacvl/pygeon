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
from sorcerer import *


class Combat:

    def __init__(self, game, list_monstre):
        self.game = game
        self.stop_running = False
        self.texts = pygame.sprite.Group()
        self.score = 0  # pour le dice
        self.diceevt = DiceEvent(self, self.game)
        self.pause = False
        self.tourm = True  # cette valeur est a True si c'est le tour du monstre de jouer
        self.perso1 = self.game.player
        self.perso2 = self.game.player.crew_mate[0]
        # a modifier quand on definit sur la map 3 joueurs
        self.perso3 = self.game.player.crew_mate[1]
        self.stop = False  # pour la generation du nombre aleatoire
        self.actdamage = False  # pour activer le calcul des degats
        self.liste_monstre = list_monstre  # a modifier
        self.monstre = Monstre(18,17)  # a remplacer plus tard
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
        self.get_num, self.options_sorts, self.get_rang, self.options_bonus = False, False, False, False
        self.sort_choisi = False
        self.liste_sort,self.list_hit, self.get_listehit =[[0 for i in range(8)]], [], False
        self.nb_monstres, self.nb_attack_monstre = 0, 0 # a remodifier

    def affichage(self):
        global n, list_case, rang
        rang = 0
        self.afficheoptions, self.first_Entry, self.activate, self.entered = False, True, False, False
        running = True
        click = True
        pixel_mask = pygame.mask.from_surface(pixel_red)
        souris_surf = pygame.Surface((1, 1))
        souris_surf.fill(RED)
        souris_surf.set_colorkey(BLACK)
        print("liste monstres ",self.liste_monstre)
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

        #VOIR TOUT LES MONSTRES
        self.nb_monstres= len(self.liste_monstre)

        for x in self.liste_monstre:
            x.case = x.trouver_case(list_case)

        while (running and not self.stop_running):
            #print(self.running)

            self.angle += 10

            self.perso1.levelupchange()
            self.perso2.levelupchange()
            self.perso3.levelupchange()
            self.perso1.check_alive()
            self.perso2.check_alive()
            self.perso3.check_alive()
            # self.perso3.is_alive = False
            # self.perso1.is_alive = False
            
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
                if x.in_case != None and not x.is_select:
                    x.in_case.type_animation = "idle"
                if x.in_case != None and x.is_select:
                    x.in_case.type_animation = "idle"  # attack
                if x.in_case != None:
                    x.in_case.animate()

            for x in list_case:
                x.checkIfSelected()

            ##################################Partie pour les sorts#########################
            # if self.attack:
            #     if self.sort_choisi:
            #         self.bouttons_range(self.liste_sort[0][4])
            #         list_case[self.liste_tours[self.compteur_tour][2].n_case].print_effect(list_case,k=self.liste_sort[0][4]-1,m=self.liste_sort[0][2]-2)
            #         self.activate = True
            if self.get_rang:
                list_case[self.liste_tours[self.compteur_tour][2].n_case].print_effect(list_case,k=rang-1,m=self.liste_sort[0][2]-2)

            if (not self.get_listehit and self.get_rang):
                self.text, self.text_tour = "",""
                self.list_hit = list_case[self.liste_tours[self.compteur_tour][2].n_case].get_effect(list_case,k=rang-1,m=self.liste_sort[0][2]-2)
                for x in self.list_hit:
                    print("name ",x.name)
                    print("hp ",x.hp)
                    if self.liste_sort[0][1] == 1: #degats
                        x.hp -= self.liste_sort[0][0]
                    elif self.liste_sort[0][1] == 0: #soins
                        x.hp += self.liste_sort[0][0]
                    self.text += "\t"+ x.name + " hit\t" 
                    self.text_tour += "\t"+ x.name +" hp: "+ str(x.hp) +"\t"
                self.message = Text(self, text=self.text, size_font=30, pos=[
                                image_box.get_width(), 20], life_time=5000)
                self.message_tour = Text(self, text=self.text_tour, size_font=30, pos=[
                                         image_box.get_width(), 50], life_time=5000)
                self.texts.add(self.message, self.message_tour)
                self.message_final = Text(self, text="", size_font=30, pos=[
                                image_box.get_width(), 20], life_time=5000)
                self.get_listehit, self.activate = True, True
                print("self list hit ", self.list_hit)

            #################################################################################

                # if current_selec != None:
                #     current_selec.select(True)
                #     #current_selec.select_neighbour(list_case)
                #     current_selec.print_effect(list_case)

            for x in list_case:
                x.print_contains()


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

            running, self.game.click = basic_checkevent(self.game.click)
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

            elif (not self.first_Entry and not self.checkIfTourPerso(self.compteur_tour)):
                for x in self.liste_monstre: ################################################################################
                    x.case.is_select = True
                if (not self.entered and len(self.liste_monstre) > 0):
                    self.monstre_attack(self.liste_monstre[0])

            # myfont = pygame.font.SysFont('Comic Sans MS', 70)
            # textsurface = myfont.render("{}".format(self.game.clock.get_fps()), False, (0, 0, 0))
            # screen.blit(textsurface, (300, 500))
            if (self.clic):
                bouton2_cliqué = creation_img_text_click(
                    image_boutton, "Sorts", ColderWeather_small, WHITE, screen, click, 300, 150)
                bouton3_cliqué = creation_img_text_click(
                    image_boutton, "Mouvement", ColderWeather_small, WHITE, screen, click, 300, 250)
                bouton4_cliqué = creation_img_text_click(
                    image_boutton, "Bonus action", ColderWeather_small, WHITE, screen, click, 300, 350)
                bouton5_cliqué = creation_img_text_click(
                    image_boutton, "Attack", ColderWeather_small, WHITE, screen, click, 300, 450)
                bouton6_cliqué = creation_img_text_click(
                    image_boutton, "Nothing", ColderWeather_small, WHITE, screen, click, 300, 550)
                self.check_bouttons(
                    bouton2_cliqué, bouton3_cliqué, bouton4_cliqué, bouton5_cliqué,bouton6_cliqué)

            self.check_bouttons_mvt()
            self.check_bouttons_sorts()
            self.bonus_action()

            #if not fin: #pour ne plus afficher le de une fois qu'il a terminé de tourner
            self.essai()

            # if current_selec != None:
            #     current_selec.select(True)
            #     current_selec.select_neighbour(list_case)

            running, self.game.click = basic_checkevent(self.game.click)

            # if f != 255:
            #     for x in range(255):
            #         f+=0.008
            #         transition.set_alpha(int(255-f))
            #     screen.blit(transition,(0,0))

            if (self.message_final.update() and self.activate):
                print("message final")
                if (self.checkIfTourPerso(self.compteur_tour)):
                    print(self.liste_tours[self.compteur_tour][2].actionP,"bonus ",self.liste_tours[self.compteur_tour][2].bonusAction)
                    list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = False
                    self.mourir_monstre()
                    self.nb_monstres = len(self.liste_monstre)
                    if self.nb_monstres == 0:
                        self.stop_running = True
                    #je peux enlever le print_effect_inverse je pense
                    if self.sort_choisi:
                        list_case[self.liste_tours[self.compteur_tour][2].n_case].print_effect_inverse(list_case,k=self.liste_sort[0][4]-1,m=self.liste_sort[0][2]-2)
                    self.get_rang, self.sort_choisi, self.get_listehit = False, False, False
                    if (self.liste_tours[self.compteur_tour][2].actionP == 0):
                        self.liste_tours[self.compteur_tour][2].actionP = 1
                        self.liste_tours[self.compteur_tour][2].bonusAction = 1
                        self.compteur_tour += 1
                        self.activate = False
                        self.reset_compteur()
    
                elif not self.checkIfTourPerso(self.compteur_tour):
                    if self.nb_attack_monstre < self.nb_monstres:
                        self.entered = False
                        self.mourir(self.perso1)
                        self.mourir(self.perso2)
                        self.mourir(self.perso3)
                        self.monstre_attack(self.liste_monstre[self.nb_attack_monstre])
                    else:
                        for x in self.liste_monstre:
                            x.case.is_select = False

                        # self.compteur_tour += 1
                        # self.nb_attack_monstre = 0
                        # self.reset_compteur()
                        self.mourir(self.perso1)
                        self.mourir(self.perso2)
                        self.mourir(self.perso3)
                        self.compteur_tour += 1
                        self.nb_attack_monstre = 0
                        self.reset_compteur()
                        self.activate, self.entered = False, False
                        # self.reset_compteur()

                self.reset_compteur()
                if self.checkIfTourPerso(self.compteur_tour):
                    self.bloc = False
            #self.reset_compteur()

            # """ FPS
            draw_text("FPS: %i" % (self.game.clock.get_fps()),
                      ColderWeather, WHITE, screen, 100, 100)
            pygame.display.update()
            self.game.clock.tick(64)

    def check_nbvivants(self):
        liste_vivants = []
        if self.perso1.is_alive:
            liste_vivants.append(self.perso1)
        if self.perso2.is_alive:
            liste_vivants.append(self.perso2)
        if self.perso3.is_alive:
            liste_vivants.append(self.perso3)
        return liste_vivants

    "Fonction qui me permet de determiner les tours si j'ai initialement 3 personnages"

    def check_conditions(self):
        print("check conditions")
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
                #print(self.message.spawn_time)
                self.message_tour = Text(self, text=self.text_tour, size_font=30, pos=[
                                         image_box.get_width(), 50], life_time=5000)
                self.texts.add(self.message, self.message_tour)
                self.next_text = False

    "Fonction responsable de la generation des tours si on a 2 persos en vie, les persos vivants sont passes en arguments"

    def check_conditions2(self,perso1,perso2):
        if self.n_entrees == 1:
            self.diceevt.resume(20, i=500)
            self.liste_tours.append(
                [self.monstre.name, self.monstre.resultat, self.monstre])
            a = self.monstre.tour
            self.monstre.tour, perso1.tour = perso1.tour, a
        elif self.n_entrees == 2:
            self.diceevt.resume(20, i=500)
            self.liste_tours.append(
                [perso1.name, perso1.resultat, perso1])
            a = perso1.tour
            perso1.tour, perso2.tour = perso2.tour, a
        else:
            if self.first_Entry:
                self.liste_tours.append(
                    [perso2.name, perso2.resultat, perso2])
                self.pause = True
                print(self.liste_tours)
                self.trier(self.liste_tours)
                print(self.liste_tours)
                for liste in self.liste_tours:
                    self.text_tour = self.text_tour + liste[0]+"\n"
                self.first_Entry = False
                self.message = Text(self, text=self.text, size_font=30, pos=[
                                    image_box.get_width(), 20], life_time=5000,born=1000)
                #print(self.message.spawn_time)
                self.message_tour = Text(self, text=self.text_tour, size_font=30, pos=[
                                         image_box.get_width(), 50], life_time=5000, born=1000)
                self.texts.add(self.message, self.message_tour)
                self.next_text = False

    "Fonction responsable de la generation des tours si on a 1 perso en vie, le perso vivant est passe en arguments"

    def check_conditions3(self,perso1):
        if self.first_Entry:
            self.texts.remove(self.message)

        if self.n_entrees == 1:
            self.diceevt.resume(20, i=500)
            self.liste_tours.append(
                [self.monstre.name, self.monstre.resultat, self.monstre])
            a = self.monstre.tour
            self.monstre.tour, perso1.tour = perso1.tour, a
        else:
            if self.first_Entry:
                self.liste_tours.append(
                    [perso1.name, perso1.resultat, perso1])
                self.pause = True
                print(self.liste_tours)
                self.trier(self.liste_tours)
                print(self.liste_tours)
                for liste in self.liste_tours:
                    self.text_tour = self.text_tour + liste[0]+"\n"
                self.first_Entry = False
                self.message = Text(self, text=self.text, size_font=30, pos=[
                                    image_box.get_width(), 20], life_time=5000)
                #print(self.message.spawn_time)
                self.message_tour = Text(self, text=self.text_tour, size_font=30, pos=[
                                         image_box.get_width(), 50], life_time=5000)
                self.texts.add(self.message, self.message_tour)
                self.next_text = False

    "Fonction responsable du calcul des degats"

    def degats(self):
        global liste_vivants
        #liste_vivants = self.check_nbvivants()
        """Calcul de degats lors d un attack d un monstre"""
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
            for perso in liste_vivants:
                if perso.hit:
                    perso.hp -= self.diceevt.resultat_degats
                    perso.hit = False
                    self.text_tour += " " +perso.name+" hp= "+str(perso.hp)
            self.text = "Score: " + \
                str(self.diceevt.resultat_degats)
            self.actdamage = False
            #ici le message ne doit contenir que les noms des persos qui sont toujours en vie

            self.message = Text(self, text=self.text, size_font=30, pos=[
                                image_box.get_width(), 20], life_time=19000, born=13000)
            self.message_tour = Text(self, text=self.text_tour, size_font=30, pos=[
                                        image_box.get_width(), 50], life_time=19000, born=13000)
            self.texts.add(self.message, self.message_tour)

        """Calcul de degats lors d un attack d un perso"""
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
            self.text_tour= " "
            i = 1
            for monstre in self.liste_monstre:
                if monstre.hit:
                    monstre.hp -= self.diceevt.resultat_degats
                    monstre.hit = False
                    #on doit ajouter ici les hp de tous les monstres presents sur la map qui sont dans la liste self.liste_monstres
                    self.text_tour += " Monstre"+str(i)+" hp: "+str(monstre.hp)+"\t"
                    i += 1
            self.actdamage = False
            self.message = Text(self, text=self.text, size_font=30, pos=[
                                image_box.get_width(), 20], life_time=18000, born=14000)
            self.message_tour = Text(self, text=self.text_tour, size_font=30, pos=[
                                     image_box.get_width(), 50], life_time=18000, born=14000)
            print("dernier self.message "+str(self.message.spawn_time))
            self.texts.add(self.message, self.message_tour)

    def essai(self):  # fonction responsable de l'affichage du de
        liste_vivants = self.check_nbvivants()
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

            #print("::"+str(self.diceevt.resultat))
            self.stop = False
            if self.first_Entry:
                self.text = self.text + "\t"+self.tour+": " + \
                    str(self.diceevt.resultat)  # self.message
            #draw_text(self.message, ColderWeather_small, WHITE,screen, 100, 800)
                if len(liste_vivants) == 3:
                    self.check_conditions()
                elif len(liste_vivants) == 2:
                    self.check_conditions2(liste_vivants[0],liste_vivants[1])
                elif len(liste_vivants) == 1:
                    self.check_conditions3(liste_vivants[0])
            #arreter le combat qd ts les persos sont morts ou qd tous les monstres sonts morts
            if (len(liste_vivants) == 0):
                self.stop_running = True
                print("fin combat")

            """Il faut faire de meme ici pr la liste des monstres"""
            #print(self.perso1.hp, self.perso2.hp, self.perso3.hp)

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
        if (b1 and pygame.mouse.get_pressed()[0]):
            print("sorts")
            #self.clic = False
            self.options_sorts, self.player_nbmvt, self.options_bonus= True, False, False
            self.check_bouttons_sorts()
            #self.attack()
        elif (b2 and pygame.mouse.get_pressed()[0]):
            self.options_sorts, self.options_bonus = False, False
            self.player_nbmvt = True
            self.player_mvt = True
        elif (b3 and pygame.mouse.get_pressed()[0]):
            self.options_sorts, self.player_nbmvt, self.options_bonus= False, False, True
            self.bonus_action()
        elif(b4 and pygame.mouse.get_pressed()[0]):
            self.clic = False
            self.options_sorts, self.player_nbmvt, self.options_bonus= False, False, False
            self.attack_basic()
        elif(b5 and pygame.mouse.get_pressed()[0]):
            self.clic = False
            self.options_sorts, self.player_nbmvt, self.options_bonus= False, False, False
            self.nothing()

    def check_bouttons_mvt(self):
        if (self.player_nbmvt and not self.options_sorts and not self.options_bonus):
            self.get_num, self.bloc = False, True
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

    def check_bouttons_sorts(self):
        global list_case,rang

        if (self.options_sorts and not self.player_nbmvt):
            self.sort_choisi, self.bloc,  self.get_rang = False, True, False
            # list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = True
            self.bouton1_attack_cliqué = creation_img_text_click(
                image_boutton1, "magic missile", ColderWeather_small, WHITE, screen, click, 550, 150)
            self.bouton2_attack_cliqué = creation_img_text_click(
                image_boutton1, "fireball", ColderWeather_small, WHITE, screen, click, 550, 200)
            self.bouton3_attack_cliqué = creation_img_text_click(
                image_boutton1, "firebolt", ColderWeather_small, WHITE, screen, click, 550, 250)

            if (self.bouton1_attack_cliqué and pygame.mouse.get_pressed()[0]):
                list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = True
                self.liste_sort = []
                self.options_sorts, self.clic = False, False
                self.liste_sort = self.liste_tours[self.compteur_tour][2].magic_missile()
                print("liste ",self.liste_sort)
                if self.liste_sort:
                    self.sort_choisi = True
                else:
                    self.bloc, self.options_sorts = False, False
                    list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = False

            elif (self.bouton2_attack_cliqué and pygame.mouse.get_pressed()[0]):
                list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = True
                self.liste_sort = []
                self.options_sorts, self.clic = False, False
                self.liste_sort = self.liste_tours[self.compteur_tour][2].fireball()
                ##########essai#################
                if self.liste_sort:
                    self.sort_choisi = True
                else:
                    self.bloc, self.options_sorts = False, False
                    list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = False
                ####################################
            elif (self.bouton3_attack_cliqué and pygame.mouse.get_pressed()[0]):
                list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = True
                self.liste_sort = []
                self.options_sorts, self.clic = False, False
                self.liste_sort = self.liste_tours[self.compteur_tour][2].firebolt()
                if self.liste_sort:
                    self.sort_choisi = True
                else:
                    self.bloc, self.options_sorts = False, False
                    list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = False

        # if self.liste_sort:
        #     self.sort_choisi = True
        # else:
        #     # self.message_final = Text(self, text="", life_time=2000)
        #     # self.activate = True
        #     self.bloc = False
            # list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = False

        if (self.sort_choisi and not self.get_rang):
            liste_bouttons = self.bouttons_range(self.liste_sort[0][4])
            rang = self.range_choisi(liste_bouttons)
            #list_case[self.liste_tours[self.compteur_tour][2].n_case].print_effect(list_case,k=self.liste_sort[0][4]-1,m=self.liste_sort[0][2]-2)
            #self.activate = True


    #il faut ajouter la aussi fighter et l'eutre classe
    def checkIfTourPerso(self, i):
        return (type(self.liste_tours[i][2]) == Perso or type(self.liste_tours[i][2]) == Sorcerer)

    def attack_basic(self):
        global list_case
        self.bloc = True
        self.text_tour = " "
        self.liste_tours[self.compteur_tour][2].actionP -= 1
        list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = True
        self.diceevt.resume(20, i=4000)
        self.diceevt.resultat = random.randint(1, 20)
        self.text = "Score du de: "+str(self.diceevt.resultat)+" et bonus STR: "+str(bonus(
            self.liste_tours[self.compteur_tour][2].STR)) + " Score: "+str(self.diceevt.resultat+bonus(self.liste_tours[self.compteur_tour][2].STR))

        #ici je dois mettre une boucle for pour passer sur ts les monstres
        i, hit = 1, False #hit est a true si au moins un monstre est touche
        for monstre in self.liste_monstre:
            if self.diceevt.resultat + bonus(self.liste_tours[self.compteur_tour][2].STR) >= monstre.ac:
                self.text_tour += "Monster"+str(i)+" hit\t"
                monstre.hit, hit = True, True
            else:
                self.text_tour += "Monster"+str(i)+" missed\t"
            i += 1
        
        if hit:
            self.actdamage = True
            self.message_final = Text(self, text="", life_time=18000)
        else:
            self.message_final = Text(self, text="", life_time=11000)

        self.message = Text(self, text=self.text, size_font=30, pos=[
                            image_box.get_width(), 20], life_time=10000, born=5000)
        self.message_tour = Text(self, text=self.text_tour, size_font=30, pos=[
                                 image_box.get_width(), 50], life_time=10000, born=5000)
        self.texts.add(self.message, self.message_tour)

        if self.actdamage:
            self.degats()

        self.activate = True

    # def sorts(self):
    #     global list_case
    #     self.bloc = True
    #     list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = True
    #     self.check_bouttons_sorts()


    def nbre_mvt(self):
        self.compteur_mouvement = 0
        if(self.bouton1_nbmvt_cliqué and pygame.mouse.get_pressed()[0]):
            self.liste_tours[self.compteur_tour][2].n_mvt = 1
            self.player_nbmvt, self.clic, self.get_num = False, False, True
        elif(self.bouton2_nbmvt_cliqué and pygame.mouse.get_pressed()[0]):
            self.liste_tours[self.compteur_tour][2].n_mvt = 2
            self.player_nbmvt, self.clic, self.get_num = False, False, True
        elif(self.bouton3_nbmvt_cliqué and pygame.mouse.get_pressed()[0]):
            self.liste_tours[self.compteur_tour][2].n_mvt = 3
            self.player_nbmvt, self.clic, self.get_num = False, False, True
        elif(self.bouton4_nbmvt_cliqué and pygame.mouse.get_pressed()[0]):
            self.liste_tours[self.compteur_tour][2].n_mvt = 4
            self.player_nbmvt, self.clic, self.get_num = False, False, True
        elif(self.bouton5_nbmvt_cliqué and pygame.mouse.get_pressed()[0]):
            self.liste_tours[self.compteur_tour][2].n_mvt = 5
            self.player_nbmvt, self.clic, self.get_num = False, False, True

    def mouvement(self):
        global list_case, ki, kj
        ki, kj = list_case[self.liste_tours[self.compteur_tour][2].n_case].i , list_case[self.liste_tours[self.compteur_tour][2].n_case].j 
        if (self.bouton1_mvt_cliqué and pygame.mouse.get_pressed()[0]):
            ki -= 1
            kj -= 1
            self.liste_tours[self.compteur_tour][2].actionP -= 1
            while self.compteur_mouvement < self.liste_tours[self.compteur_tour][2].n_mvt:
                self.mouvement_haut()
        elif (self.bouton2_mvt_cliqué and pygame.mouse.get_pressed()[0]):
            ki -= 1
            kj += 1
            self.liste_tours[self.compteur_tour][2].actionP -= 1
            while self.compteur_mouvement < self.liste_tours[self.compteur_tour][2].n_mvt:
                self.mouvement_direct()
        elif (self.bouton3_mvt_cliqué and pygame.mouse.get_pressed()[0]):
            ki += 1
            kj += 1
            self.liste_tours[self.compteur_tour][2].actionP -= 1
            while self.compteur_mouvement < self.liste_tours[self.compteur_tour][2].n_mvt:
                self.mouvement_bas()

        if (self.compteur_mouvement >= self.liste_tours[self.compteur_tour][2].n_mvt):
            self.player_mvt = False

    def mouvement_direct(self):
        global list_case,ki,kj
        self.bloc = True
        self.compteur_mouvement += 1
        #############essai##################
        # self.perso3.hp -= 1
        # self.perso1.hp += 10
        ###########################################
        n = numero_case(list_case, ki, kj)
        if (self.liste_tours[self.compteur_tour][2].nbre_direct < 6):
            if self.check_case(ki, kj):
                self.liste_tours[self.compteur_tour][2].nbre_direct += 1
                kj += 1
                ki -= 1
                if self.compteur_mouvement == self.liste_tours[self.compteur_tour][2].n_mvt:
                    list_case[n].in_case, list_case[self.liste_tours[self.compteur_tour][2].n_case].in_case = self.liste_tours[self.compteur_tour][2], None
                    list_case[n].is_select = True
                    self.liste_tours[self.compteur_tour][2].n_case = n
            else:
                print("erreur mvt direct")
                self.message = Text(self, text="Erreur quelqu'un se trouve deja dans cette case",
                                    color=RED, size_font=30, pos=[image_box.get_width()+50, 20], life_time=4000)
                self.texts.add(self.message)

                n = numero_case(list_case, ki+1, kj-1)
                if n !=  self.liste_tours[self.compteur_tour][2].n_case:
                    list_case[n].in_case, list_case[self.liste_tours[self.compteur_tour][2].n_case].in_case = self.liste_tours[self.compteur_tour][2], None
                list_case[n].is_select = True
                self.liste_tours[self.compteur_tour][2].n_case = n
        else:
            print("erreur mvt direct")
            self.message = Text(self, text="Erreur vous avez depasse la limite", color=RED, size_font=30, pos=[
                                image_box.get_width()+50, 20], life_time=4000)
            self.texts.add(self.message)

            n = numero_case(list_case, ki+1, kj-1)
            if n !=  self.liste_tours[self.compteur_tour][2].n_case:
                list_case[n].in_case, list_case[self.liste_tours[self.compteur_tour][2].n_case].in_case = self.liste_tours[self.compteur_tour][2], None
            list_case[n].is_select = True
            self.liste_tours[self.compteur_tour][2].n_case = n

        self.message_final = Text(self, text="", life_time=4000)
        self.activate = True

    def mouvement_bas(self):
        global list_case, ki ,kj
        self.bloc = True
        self.compteur_mouvement += 1
        n = numero_case(list_case, ki, kj)
        if ((kj-1 == 4 + self.liste_tours[self.compteur_tour][2].nbre_direct) and ((ki-1 == 12-self.liste_tours[self.compteur_tour][2].nbre_direct) or (ki-1 == 10 - self.liste_tours[self.compteur_tour][2].nbre_direct))):  # pour ne pas depasser la carte
            print("erreur mvt bas")
            self.message = Text(self, text="Erreur vous avez depasse la limite", color=RED, size_font=30, pos=[
                                image_box.get_width()+50, 20], life_time=4000)
            self.texts.add(self.message)

            n = numero_case(list_case, ki-1, kj-1)
            if n !=  self.liste_tours[self.compteur_tour][2].n_case:
                list_case[n].in_case, list_case[self.liste_tours[self.compteur_tour][2].n_case].in_case = self.liste_tours[self.compteur_tour][2], None
            list_case[n].is_select = True
            self.liste_tours[self.compteur_tour][2].n_case = n
        else:
            if self.check_case(ki, kj):
                kj += 1
                ki += 1
                if self.compteur_mouvement == self.liste_tours[self.compteur_tour][2].n_mvt:
                    list_case[n].in_case, list_case[self.liste_tours[self.compteur_tour][2].n_case].in_case = self.liste_tours[self.compteur_tour][2], None
                    list_case[n].is_select = True
                    self.liste_tours[self.compteur_tour][2].n_case = n
            else:
                self.message = Text(self, text="Erreur quelqu'un se trouve deja dans cette case",
                                    color=RED, size_font=30, pos=[image_box.get_width()+50, 20], life_time=4000)
                self.texts.add(self.message)
                n = numero_case(list_case, ki-1, kj-1)
                if n !=  self.liste_tours[self.compteur_tour][2].n_case:
                    list_case[n].in_case, list_case[self.liste_tours[self.compteur_tour][2].n_case].in_case = self.liste_tours[self.compteur_tour][2], None
                list_case[n].is_select = True
                self.liste_tours[self.compteur_tour][2].n_case = n
        self.message_final = Text(self, text="", life_time=4000)
        # print(list_case[self.liste_tours[self.compteur_tour][2].n_case].i, list_case[self.liste_tours[self.compteur_tour][2].n_case].j)
        self.activate = True

    def mouvement_haut(self):
        global list_case, ki, kj
        self.bloc = True
        self.compteur_mouvement += 1
        n = numero_case(list_case, ki, kj)
        if ((ki+1 == 6-self.liste_tours[self.compteur_tour][2].nbre_direct) and ((kj+1 == self.liste_tours[self.compteur_tour][2].nbre_direct) or (kj+1 == self.liste_tours[self.compteur_tour][2].nbre_direct-2))):  # pour ne pas depasser la carte
            self.message = Text(self, text="Erreur vous avez depasse la limite", color=RED, size_font=30, pos=[
                                image_box.get_width()+50, 20], life_time=2000)
            self.texts.add(self.message)
            
            n = numero_case(list_case, ki+1, kj+1)
            if n !=  self.liste_tours[self.compteur_tour][2].n_case:
                list_case[n].in_case, list_case[self.liste_tours[self.compteur_tour][2].n_case].in_case = self.liste_tours[self.compteur_tour][2], None
            list_case[n].is_select = True
            self.liste_tours[self.compteur_tour][2].n_case = n

        else:
            if self.check_case(ki, kj):
                kj -= 1
                ki -= 1
                if self.compteur_mouvement == self.liste_tours[self.compteur_tour][2].n_mvt:
                    list_case[n].in_case, list_case[self.liste_tours[self.compteur_tour][2].n_case].in_case = self.liste_tours[self.compteur_tour][2], None
                    list_case[n].is_select = True
                    self.liste_tours[self.compteur_tour][2].n_case = n
            else:
                self.message = Text(self, text="Erreur quelqu'un se trouve deja dans cette case",
                                    color=RED, size_font=30, pos=[image_box.get_width()+50, 20], life_time=4000)
                self.texts.add(self.message)

                n = numero_case(list_case, ki+1, kj+1)
                if n !=  self.liste_tours[self.compteur_tour][2].n_case:
                    list_case[n].in_case, list_case[self.liste_tours[self.compteur_tour][2].n_case].in_case = self.liste_tours[self.compteur_tour][2], None
                list_case[n].is_select = True
                self.liste_tours[self.compteur_tour][2].n_case = n
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
        global list_case,rang

        if (self.options_bonus and not self.options_sorts and not self.player_nbmvt):
            self.bloc = True
            # list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = True
            self.bouton1_attack_cliqué = creation_img_text_click(
                image_boutton1, "Convert SP", ColderWeather_small, WHITE, screen, click, 550, 350)
            self.bouton2_attack_cliqué = creation_img_text_click(
                image_boutton1, "Convert Spells", ColderWeather_small, WHITE, screen, click, 550, 400)
            self.bouton3_attack_cliqué = creation_img_text_click(
                image_boutton1, "Quick Spell", ColderWeather_small, WHITE, screen, click, 550, 450)

            if (self.bouton1_attack_cliqué and pygame.mouse.get_pressed()[0]):
                self.bloc, self.options_bonus, self.clic = False, False, False
                n = self.liste_tours[self.compteur_tour][2].convertSP()
                list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = True
                self.message_final = Text(self, text='', life_time=2000)
                self.activate = True
            elif (self.bouton2_attack_cliqué and pygame.mouse.get_pressed()[0]):
                self.bloc, self.options_bonus, self.clic = False, False, False
                n = self.liste_tours[self.compteur_tour][2].convertSpellS()
                list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = True
                self.message_final = Text(self, text='', life_time=2000)
                self.activate = True
            elif (self.bouton3_attack_cliqué and pygame.mouse.get_pressed()[0]):
                self.bloc, self.options_bonus, self.clic = False, False, False
                n = self.liste_tours[self.compteur_tour][2].quick_spell()
                list_case[self.liste_tours[self.compteur_tour][2].n_case].is_select = True
                self.message_final = Text(self, text='', life_time=2000)
                self.activate = True
                

    def nothing(self):
        print("nothing")

    def monstre_attack(self,monstre):
        global list_case, liste_vivants
        self.nb_attack_monstre += 1
        liste_vivants = self.check_nbvivants()
        #############

        self.entered = True
        self.text_tour = "Tour des monstres:"
        # print("dice resultat "+str(self.diceevt.resultat_monstreatk))
        # print(str(self.perso1.hit)+str(self.perso2.hit)+str(self.perso3.hit))
        self.done_tourner = False

        
        self.next_dice = False
        self.diceevt.resume(20, i=7000, birthday_time=3000)
        self.perso1.hit, self.perso2.hit, self.perso3.hit = False, False, False
        self.diceevt.resultat_monstreatk = random.randint(1, 20)
        self.bloc = True
        self.text = "Score du dice= "+str(self.diceevt.resultat_monstreatk) + " et bonus STR = "+str(
            bonus(monstre.STR))+"->Score =  "+str(self.diceevt.resultat_monstreatk+bonus(monstre.STR))
        self.done_tourner = True

        for perso in liste_vivants:
            if(self.diceevt.resultat_monstreatk+bonus(monstre.STR) < perso.armor_class and self.done_tourner ):
                self.text_tour += " "+perso.name+" missed"
            elif(self.diceevt.resultat_monstreatk+bonus(monstre.STR) >= self.perso1.armor_class and self.done_tourner):
                self.text_tour += " "+perso.name+" hit"
                perso.hit = True

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

        self.next_text = False
        self.activate = True

    def reset_compteur(self):
        if self.compteur_tour >= len(self.liste_tours):
            self.compteur_tour = 0



    def mourir(self,player):
        global list_case
        current_tour = self.liste_tours[self.compteur_tour]
        if (not player.is_alive):
            list_case[player.n_case].in_case = None
            for l in self.liste_tours:
                if l[2] == player:
                    self.liste_tours.remove(l)
        self.compteur_tour = self.liste_tours.index(current_tour)

    def mourir_monstre(self):
        for monstre in self.liste_monstre:
            monstre.check_alive()
            if(not monstre.is_alive):
                monstre.case.in_case = None
                self.liste_monstre.remove(monstre)

    """Cette fonction sert a generer les bouttons permettant au perso de choisir le range qu'il desire pour un sort, cette fonction rend une liste de bouttons"""
    def bouttons_range(self, n):
        liste_bouttons =[]
        k = 550
        for i in range(n):
            bouton_range = creation_img_text_click(image_boutton, "range "+str(i+1), ColderWeather_small, WHITE, screen, click, k, 1000)
            liste_bouttons.append(bouton_range)
            k += 200
        return liste_bouttons

    """Recuperer le range choisi"""
    def range_choisi(self,liste):
        i = 1
        for boutton in liste:
            if(boutton and pygame.mouse.get_pressed()[0]):
                self.get_rang = True
                return i
            i += 1

#j ai ajoute un attribut ac au perso et un dex au monstre
