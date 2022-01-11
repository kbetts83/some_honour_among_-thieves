import pygame
import random

import display

#initiialize display and import display settings
pygame.init()
pygame.mixer.init()
#win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Some Honor Among Thieves - Map - Test")
clock = pygame.time.Clock()

# sprite lists
all_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()
room_sprites = pygame.sprite.Group()
way_sprites = pygame.sprite.Group()
hall_sprites = pygame.sprite.Group()

screen_height = display.screen_height
screen_width = display.screen_width
map_width = screen_width * 8
map_height = screen_height * 8
    
#colours of rooms : 1- 6 not main entry , there will only be one main entry
main_entry = (255,255,255)
office = (131, 252, 244)
storage = (255, 48, 4)
kitchen = (109, 41, 255)
bathroom = (40, 250, 96)
industry = (245, 245, 37)
hallway = (100,100,150)
waypoint  = (250,250,250)
wall = (0,0,0)
wall_width = 10




#room size variables
small_room_area = (0 , 9999)
med_room_area = (10000, 19999)
large_room_area = (20000, 10000000)

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
