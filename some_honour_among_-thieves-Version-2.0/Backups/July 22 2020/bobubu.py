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

    room_start_pos = random.randint (1,4)


    def __init__(self,x,y,posx,posy,col):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((x , y ))
        self.image.fill(col)  
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.x = x
        self.y = y
        col = col

    def check_halls(proto_hall):
        
        potential_hall_list = []

        weight_choice = 0
        hall_stats = []

        #attempt to find the last direction , if can't be found, make it 'nope'
        try:
            last_direction = Room.last_direction
        except:
            last_direction = 'nope'

        #get attributes for halls
        hall_stats.append(proto_hall[5])
        create_hall = Room (proto_hall[0], proto_hall[1],proto_hall[2],proto_hall[3], proto_hall[4])

        temp_hall_x = proto_hall[0]
        temp_hall_y = proto_hall[1]
        temp_hall_posx = proto_hall[2]
        temp_hall_posy = proto_hall[3]

        temp_hall_dir = proto_hall[5]

        #weight the choice left if it goes over the boudnary of the map

        bound_collide_check = pygame.sprite.spritecollide(create_hall, boundary_sprites, False)
        if bound_collide_check:
            weight_choice -= 10
        else:
            weight_choice + 2

        #weight better if it's not a boundary
        if not bound_collide_check:
            weight_choice += 3

        #check for room collision
        room_collide_check = pygame.sprite.spritecollide(create_hall, room_sprites, False)
        if room_collide_check:
            weight_choice -= 250

        #check for other hall collition
        hall_collide_check = pygame.sprite.spritecollide(create_hall, hall_sprites, False)
        if hall_collide_check:
            weight_choice -= 1
        else:
            weight_choice +=  1

        #guide the rooms away from the start room

            # n
            if Room.room_start_pos == 1:
                if temp_hall_dir == "down_down":
                    weight_choice +=  1

            # e
            if Room.room_start_pos == 2:
                if temp_hall_dir == "left_left":
                    weight_choice +=  1

            # s
            if Room.room_start_pos == 3:
                 if temp_hall_dir == "up_up":
                    weight_choice +=  1

            # w
            if Room.room_start_pos == 4:
                if temp_hall_dir == "right_right":
                    weight_choice +=  1

        #weight less if previous direciton is the same as the last
        if (temp_hall_dir) != last_direction:
            weight_choice += 2

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

        neighbor_hall_check = pygame.sprite.spritecollide(create_hall, hall_sprites, False)
        if neighbor_hall_check:
            weight_choice -= 5

        if not neighbor_hall_check:
            weight_choice += 2
                        
        #get the last direction
        Room.last_direction = temp_hall_dir

    
        
        #add hall to temporary sprite list
        pos_hall_sprites.add(create_hall)

        hall_stats.append (weight_choice)
        hall_stats.append ((proto_hall[0], proto_hall[1],proto_hall[2],proto_hall[3], proto_hall[4], weight_choice))
        
        Room.potential_hall_list.append(hall_stats)

    def draw(build_e):

        if build_e == True:
            #create entryway
            #and create starting position for characters
            
            x = 50
            y = 50

            #room_start_pos factor this in
            

            posx = 200
            posy = 200

            r = Room (x,y,posx, posy, Room.main_entry)
            room_list.append ((x,y,posx,posy, Room.main_entry))
            room_sprites.add(r)
            Room.hall_list.append((x,y,posx,posy, Room.main_entry, 'no'))
            all_sprites.add(r)

           

        #build rooms

        hll = 0
            
        #fetch the ata for each hall
        current_hall = Room.hall_list[hll]
        print (current_hall)
        hall_x = current_hall[0]
        hall_y = current_hall[1]
        hall_posx = current_hall[2]
        hall_posy = current_hall[3]

        #figure out if it's a long hall or a tall hall
        #then set which way the room gets to shift if possible

        #and check how long the long/tall is so we can figure out how many rooms we gotta put in
        
        if hall_x > hall_y:
            shift_a = hall_posx + hall_thin
            shift_b = hall_posx + hall_thin
            #shift c and b is over by the previous hall room length

            hall_len = hall_x

        if hall_y > hall_x:
            shift_a = hall_posy + hall_thin
            shift_b = hall_posy + hall_thin
            #shift c and b is over by the previous hall room length

            hall_len = hall_y

    
        #generate the type of room
        room_type = random.randint (0, 4)
        room_type = 0

            
        if room_type == 0:
            #office_room
            x = 100
            y = 100
            hall_col = Room.office
            repeat = 3
            
        if room_type == 1:
            #storage_room
            x = (random.randint (100,200))
            y = (random.randint (100,200))
            hall_col = Room.storage
            repeat = 8
            

        if room_type == 2:
            #kitchen_room
            x = (random.randint (100,200))
            y = (random.randint (100,200))
            hall_col = Room.kitchen
            repeat = 11

        if room_type == 3:
            #bathroom_room
            x = 100
            y = 100
            hall_col = Room.bathroom
            repeat = 9

        if room_type == 4:
            #industry_room
            x = (random.randint (300,400))
            y = (random.randint (300,400))
            hall_col = Room.industry
            repeat = 8


                
        r = Room (x,y,hall_posx, hall_posy, hall_col)

        room_sprites.add(r)
        all_sprites.add(r)

            
