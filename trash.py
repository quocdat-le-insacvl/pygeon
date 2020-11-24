#y= 0
            #for i in range(len(key)):
            #    if 50*i % LONGUEUR > LONGUEUR - 100:
            #        y +=1
            #    screen.blit(key[i].wpn_img,((50*i % LONGUEUR),(y*50)))
            
            #self.draw_text('Credit', Drifftype, WHITE, screen, 20, 20)
 text_width, text_height = Drifftype.size("Option")
            button_2 = pygame.Rect(LONGUEUR//2 - text_width // 2, LARGEUR//2.1, text_width, text_height)
            self.draw_text('Option',Drifftype,GREY,screen,LONGUEUR//2 - text_width // 2,LARGEUR//2.1)

            text_width, text_height = Drifftype.size("Credit")
            self.draw_text('Credit',Drifftype,GREY,screen,LONGUEUR//2 - text_width // 2,LARGEUR//1.6)
            button_3 = pygame.Rect(LONGUEUR//2 - text_width // 2, LARGEUR//1.6, text_width, text_height)

            text_width, text_height = Drifftype.size("Quit")
            button_4 = pygame.Rect(LONGUEUR//2 - text_width // 2, LARGEUR//1.3, text_width, text_height)
            self.draw_text('Quit',Drifftype,GREY,screen,LONGUEUR//2 - text_width // 2,LARGEUR//1.3)

text_width, text_height = Drifftype.size("Play")
            button_1 = pygame.Rect(LONGUEUR//2 - text_width // 2, LARGEUR//3, text_width, text_height)
            self.draw_text('Play',Drifftype,GREY,screen,LONGUEUR//2 - text_width // 2,LARGEUR//3)