import pygame
import random

import display

#initiialize display and import display settings
pygame.init()
pygame.mixer.init()
#win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Some Honor Among Thieves - Map - Test")
clock = pygame.time.Clock()

#room list - too be updated with randomly generated list
rooms = []
#rooms = (
##        (50,50,0, 0,main_entry),
##        (200,50,50, 0,hallway),
##        (200,50,250,0,hallway),
##        (150,50,450,0,hallway),
##        (50,300,550,50,hallway),
##        (300,50,250,300,hallway),
##        (50,100,250,350,hallway),
##        (250,50,0,400,hallway),
##        (50,350,0,50,hallway),
##        (50,250,400,350,hallway),
##        (200,200, 50,50, industry),
##        (100,100,250,50, office),
##        (100,100,350,50, office),
##        (100,100,450,50, office),
##        (200,150,250,150,storage),
##        (100,150,450,150, bathroom),
##        (200,200, 50,200,industry),
##        (100,100, 300,450, kitchen),
##        (150,300,450,350, storage),
##        (100,100,0,500,office),
##        (100,100,100,500,office),
##        (100,100,200,500, office))




#make loop - if bottom of door == top of room thats not a hallway, delete that sprite


###main game loop
##game_continue = True
##while game_continue:
##    clock.tick(60)
##
##    for event in pygame.event.get():
##        if event.type == pygame.QUIT:
##            game_continue = False
##
##    all_sprites.update()
##
##    win.fill((231,226,211))
##    all_sprites.draw(win)
##    pygame.display.flip()
##
##pygame.quit()