#set up waypoint class
class Waypoint (pygame.sprite.Sprite):
    wp = (0,100,100)

    def __init__(self, posx,posy,col):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10 , 10 ))
        self.image.fill(col)  # the colour
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    def hall_waypoint():
        pass
    
##        wp = [Room.theif_x_start, Room.theif_y_start]
##        Waypoint = (wp)
##        add.all_sprites(wp)
        

#set up wall class
class Wall (pygame.sprite.Sprite):
    wall = (0,0,0)
    wall_width = 10
    
    def __init__(self,x,y,posx,posy,col):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((x , y ))
        self.image.fill(col)  # the colour
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.x = Wall.wall_width
        self.y = Wall.wall_width
        col = Wall.wall

    def create_wall():

        #get information for walls from room list
        for w in range (0, len (room_list)):
            current_room = room_list[w]
            x =    current_room [0]
            y=     current_room [1]
            posx = current_room [2]
            posy = current_room [3]
            col  = current_room [4]

            #calculate how many times we need to build each unit of wall
            wall_units_hor = (int(x / Wall.wall_width))
            wall_units_ver = (int(y / Wall.wall_width))

            if col != (100,100,150):
                #create both top and bottom walls for rooms
                for wh in range (wall_units_hor):
                    room_wall_top = Wall (Wall.wall_width, Wall.wall_width, posx + (wh*10) , posy, Wall.wall)
                    #check if there's already a wall there, if so, just delete it
                    overlap_wall_test = pygame.sprite.spritecollide(room_wall_top, wall_sprites, True)
                    wall_sprites.add(room_wall_top)
                    
                    room_wall_bot = Wall (Wall.wall_width, Wall.wall_width, posx + (wh *10) , posy+y, Wall.wall)
                    overlap_wall_test = pygame.sprite.spritecollide(room_wall_bot, wall_sprites, True)
                    wall_sprites.add(room_wall_bot)

                #create left and right walls for rooms
                for wh in range (wall_units_ver + 1):
                    room_wall_left = Wall (Wall.wall_width, Wall.wall_width, posx, posy + (wh*10), Wall.wall)
                    overlap_wall_test = pygame.sprite.spritecollide(room_wall_left, wall_sprites, True)
                    wall_sprites.add(room_wall_left)

                    room_wall_right = Wall (Wall.wall_width, Wall.wall_width, posx +x , posy + (wh*10), Wall.wall)
                    overlap_wall_test = pygame.sprite.spritecollide(room_wall_right, wall_sprites, True)
                    wall_sprites.add(room_wall_right)

            if col == (100,100,150):

                #create bottom and top walls for halls.

                #create a top "test wall" to see if it collides with more than one hallway
                for wh in range (wall_units_hor):
                    hall_top_test = Wall (Wall.wall_width, Wall.wall_width* 3, posx + wh *10 , posy- Wall.wall_width, Wall.wall)
                    wall_sprites.add(hall_top_test)
                    top_test = pygame.sprite.spritecollide(hall_top_test, hall_sprites, False)

                    #if there's only 1 collision, it means it's on the outside, so build it
                    if (len(top_test)) == 1:
                            room_wall_top = Wall (Wall.wall_width, Wall.wall_width, posx + wh * 10, posy, Wall.wall)
                            overlap_wall_test = pygame.sprite.spritecollide(room_wall_top, wall_sprites, True)

                            wall_sprites.add(room_wall_top)

                    pygame.sprite.Sprite.kill(hall_top_test)

                    #create a bottom "test wall" to see if it collides with more than one hallway

                for wh in range (wall_units_hor):
                    hall_bot_test = Wall (Wall.wall_width, Wall.wall_width*3, posx + wh * 10  , posy + y- Wall.wall_width, Wall.wall)
                    wall_sprites.add(hall_bot_test)
                    bot_test = pygame.sprite.spritecollide(hall_bot_test, hall_sprites, False)

                    #if there's only 1 collision, it means it's on the outside, so build it
                    if (len(bot_test)) == 1:
                        
                        room_wall_bot = Wall (Wall.wall_width, Wall.wall_width, posx + wh * 10  , posy+y, Wall.wall)
                        overlap_wall_test = pygame.sprite.spritecollide(room_wall_bot, wall_sprites, True)

                        wall_sprites.add(room_wall_bot)

                    pygame.sprite.Sprite.kill(hall_bot_test)

                #create left and right walls

                #create a left "test wall" to see if it collides with more than one hallway
                for wv in range (wall_units_ver):
                    hall_left_test = Wall (Wall.wall_width * 3, Wall.wall_width, posx - Wall.wall_width , posy + wv * 10, Wall.wall)
                    wall_sprites.add(hall_left_test)
                    left_test = pygame.sprite.spritecollide(hall_left_test, hall_sprites, False)

                    #if there's only 1 collision, it means it's on the outside, so build it
                    if (len(left_test)) == 1:
                            room_wall_left = Wall (Wall.wall_width, Wall.wall_width, posx, posy  + wv * 10, Wall.wall)
                            overlap_wall_test = pygame.sprite.spritecollide(room_wall_left, wall_sprites, True)

                            wall_sprites.add(room_wall_left)

                    pygame.sprite.Sprite.kill(hall_left_test)

                #create a right "test wall" to see if it collides with more than one hallway
                for wv in range (wall_units_ver):
                    hall_right_test = Wall (Wall.wall_width * 3, Wall.wall_width, posx + x - Wall.wall_width , posy + wv * 10, Wall.wall)
                    wall_sprites.add(hall_right_test)
                    right_test = pygame.sprite.spritecollide(hall_right_test, hall_sprites, False)

                    #if there's only 1 collision, it means it's on the outside, so build it
                    if (len(right_test)) == 1:
                            room_wall_right = Wall (Wall.wall_width, Wall.wall_width, posx + x, posy  + wv * 10, Wall.wall)
                            overlap_wall_test = pygame.sprite.spritecollide(room_wall_right, wall_sprites, True)
                            wall_sprites.add(room_wall_right)

                    pygame.sprite.Sprite.kill(hall_right_test)

            #add to the waypoint list 
            all_sprites.add (wall_sprites)
       
