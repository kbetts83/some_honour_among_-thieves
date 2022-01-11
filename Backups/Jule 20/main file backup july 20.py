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
    hall_thin = 50

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
        self.col = col

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

    def hall_room_check(ra,rb, rla, rlb ):

        commit_ra = True
        commit_rb = True
        
        #check to see if there's a collision with the new room/hall
        #if so, try and move, no luck, delete
        overlap_hall_testa = pygame.sprite.spritecollide(ra, hall_sprites, False)
        overlap_hall_testb = pygame.sprite.spritecollide(rb, hall_sprites, False)

        if overlap_hall_testa:
            pygame.sprite.Sprite.kill(ra)
            commit_ra = False
            
        if overlap_hall_testb:
            pygame.sprite.Sprite.kill(rb)
            commit_rb = False

        overlap_room_testa = pygame.sprite.spritecollide(ra, room_sprites, False)
        overlap_room_testb = pygame.sprite.spritecollide(rb, room_sprites, False)

        if overlap_room_testa:
            pygame.sprite.Sprite.kill(ra)
            commit_ra = False

        if overlap_room_testa:
            pygame.sprite.Sprite.kill(rb)
            commit_rb = False

        if commit_ra == True:
            room_sprites.add(ra)
            all_sprites.add (ra)
            room_list.append (rla)

        if commit_rb == True:
            room_sprites.add(rb)
            all_sprites.add (rb)
            room_list.append (rlb)

    
    def build_rooms(final_hall_att ):

        tall = False
        long = False

        #fetch the ata for each hall
        current_hall = final_hall_att
        hall_x = current_hall[0]
        hall_y = current_hall[1]
        hall_posx = current_hall[2]
        hall_posy = current_hall[3]

        #make sure it's a hallway

        if current_hall [4] == (100,100,150):
            room_type = random.randint (0, 4)
        
        #figure out if it's a long hall or a tall hall
        #then set which way the room gets to shift if possible
        #and check how long the long/tall is so we can figure out how many rooms we gotta put in

            #if it's long
            if hall_x > hall_y:
                hall_len = hall_x
                long = True
                
                #top
                posx_a = hall_posx
                posy_a = hall_posy - hall_y - Room.hall_thin
                
                #bot
                posx_b = hall_posx
                posy_b = hall_posy + Room.hall_thin

            #if it's tall
            if hall_y > hall_x:
                hall_len = hall_y
                tall= True
                
                # left
                posx_a = hall_posx - Room.hall_thin - hall_x
                posy_a = hall_posy

                #right
                posx_b = hall_posx +Room.hall_thin
                posy_b = hall_posy


            #roll for room type                    

            if room_type == 0:
                #office_room
                x = 100
                y = 100
                col = Room.office           
                
            if room_type == 1:
                #storage_room
                x = (random.randint (100,200))
                y = (random.randint (100,200))
                col = Room.storage                   

            if room_type == 2:
                #kitchen_room
                x = (random.randint (100,200))
                y = (random.randint (100,200))
                col = Room.kitchen                

            if room_type == 3:
                #bathroom_room
                x = 100
                y = 100
                col = Room.bathroom

            if room_type == 4:
                #industry_room
                x = (random.randint (300,400))
                y = (random.randint (300,400))
                col = Room.industry


            #decide how many rooms to create
            room_count_x = int (hall_len / x)
            room_count_y = int (hall_len / y)

            #now draw the room/s
            #check if room doesn't hit another room


            if long == True:
                for x_co in range (room_count_x):

                    repeat = x_co * x

                    ra = Room (x,y,posx_a + repeat , posy_a, col)
                    rla= ((x,y, posx_a + repeat , posy_a, col))
                    rb = Room (x,y,posx_b + repeat , posy_b, col)
                    rlb = ((x,y,posx_b + repeat , posy_b, col))
                    Room.hall_room_check (ra,rb,rla,rlb)

            if tall == True:
                for y_co in range (room_count_y):

                    repeat = y_co * y

                    ra = Room (x,y,posx_a, posy_a + repeat , col)
                    rla = ((x,y,posx_a, posy_a + repeat , col))
                    rb = Room (x,y,posx_b, posy_b + repeat  , col)
                    rlb = ((x,y,posx_b, posy_b + repeat  , col))
                    Room.hall_room_check (ra,rb,rla, rlb)

            tall = False
            long = False
            repeat = 0

    def draw(build_e):

        if build_e == True:
            #create entryway
            #and create starting position for characters
            
            x = 50
            y = 50

            #room_start_pos factor this in
            
            #north
            if Room.room_start_pos == 1:
                posx =random.randrange (0,screen_width - 60,50)
                posy = 0
                Room.theif_x_start = posx + (x/2)
                Room.theif_y_start = posy + Wall.wall_width

            #east
            if Room.room_start_pos == 2:
                posx = screen_width - 60
                posy = random.randrange(0, screen_height - 100, 50)
                Room.theif_x_start = posx + x - (Wall.wall_width * 2)
                Room.theif_y_start = posy + y/2

            # south
            if Room.room_start_pos == 3:
                posx= random.randrange(0, screen_height - 60, 50)
                posy = screen_height - 60
                Room.theif_x_start = posx + x/2
                Room.theif_y_start = posy + y - (Wall.wall_width*2)

            #west
            if Room.room_start_pos == 4:
                posx = 0
                posy= random.randrange(0, screen_height - 60, 50)
                Room.theif_x_start = posx + Wall.wall_width
                Room.theif_y_start = posy + y/2

            posx = 300
            posy = 300

            r = Room (x,y,posx, posy, Room.main_entry)
            room_list.append ((x,y,posx,posy, Room.main_entry))
            room_sprites.add(r)
            Room.hall_list.append((x,y,posx,posy, Room.main_entry, 'no'))
            all_sprites.add(r)

            #create boundaires

            b1 = Room (1000,1000, 0, -1000, Room.main_entry)
            b2 = Room (1000,1000, 0, Room.map_height, Room.main_entry)
            b3 = Room (1000,1000, -1000, 0, Room.main_entry)
            b4 = Room (1000,1000 ,Room.map_width, 0, Room.main_entry)
            
            boundary_sprites.add (b1, b2, b3, b4)
            all_sprites.add (boundary_sprites)

            orx = x
            ory = y
            orposx = posx
            orposy = posy

        else:
            
            x = 50
            y = 50
            
        for hb in range (3):

            #hallway size variables
            hall_thin = 50
            hall_long = random.randrange (250, 450, 50)

            #create 8 options - left up, left left, left down, middle up, middle down, right up, right right, right down
            last_room = Room.hall_list[hb]
            last_x = last_room[0]
            last_y = last_room[1]
            last_posx= last_room[2]
            last_posy = last_room[3]
            last_direction = last_room[4]

            #take the coordinates and run them through the check_hall function
            #this function checks collisions and
            
            right_up = (hall_thin, hall_long, last_posx+ x , last_posy- hall_long + last_y, Room.hallway,"right_up")
            #Room.check_halls(right_up)
            right_right = (hall_long, hall_thin, last_posx+x , last_posy, Room.hallway, "right_right")
            Room.check_halls(right_right)
            right_down = (hall_thin, hall_long, last_posx+x , last_posy- last_y + last_y, Room.hallway, "right_down")
            #Room.check_halls(right_down)
            left_up = (hall_thin, hall_long, last_posx- x , last_posy- hall_long + last_y, Room.hallway, "left_up")
            #Room.check_halls(left_up)
            left_left = (hall_long, hall_thin, last_posx- hall_long , last_posy, Room.hallway,"left_left")
            Room.check_halls(left_left)
            left_down =(hall_thin, hall_long, last_posx - x ,  last_posy- last_y + last_y , Room.hallway, "left_down")
            #Room.check_halls(left_down)
            up_up = (hall_thin, hall_long, last_posx , last_posy- hall_long, Room.hallway, "up_up")
            Room.check_halls(up_up)
            down_down = (hall_thin, hall_long, last_posx , last_posy+ last_y, Room.hallway,"down_down")
            Room.check_halls(down_down)

            #sort list by score
            Room.potential_hall_list.sort(key=lambda x:x[1], reverse= True)
            
            #select hall from top 3 scored halls at random and make that the new hall
            final_hall = Room.potential_hall_list[random.randint(0,1)]
            
            #final_hall = Room.potential_hall_list[0]
            final_hall_att = (final_hall[2])
            
            hall = Room (final_hall_att[0], final_hall_att[1],final_hall_att[2],final_hall_att[3], final_hall_att[4])
            room_sprites.add (hall)

            #add hall sprite to all sprites and to hall_list
            hall_sprites.add(hall)
            all_sprites.add (hall)
            Room.hall_list.append (final_hall_att)
            room_list.append (final_hall_att)

            Room.build_rooms(final_hall_att)
    
            #reset potential hall list
            Room.potential_hall_list.clear()

            
            
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
