#Main File for Some Honor Among Thieves?

import pygame
import random

import display
import character
import map

#initiialize display and import display settings
pygame.init()
pygame.mixer.init()
win = pygame.display.set_mode((display.screen_width, display.screen_height))
pygame.display.set_caption("Some Honor Among Thieves")
clock = pygame.time.Clock()

# sprite lists
all_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()
room_and_hall_sprites = pygame.sprite.Group()
room_sprites = pygame.sprite.Group()
way_sprites = pygame.sprite.Group()
hall_sprites = pygame.sprite.Group()
pos_hall_sprites = pygame.sprite.Group()
door_sprites = pygame.sprite.Group()
possible_door_sprites = pygame.sprite.Group()
check_sprites = pygame.sprite.Group()
boundary_sprites = pygame.sprite.Group()
check_hall_sprites = pygame.sprite.Group()

#lists for rooms, walls, etc
wall_list = []
room_list = []
way_list = []

screen_width = display.screen_width
screen_height = display.screen_height

global draw_entry
draw_entry = True

###set up Room class
class Room (pygame.sprite.Sprite):
    
    screen_height = display.screen_height
    screen_width = display.screen_width

    map_mod = 1
    map_width = screen_width * map_mod
    map_height = screen_height *map_mod
        
    #colours of rooms : 1- 6 not main entry , there will only be one main entry
    main_entry = (205,205,205)
    office = (131, 252, 244)
    storage = (255, 48, 4)
    kitchen = (109, 41, 255)
    bathroom = (40, 250, 96)
    industry = (245, 245, 37)
    hallway = (100,100,150)
    waypoint  = (100,250,250)
    wall = (0,0,0)
    wall_width = 10

    #room size variables
    small_room_area = (0 , 9999)
    med_room_area = (10000, 19999)
    large_room_area = (20000, 10000000)
    screen_width = display.screen_width
    screen_height = display.screen_height

    theif_x_start = 0
    theif_y_start = 0

    #set up lists
    hall_list = []
    potential_hall_list = []
    last_direction = "nope"


    def __init__(self,x,y,posx,posy,col):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((x , y ))
        self.image.fill(col)  # the colour
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.x = x
        self.y = y
        col = col

    def draw():
        
        potential_hall_list = []

        weight_choice = 0
        hall_stats = []

                
        hall = Room (200, 200,400,400, Room.office)
        proto_hall = (200, 200,400,400, Room.office)
        room_sprites.add (hall)

        #add hall sprite to all sprites and to hall_list
        hall_sprites.add(hall)
        all_sprites.add (hall)


        #attempt to find the last direction , if can't be found, make it 'nope'
        try:
            last_direction = Room.last_direction
        except:
            last_direction = 'nope'

        #get attributes for halls

        create_hall = Room (proto_hall[0], proto_hall[1],proto_hall[2],proto_hall[3], proto_hall[4])

        temp_hall_x = proto_hall[0]
        temp_hall_y = proto_hall[1]
        temp_hall_posx = proto_hall[2]
        temp_hall_posy = proto_hall[3]



            #build the checks
        up_check    = Room (10,30, temp_hall_x /2 + temp_hall_posx, temp_hall_posy-15, (0,0,100))
        down_check  = Room (10,30, temp_hall_x /2 + temp_hall_posx , temp_hall_posy +temp_hall_y - 15, (0,0,100))
        right_check = Room (30,10, temp_hall_x + temp_hall_posx-15, temp_hall_posy +temp_hall_y /2,(0,0,100)) 
        left_check  = Room (30,10, temp_hall_posx-15, temp_hall_posy +temp_hall_y /2,(0,0,100)) 

            #add checks to sprite group
        check_hall_sprites.add(up_check)
        check_hall_sprites.add(down_check)
        check_hall_sprites.add(right_check)
        check_hall_sprites.add(left_check)

        all_sprites.add(check_hall_sprites)


        
        #add hall to temporary sprite list
        pos_hall_sprites.add(create_hall)

        hall_stats.append (weight_choice)
        hall_stats.append ((proto_hall[0], proto_hall[1],proto_hall[2],proto_hall[3], proto_hall[4], weight_choice))
        
        Room.potential_hall_list.append(hall_stats)






Room.draw()


#main game loop
game_continue = True
while game_continue:
    clock.tick(display.fps_rate)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_continue = False

    all_sprites.update()

    win.fill((231,226,211))
    all_sprites.draw(win)
    pygame.display.flip()

pygame.quit()