class Door(pygame.sprite.Sprite):

    door = (237, 252, 146)
    possible_door_list = []

    def __init__(self, way_pos_x,way_pos_y):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill (Door.door)
        self.rect = self.image.get_rect()
        self.rect.x = way_pos_x
        self.rect.y = way_pos_y

    def create_door():

        for d in range (0, len (room_list)):

            current_room = room_list[d]
            x =    current_room [0]
            y=     current_room [1]
            posx = current_room [2]
            posy = current_room [3]
            col =  current_room [4]
            
            #resent counters & lists
            extra_door = 0
            current_door = []

            #roll to decide if the room gets an extra +1 room
            extra_door_roll = random.randint (1,10)

            if extra_door_roll >= 8:
                extra_door = 1

            #add room number to list of current doors
            current_door.append (d)
            
            #if it's not a hallway, calculate the area of the room and decide how many doors that room should have.
            
            if col != (100,100,150):

                room_area = x * y
                
                if Room.small_room_area[0] <= room_area <= Room.small_room_area[1]:
                    room_doors = 1 + extra_door

                if Room.med_room_area[0] <= room_area <= Room.med_room_area[1]:
                    room_doors = 2 + extra_door
                    
                if Room.large_room_area[0] <= room_area <= Room.large_room_area[1]:
                    room_doors = 3 + extra_door

                #add number of doors to list of current doors
                current_door.append (room_doors)

                #check to see if the room hits a hallway.
                #if it hits a hallway, that should be the default door if there's only one door

                #also add alternate (door 2 and door 3) in case there are too many collisions

                north_door = [random.randrange (posx + Wall.wall_width ,    posx + x - Wall.wall_width *3, Wall.wall_width),    posy  - Wall.wall_width]
                south_door = [random.randrange (posx + Wall.wall_width ,    posx + x - Wall.wall_width *3, Wall.wall_width),    posy + y - Wall.wall_width]
                east_door = [posx + x  - Wall.wall_width, random.randrange (posy + Wall.wall_width, posy+ y - Wall.wall_width *3), Wall.wall_width]
                west_door = [posx - Wall.wall_width, random.randrange (posy + Wall.wall_width, posy+ y - Wall.wall_width *3), Wall.wall_width]

                for x in range (1,5):
                    
                    if x == 1:
                        door =   Door (north_door[0], north_door[1])
                        door_entry =  (north_door[0], north_door[1])
                        
                    if x == 2:
                        door =   Door (south_door[0], south_door[1])
                        door_entry =  (south_door[0], south_door[1])

                    if x == 3:
                        door =   Door (east_door[0],  east_door[1])
                        door_entry =  (east_door[0], east_door[1])

                    if x == 4:
                        door =   Door (west_door[0], west_door[1])
                        door_entry =  (west_door[0], west_door[1])

                    door_hall_check = pygame.sprite.spritecollide(door, hall_sprites, False)
                    
                    if door_hall_check :
                        possible_door_sprites.add (door)
                        all_sprites.add (door)
                        current_door.append ( door_entry)

                # then check to see if the door hits at least 2 rooms, if it does, plaace a temporary door there as well
                # unless that door hits more than X # of walls walls, then kill the door

                    door_room_check = pygame.sprite.spritecollide(door, room_sprites, False)
                    if (len(door_room_check)) > 1 :
                        possible_door_sprites.add (door)
                        all_sprites.add (door)
                        current_door.append (door_entry)

                    door_wall_check = pygame.sprite.spritecollide(door, wall_sprites,False)

                    if (len(door_wall_check)) >= 4 :
                        pygame.sprite.Sprite.kill(door)
                        try:
                            current_door.remove ((door_entry))
                        except:
                            pass
                    pygame.sprite.Sprite.kill(door)

                Door.possible_door_list.append (current_door)

        for fd in range (0, len (Door.possible_door_list)):

            current = Door.possible_door_list[fd]
            room = current [0]
            current.pop(0)
            doors_alloted = current [0]
            current.pop(0)

            num_of_doors = (len(current))
                
            while doors_alloted < num_of_doors:
                choose_door_to_del = random.randint (0, (num_of_doors-1))
                current.pop(choose_door_to_del)

                num_of_doors = (len(current))

            for fr in range (len(current)):
                door_att = current [fr]
                door =   Door (door_att[0], door_att[1])
                door_sprites.add (door)

        #delete any walls that the doors collide with
        door_wall_group_check = pygame.sprite.groupcollide(door_sprites, wall_sprites, True , True)


#Set up Thief - which is the class for  players
class Thief(pygame.sprite.Sprite):
    
        def __init__(self, pos_x,pos_y):

            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((20,20))
            self.image.fill (Door.door)
            self.rect = self.image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y




#call classes and functions to build

Room. draw(True)
Room. draw(False)

Waypoint.hall_waypoint()
Wall.create_wall()
Door.create_door()

#sprite stuff and add in theifs, geo and enemies        
gio = Thief(Room.theif_x_start, Room.theif_y_start)
all_sprites.add(gio)

#test area - print stuff here

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
