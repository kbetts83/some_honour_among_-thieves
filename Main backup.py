#Main File for Some Honor Among Thieves?

import pygame
import random
import math

# sprite lists
all_sprites = pygame.sprite.Group()

wall_sprites = pygame.sprite.Group()
room_sprites = pygame.sprite.Group()
hall_sprites = pygame.sprite.Group()
possible_door_sprites = pygame.sprite.Group()
possible_hall_sprites = pygame.sprite.Group()
possible_room_sprites = pygame.sprite.Group()
door_sprites = pygame.sprite.Group()
entry_sprite = pygame.sprite.Group()
wall_check_sprites = pygame.sprite.Group()

check_sprites = pygame.sprite.Group()
boundary_sprites = pygame.sprite.Group()
q1_sprite = pygame.sprite.Group()
q2_sprite = pygame.sprite.Group()
q3_sprite = pygame.sprite.Group()
q4_sprite = pygame.sprite.Group()


#display settings
screen_height = 600
screen_width = 800
fps_rate = 60

#initiialize display and import display settings
pygame.init()
pygame.mixer.init()
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Some Honor Among Thieves")
clock = pygame.time.Clock()

class Map (pygame.sprite.Sprite):
    
    #colours of rooms : 1- 7 not main entry , there will only be one main entry
    main_entry = (255, 255, 250)#white
    office = (158, 229, 240) #cyan
    closet = (69,69,59) #dark brown black
    storage = (240, 158, 158) #red
    kitchen = (184, 158, 240) #purple
    bathroom = (191, 240, 158) #green
    industry = (240, 240, 158) # yellow
    locker = (10, 0, 150) #navy blue
    hallway = (100,100,150)
    waypoint  = (100,250,250)
    wall = (0,0,0)

    #room  variables
    small_room_area = (0 , 9999)
    med_room_area = (10000, 19999)
    large_room_area = (20000, 10000000)

    hall_thin = 50
    default_room_size = 50

    room_start_pos = random.randint (1,4)

    #wall variabless
    wall_width = 10


    #door variables
    pot_door_size = wall_width * 2

    #map variables
    map_mod = 1
    map_width = screen_width * map_mod
    map_height = screen_height *map_mod

    #set up lists
    room_list = []
    hall_list = []
    map_list = []
    potential_hall_list = []
    wall_list = []
    final_room_bp = []
    last_corner = []
    final_wall_list = []

    #grow variables
    pot_pos_x = 0
    pot_pos_y = 0
    pot_x = 0
    pot_y = 0


    def __init__(self,posx,posy,x,y,col):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((x , y ))
        self.image.fill(col)  
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.x = x
        self.y = y
        self.col = col

    #sub methods

    def grow_room_space (repeat, pot_pos_x, pot_pos_y, pot_x, pot_y, grow_incr ):

        for xr in range (repeat):
            
            east_grow = True
            west_grow = True
            south_grow = True
            north_grow = True

            if east_grow == True:
                
                #grow east
                #make the potential room grow in the east direction
                pot_x += grow_incr

                #add to sprite and set up collision test
                pot_r = Map (pot_pos_x, pot_pos_y, pot_x, pot_y ,(100,0,0))
                e_hall_collision_test = pygame.sprite.spritecollide(pot_r, hall_sprites, False) or pygame.sprite.spritecollide(pot_r, entry_sprite, False) or pygame.sprite.spritecollide(pot_r, possible_room_sprites, False) or pygame.sprite.spritecollide(pot_r, room_sprites, False)
                possible_room_sprites.add (pot_r)

                #test for a collision
                if e_hall_collision_test:
                    pot_x -= grow_incr
                    pygame.sprite.Sprite.kill(pot_r)
                    east_grow = False
                       
                if not e_hall_collision_test:

                    pygame.sprite.Sprite.kill(pot_r)

            if west_grow == True:
                
                #grow west
                #make the potential room grow in the east direction
                pot_x += grow_incr
                pot_pos_x -= grow_incr
                
                pot_r = Map (pot_pos_x, pot_pos_y, pot_x, pot_y ,(100,0,0))
                w_hall_collision_test = pygame.sprite.spritecollide(pot_r, hall_sprites, False)  or pygame.sprite.spritecollide(pot_r, entry_sprite, False) or pygame.sprite.spritecollide(pot_r, possible_room_sprites, False)  or pygame.sprite.spritecollide(pot_r, room_sprites, False)

                #test for a collision
                if w_hall_collision_test:
                    pot_x -= grow_incr
                    pot_pos_x += grow_incr
                    pygame.sprite.Sprite.kill(pot_r)
                    west_grow = False
                    
                if not w_hall_collision_test:
                    pygame.sprite.Sprite.kill(pot_r)

            if south_grow == True:
                
                #grow east
                #make the potential room grow in the east direction
                pot_y += grow_incr

                #add to sprite and set up collision test
                pot_r = Map (pot_pos_x, pot_pos_y, pot_x, pot_y ,(100,0,0))
                s_hall_collision_test = pygame.sprite.spritecollide(pot_r, hall_sprites, False)  or pygame.sprite.spritecollide(pot_r, entry_sprite, False) or pygame.sprite.spritecollide(pot_r, possible_room_sprites, False) or pygame.sprite.spritecollide(pot_r, room_sprites, False)
                
                #test for a collision
                if s_hall_collision_test:
                    pot_y -= grow_incr
                    pygame.sprite.Sprite.kill(pot_r)
                    east_grow = False
                    
                if not s_hall_collision_test:
                    pygame.sprite.Sprite.kill(pot_r)

            if north_grow == True:
                
                #grow north
                #make the potential room grow in the east direction
                pot_y += grow_incr
                pot_pos_y -= grow_incr
                
                pot_r = Map (pot_pos_x, pot_pos_y, pot_x, pot_y ,(100,0,0))
                n_hall_collision_test = pygame.sprite.spritecollide(pot_r, hall_sprites, False)  or pygame.sprite.spritecollide(pot_r, entry_sprite, False) or pygame.sprite.spritecollide(pot_r, possible_room_sprites, False) or pygame.sprite.spritecollide(pot_r, room_sprites, False)

                #test for a collision
                if n_hall_collision_test:
                    pot_y -= grow_incr
                    pot_pos_y += grow_incr
                    pygame.sprite.Sprite.kill(pot_r)
                    west_grow = False

                if not n_hall_collision_test:
                    pygame.sprite.Sprite.kill(pot_r)
            
            #do one final check - stop the room from getting too big        
            area_check = pot_x* pot_y
            if area_check >= 100000:
                east_grow = False
                west_grow = False
                south_grow = False
                north_grow = False
        
        return (pot_pos_x, pot_pos_y, pot_x, pot_y )

    def corner_check (posx, posy):
        check_sprites.empty ()

        #create a "square' around the potential wall
        mod = Map.wall_width * 2
        c1 = Map (posx - mod, posy - mod ,Map.wall_width, Map.wall_width, (250, 250, 250)  )
        c2 = Map (posx + mod, posy - mod ,Map.wall_width, Map.wall_width, (250, 250, 250) )
        c3 = Map (posx + mod, posy + mod ,Map.wall_width, Map.wall_width, (250, 250, 250) )
        c4 = Map (posx - mod, posy + mod ,Map.wall_width, Map.wall_width, (250, 250, 250) )

        check_sprites.add (c1,c2,c3,c4)
        check = pygame.sprite.groupcollide(check_sprites, hall_sprites, False, False, collided = None)


    def anchor_block(posx,posy,x,y, list_to_add, build, direction ):
        
        if build == "hall":
            size_mod = random.randint (2,4)

        else:
            size_mod = 1

        for ab in range (1,5): 
            ab_posx, ab_posy, ab_x, ab_y = int (posx) , int (posy) , int(x) , int(y)
            direction = 'null'
            
            if ab == 1:
                #create the block on the north side #works
                direction = 'north'
                ab_y = (ab_y * size_mod)
                ab_posy -= ( ab_y )
                if build in ["dump" , "potential room"]:
                    ab_posx = int (posx + (x/2) )
                    ab_posy = posy - 5
                if build == "hall":
                    ab_x = 50
                    if last_direction == "east":
                        ab_posx += last_x - ab_x
                        
                if build == "potential room":
                    ab_x = 10
                    ab_y = 10
                    ab_posy -= 5
                    ab_posx = posx

                if build == "wall":
                    ab_posy = posy
                    ab_posx = posx

                if build == "hall_del":
                    ab_x = Map.default_room_size - (Map.wall_width *2)
                    ab_y = Map.wall_width * 5
                    ab_posy = posy - Map.wall_width * 2
                    ab_posx = posx + Map.wall_width

                if build == "door":
                    ab_posy = posy - ( Map.wall_width /2)
                    ab_posx = random.randint ( (posx + Map.pot_door_size), (posx + x - Map.pot_door_size) )
  
            if ab == 4:
                #create the block on the west side
                direction = 'west'
                ab_x = (ab_x * size_mod)
                ab_posx -= (ab_x )
                if build in ["dump" , "potential room"]:
                    ab_posy = int (posy + (y/2) )
                    ab_posx = posx - 5
                if build == "hall":
                    ab_y = 50

                if build == "potential room":
                    ab_x = 10
                    ab_y = 10
                    ab_posx -= 5

                if build == "wall":
                    ab_posy = posy
                    ab_posx = posx

                if build == "hall_del":
                    ab_y = Map.default_room_size - (Map.wall_width *2)
                    ab_x = Map.wall_width * 5
                    ab_posx = posx - Map.wall_width * 2
                    ab_posy = posy + Map.wall_width

                if build == "door":
                    ab_posy = random.randint ( (posy + Map.pot_door_size), posy+ y - Map.pot_door_size)
                    ab_posx = posx - ( Map.wall_width / 2)
   
            if ab == 2: 
                #create the block on the east side
                direction = 'east'
                ab_x = (ab_x * size_mod)
                ab_posx += (x)
                if build in ["dump" , "potential room"]:
                    ab_posy = int (posy + ( y /2) )
                    ab_posx -= 5
                if build == "hall":
                    ab_y = 50
                    if last_direction == "south":
                        ab_posy += (last_y-last_x)

                if build == "potential room":
                    ab_x = 10
                    ab_y = 10
                    ab_posx += 5

                if build == "wall":
                    ab_posy = posy
                    ab_posx = posx + ab_x - Map.wall_width

                if build == "hall_del":
                    ab_y = Map.default_room_size - (Map.wall_width *2)
                    ab_x = Map.wall_width * 5
                    ab_posx = (posx + x )- Map.wall_width * 2
                    ab_posy = posy + Map.wall_width

                if build == "door":
                    ab_posy = random.randint ( (posy + Map.pot_door_size), posy+ y - Map.pot_door_size)
                    ab_posx = (posx + x) - ( Map.wall_width / 2)

                    
            if ab == 3: 
                #create the block on the south side
                direction = 'south'
                ab_y = (ab_y * size_mod)
                ab_posy += (y)
                if build in ["dump" , "potential room"]:
                    ab_posx = int (posx + ( x /2) )
                    ab_posy -= 5
                if build == "hall":
                    ab_x = 50

                    if last_direction == "east":
                        ab_posx += last_x - ab_x

                if build == "potential room":
                    ab_x = 10
                    ab_y = 10
                    ab_posy += 5
                    ab_posx -= 25

                if build == "wall":
                    ab_posy = posy + (y - Map.wall_width)
                    ab_posx = posx

                if build == "hall_del":
                    ab_x = Map.default_room_size - (Map.wall_width *2)
                    ab_y = Map.wall_width * 5
                    ab_posy = (posy + y) - Map.wall_width * 2
                    ab_posx = posx + Map.wall_width

                if build == "door":
                    ab_posy = posy + y - ( Map.wall_width /2)
                    ab_posx = random.randint ( (posx + Map.pot_door_size), (posx + x - Map.pot_door_size) )
       
            #add to whichever list necessary and sprite list
            list_to_add.append ([ab_posx,ab_posy,ab_x,ab_y, Map.waypoint, direction])

    def repeat_wall(repeat,hall_or_room, pos_x, pos_y, x_mod, y_mod, i):

        # get the repeating values
        x_rep = 0
        y_rep = 0
        
        if y_mod != 0: #this is a horizontal wall
            x_rep = i * Map.wall_width
            y_rep = 0

        if x_mod != 0: #this is a horizontal wall
            x_rep = 0
            y_rep = i * Map.wall_width

        #get check block
        check_w = Map ( (pos_x + x_mod) + x_rep  , (pos_y + y_mod) + y_rep , Map.wall_width ,Map.wall_width, (250,250,250) )
        wall_check_sprites.add (check_w)
        next_door_wall_check = pygame.sprite.spritecollide(check_w, hall_sprites, False)

        if hall_or_room == "hall":

            if  not next_door_wall_check:
                w =  (pos_x + x_rep , pos_y + y_rep)
                Map.final_wall_list.append((pos_x + x_rep , pos_y + y_rep)) 

            if next_door_wall_check:
                #make a check, if it hits nothing,  consider making one more wall to fill in the old corner
                cw = Map (pos_x + x_rep - Map.wall_width , pos_y + y_rep - Map.wall_width , Map.wall_width ,Map.wall_width, (200,200,60) )
                cw_check = pygame.sprite.spritecollide(cw, hall_sprites, False) or pygame.sprite.spritecollide(cw, room_sprites, False)
                
                if not cw_check:
                    Map.final_wall_list.append((pos_x + x_rep , pos_y + y_rep)) 

            
        #add the wall for sure to all the rooms no matter what
        
        if hall_or_room == "room":
            
            Map.final_wall_list.append ((pos_x + x_rep, pos_y + y_rep ))
            
     
    def create_wall(pos_x, pos_y, x ,y, list_to_be_used, hall_or_room):

        #get the amount of times the walls are to be repeated and figure out if the walls will be short
        x_repeat =  int (x/ Map.wall_width)
        y_repeat =  int (y / Map.wall_width)

        #create the positions for the walls
        Map.anchor_block(pos_x,pos_y,x,y, Map.wall_list, 'wall', "dump" )

        #create the checkblocks
        dump_list = []

        #get coordinates for rooms
        for wall in range (len(list_to_be_used)):
            current_wall = list_to_be_used[wall]
            wall_pos_x, wall_pos_y = current_wall[0], current_wall[1]

        for xx in range (0, x_repeat + 1):
            
            #repeat for north and south
            Map.repeat_wall(x_repeat,hall_or_room, pos_x,  pos_y,    0 ,  0 - Map.wall_width, xx  )
            Map.repeat_wall(x_repeat,hall_or_room, pos_x,  pos_y + y , 0 ,  Map.wall_width, xx  )
                        
        for yy in range (0, y_repeat + 1):
                
            #and for the east and west
            Map.repeat_wall(y_repeat, hall_or_room, pos_x + x, pos_y , 0 + Map.wall_width , 0 , yy  )
            Map.repeat_wall(y_repeat, hall_or_room, pos_x,     pos_y,  0 - Map.wall_width, 0, yy  )

        #and clear the list
        Map.wall_list.clear()
        wall_check_sprites.empty()

    


    #main methods
    def entry_room():

        #create entryway

        #create initial room size
        x = Map.default_room_size
        y = Map.default_room_size
     
        #roll for room start position
        global entry_roll 
        entry_roll = random.randint (1,4)

        #north
        if entry_roll == 1:
            posx =random.randrange (0,Map.map_width - 60,50)
            posy = 0

        #east
        if entry_roll == 2:
            posx = screen_width - 50
            posy = random.randrange(0, Map.map_height - 100, 50)

        # south
        if entry_roll == 3:
            posx= random.randrange(0, Map.map_height - 50, 50)
            posy = screen_height - 50

        #west
        if entry_roll == 4:
            posx = 0
            posy= random.randrange(0, Map.map_height - 50, 50)

        # add to map list and hall list and sprite list and entry sptire
        r = Map (posx, posy,x,y, Map.main_entry)
        Map.room_list.append ((posx,posy,x,y, Map.main_entry, "null"))
        Map.hall_list.append ((posx,posy,x,y, Map.main_entry, "null"))
        room_sprites.add(r)
        entry_sprite.add (r)
        all_sprites.add(r) 
    
    def create_boundary():
        #create boundary on outskirt of map
        b1 = Map ( 0, -1000, 1000,1000, Map.main_entry)
        b2 = Map ( 0, Map .map_height,1000,1000, Map.main_entry)
        b3 = Map ( -1000, 0, 1000,1000,  Map.main_entry)
        b4 = Map ( Map.map_width, 0,1000,1000, Map.main_entry)

        boundary_sprites.add (b1,b2,b3,b4)

        #create quadrants
        q1 = Map ( 0, screen_height/2, screen_width / 2,screen_height / 2 , (15,15,15))
        q2 = Map ( 0, 0,screen_width / 2,screen_height / 2 , (35,35,35))
        q3 = Map ( screen_width/ 2, 0, screen_width / 2,screen_height / 2 ,  (55,55,55))
        q4 = Map ( screen_width/2, screen_height/2, screen_width / 2,screen_height / 2 , (75,75,75))

        q1_sprite.add(q1)
        q2_sprite.add(q2)
        q3_sprite.add(q3)
        q4_sprite.add(q4)

    def create_hallways(repeat, second_run):    

        #set up lists and variables
        global last_direction  
        last_direction = "nope"
        dump_list = []
        potential_hall_list = []
        hall_list = Map.hall_list

        hb = 0

        #if this is the second run, make a variable to make certain weights huge
        if second_run == True:
            second_mod = 100
            
        else:
            second_mod = 1
        
        for hb in range (repeat):
           
            #get coordinates of previous room
            global last_room
            
            #try and make the room the next room in hte list, otherwise make the room the very first room (entry room)

            try:
                last_room = hall_list[hb]
            except:
                last_room = hall_list[0]

            global last_posx, last_posy, last_x, last_y
            last_posx, last_posy, last_x, last_y = last_room [0], last_room [1], last_room [2], last_room [3]

            #use anchor block method to create 4 potential hall posiitons/sizes
            Map.anchor_block(last_posx, last_posy, last_x, last_y, potential_hall_list, "hall", "null" )

            #iterate through potential halls and weight them based on certain critera
            for potential_hall in range (len(potential_hall_list)):

                #set hall to a variable
                current_ph = potential_hall_list[potential_hall]

                #reset potential hall weight variable
                ph_weight = 0

                #check to see if potential hall goes out of bounds
                #check to see if potential hall goes out of bounds
                ph = Map (current_ph[0], current_ph[1], current_ph[2] ,current_ph[3], Map.hallway)

                #if it goes out of bounds,weight the room
                ph_boundary_test = pygame.sprite.spritecollide(ph, boundary_sprites, False)
                if ph_boundary_test:
                    ph_weight -= 100
                if not ph_boundary_test:
                    ph_weight += 0

                #check if the hall has any halls directily next door
                #check if the hall has any halls directily next door

                #use anchor block method to create 4 check blocks - see if those blocks collide with another hall
                #set up new list
                pr_dump_list = []
                
                Map.anchor_block(current_ph[0], current_ph[1], current_ph[2], current_ph[3], dump_list, "dump", "null" )
                for db in range (len(dump_list)):
                    current_db = dump_list[db]
                    db = Map (current_db[0], current_db[1], 11, 11, (150,150,0))
                    db_boundary_test = pygame.sprite.spritecollide(db,hall_sprites, False)
                    if db_boundary_test:
                        if (len(db_boundary_test)) >1:
                            ph_weight -= 50
                        else:
                            ph_weight += 1        

                #check if the current direction is the last direction
                #check if the current direction is the last direction

                #if so, weight it down
                if (last_direction) != (current_ph[5]):
                    ph_weight += random.randint (0,1)
                if (last_direction) == (current_ph[5]):
                    ph_weight -= random.randint (0,1)

                #check to see if there's a collision with an exisiting room
                #check to see if theres a collision with an existing room

                ph_hall_collision_test = pygame.sprite.spritecollide(ph, hall_sprites, False)
                if ph_hall_collision_test:
                    ph_weight -= random.randint (3,5)
                if not ph_hall_collision_test:
                    ph_weight += random.randint (0,1)

                #and teh same thing but for the entry hall if it hits the entry room, kill that hall with fire
                ph_entry_test = pygame.sprite.spritecollide(ph, entry_sprite, False)
                if ph_entry_test:
                    ph_weight -= 1000
                    
                #if the hall is in one side of the map, weight hte other direction

                #q1 is bot left
                bl_quad_test= pygame.sprite.spritecollide(ph, q1_sprite, False)
                if bl_quad_test:
                    if (current_ph[5]) in ["north" , "east"]:
                        ph_weight += random.randint (0,1) * second_mod 

                #q2 is top left
                b2_quad_test= pygame.sprite.spritecollide(ph, q2_sprite, False)
                if b2_quad_test:
                    if (current_ph[5]) in ["south", "east"]:
                        ph_weight += random.randint (0,1) * second_mod 

                #q3 is top right
                b3_quad_test= pygame.sprite.spritecollide(ph, q3_sprite, False)
                if b3_quad_test:
                    if (current_ph[5]) in ["south", "west"]:
                        ph_weight += random.randint (0,1) * second_mod 

                #q4 is bot right
                b4_quad_test= pygame.sprite.spritecollide(ph, q4_sprite, False)
                if b4_quad_test:
                    if (current_ph[5]) in ["north" ,"west"]:
                        ph_weight += random.randint (0,1) * second_mod 

                #give positive weight for halls going away from the intial spawn room
                #north
                if entry_roll == 1:
                    if current_ph[5] == "south":
                        ph_weight += random.randint (0,1)
                        
                #east
                if entry_roll == 2:
                    if current_ph[5] == "west":
                        ph_weight += random.randint (0,1)

                # south
                if entry_roll == 3:
                    if current_ph[5] == "north":
                        ph_weight += random.randint (0,1)

                #west
                if entry_roll == 4:
                    if current_ph[5] == "east":
                        ph_weight += random.randint (0,1)
               
                #kill the test sprite, we're done with it
                pygame.sprite.Sprite.kill(ph)
                dump_list.clear()

                #add the weighted value
                current_ph.append (ph_weight)

            # sort the potential halls by weight - best numbers up front
            potential_hall_list.sort(key=lambda x:x[6], reverse= True)
            
            #create roll if positive - which is the sum of the first two potential hall list's weighed numbers
            # if its positive, make it 1 so that it could be either the first or the 2nd in the list

            if (potential_hall_list[0][6] + potential_hall_list[1][6]) >0:
                roll_if_pos = 1
            else:
                roll_if_pos = 0

            #if the best possible hall in the hall list is a negative, stop this whole damn thing
            if (potential_hall_list[0][6] >=0):
                pass

            #select the first in the potential list and add it to the hall list and hall sprites
            hall = potential_hall_list [random.randint (0,roll_if_pos)]
            hall_list.append (hall)
            last_direction = (hall[5])
            h = Map (hall[0], hall[1],hall[2],hall[3],(Map.hallway))
            hall_sprites.add (h)
            all_sprites.add (h)

            #clear list and clear and queue up next hall
            potential_hall_list.clear()

        #create the walls for the halls

        for hall in range (len(Map.hall_list)):
            current_hall = Map.hall_list[hall]
            pos_x, pos_y, x ,y, direction = current_hall[0],current_hall[1],current_hall[2],current_hall[3], current_hall[5]
            Map.create_wall(pos_x, pos_y, x ,y, Map.wall_list, "hall")
            

    def create_rooms():

        #set up output list for the anchor method
        Map.final_room_bp = []

        #set up the potential room areas
        #and then build rooms in those areas
        
        #get the attributes for each hall
        for hall in range (len(Map.hall_list)):
            #get the stats for the last hall as well, if it's less than zero (the first one) just make it zero
            try:
                last_hall = (Map.hall_list[hall-1])
            except:
                last_hall = (Map.hall_list[0])

            #set up the current hall
            current_hall =  (Map.hall_list[hall])

            #use anchor block to create potential rooms
            ab_potential_room_list = []
            Map.anchor_block(current_hall[0], current_hall[1], current_hall[2], current_hall[3], ab_potential_room_list, "potential room", current_hall[5] )
            for pr in range (len(ab_potential_room_list)):

                #set the initial variables to grow
                current_pr = ab_potential_room_list[pr]
                pot_pos_x, pot_pos_y, pot_x, pot_y = current_pr[0], current_pr[1],current_pr[2] ,current_pr[3]
                pot_r = Map (pot_pos_x, pot_pos_y, pot_x, pot_y ,(100,0,0))
                
                #delete any potential rooms thare are inside of a hallway or main entry way
                r_hall_collision_test = pygame.sprite.spritecollide(pot_r, hall_sprites, False)  or pygame.sprite.spritecollide(pot_r, entry_sprite, False)
                if r_hall_collision_test:
                    pygame.sprite.Sprite.kill(pot_r)

                # if it passes the test, make it grow until it hits soemthing # you could probably just use methods here - fix this wh
                if not r_hall_collision_test:
                    #get the variables out of the method and assign them
                    new_var = Map.grow_room_space (50, pot_pos_x, pot_pos_y, pot_x, pot_y, 10)
                    pot_pos_x, pot_pos_y, pot_x, pot_y = new_var[0],new_var[1], new_var[2], new_var [3]

                    #if it's bigger than a set amount, do one more grow room to wigggle it up to size and then commit the room to a list
                    if pot_x > 10 or pot_y > 10:
                        second_new_var = Map.grow_room_space (10, pot_pos_x, pot_pos_y, pot_x, pot_y, 1 )
                        pot_pos_x, pot_pos_y, pot_x, pot_y = second_new_var[0], second_new_var[1], second_new_var[2], second_new_var[3]
                        pot_r = Map (pot_pos_x, pot_pos_y, pot_x, pot_y ,(0,0,0))
                        possible_room_sprites.add (pot_r)
                        Map.final_room_bp.append ([pot_pos_x, pot_pos_y, pot_x, pot_y,pot_x * pot_y ])

        #create the actual rooms within the confines of the possible room spaces
        pygame.sprite.Group.empty (possible_room_sprites)
        
        for bp in range (len(Map.final_room_bp)):

            #reset the global variables
                                                                 
            #get the coordinates
            current_room_bp = Map.final_room_bp [bp]
            current_room_bp = list (current_room_bp)

            bp_pos_x, bp_pos_y, bp_x,bp_y = current_room_bp [0], current_room_bp [1],current_room_bp [2],current_room_bp [3]
    
            #create a set for potential room type
            pot_room_set = {""}

            #parse out the type of room it could be
            if bp_x <= Map.default_room_size or bp_y <= Map.default_room_size :
                pot_room_set.update([Map.office, Map.closet ,Map.kitchen, Map.bathroom, ])
            if bp_x >= Map.default_room_size * 3 or bp_y >= Map.default_room_size * 3:
                pot_room_set.update([Map.industry, Map.storage, Map.office])
            if (bp_x <= Map.default_room_size and bp_y < Map.default_room_size *2) or (bp_x <= Map.default_room_size * 2 and bp_y < Map.default_room_size) :
                pot_room_set.update([Map.bathroom])
            if bp_x <= Map.default_room_size * 2 and bp_y <= Map.default_room_size * 2:
                pot_room_set.update([Map.kitchen, Map.bathroom])

            #remove the blank one
            pot_room_set.remove("")

            # and remove the office and factory if there's another option
            if (len(pot_room_set)) > 3:
                try:
                    pot_room_set.remove (storage)
                except:
                        pass
                try:
                    pot_room_set.remove (industry)
                except:
                        pass

            #pick one room type and add it back on to the main blueprint list
            pot_room_list = list (pot_room_set)
            try:
                pot_room = pot_room_list [random.randint (0, (len (pot_room_list))-1 )] # THIS IS messed up I think
            except:
                pot_room = 0
            current_room_bp.append(pot_room)

            Map.final_room_bp[bp] = current_room_bp

            #determine how many rooms there can be based on room type

            #determine if the room is tall or wide
            if bp_x >= bp_y :
                shape = "wide"

            else:
                shape = "tall"

            room_total = 1

            if pot_room == Map.office:
                if shape == "wide":
                    room_total = int (bp_x / Map.default_room_size)
            
                if shape == "tall":
                    room_total = int (bp_y / Map.default_room_size)

            if pot_room == Map.bathroom:
                if bp_x >= Map.default_room_size * 1.5 or bp_y >= Map.default_room_size * 1.5:
                    room_total = 2

            if pot_room == Map.bathroom or pot_room == Map.storage:
                room_total = random.randint (1,2)

            for total in range (room_total):
                
                #assign the values to the new rooms and add them to the room list
                pos_x, pos_y, x,y, col = current_room_bp[0], current_room_bp[1], current_room_bp[2], current_room_bp[3], current_room_bp[5]

                if room_total >1:
                    if shape == "wide":
                        x = int (x/room_total)
                        pos_x += (x *total)

                    if shape == "tall":
                        y = int (y/ room_total)
                        pos_y +=  (y * total)

                # if it's one of these make it 1 x1
                if col  in [Map.office, Map.closet ,Map.kitchen, Map.bathroom, Map.locker]:

                    #but if it's bigger than 2 by 2 just make it 2
                    if col == Map.office:
                        if x > Map.default_room_size *2 or  y > Map.default_room_size *2:
                            x, y = Map.default_room_size , Map.default_room_size 

                    if shape == "wide":
                        x = y

                    if shape == "tall":
                        y = x

                #get the y repeat and x repeat values so we can figure out how many walls we need
     
                #add the final room the sprites
                final_room = Map (pos_x, pos_y, x ,y, col )
                room_sprites.add (final_room)
                all_sprites.add (final_room)
                Map.room_list.append ((pos_x, pos_y, x,y, col))

                #and delete the room if there's a collision. i can probably fix this later
                last_room_test = pygame.sprite.spritecollide(final_room, hall_sprites, False)
                if last_room_test:
                    pygame.sprite.Sprite.kill(final_room)

                if not last_room_test:
                    Map.create_wall(pos_x, pos_y, x ,y, Map.wall_list, "room")

        #and finally, go through the list of final walls - iterate through and build them
        for w in range (len(Map.final_wall_list)):

            posx,posy = Map.final_wall_list[w][0], Map.final_wall_list[w][1]
            wall = Map (posx, posy, Map.wall_width, Map.wall_width, (0,0,0) )
            wall_sprites.add (wall)
            all_sprites.add (wall)
                    
    def create_doors():

        #create the door list for the anchor block
        pot_door_list = []
        door_list = []
        sub_d_list = []
        final_door_list = []
        
        #get list of rooms and their attributes
        for r in range (len(Map.room_list)):

            room = Map.room_list [r]
            pos_x, pos_y, x, y , room_type = room[0],room[1],room[2],room[3],room[4]

            #use the anchor block to create possible door locations - 
            Map.anchor_block(pos_x,pos_y,x,y, pot_door_list, 'door', "door" )
            door_list.append (pot_door_list)
            pot_door_list = []

        # go through the list of doors and...
        
        for cs in range (len(door_list)):
            current_set = door_list[cs]
            last_list= []
            for cd in range (len(current_set)):
                
                current_door = current_set [cd]
                door_pos_x, door_pos_y = current_door[0], current_door[1],

                #...convert them into sprites - if the sprites are placed properly, leave them, if not delete them
                ms = Map (door_pos_x, door_pos_y, Map.pot_door_size, Map.pot_door_size, (69,69,69) )

                #check to make sure the doors hit at least 2 rooms - that way the doors don't open up to nothing (also check to make sure it collides with a wall)
                room_check = pygame.sprite.spritecollide(ms, room_sprites, False)
                if (len(room_check) ) > 1:
                    wall_check = pygame.sprite.spritecollide(ms, wall_sprites, False)
                    if wall_check:
                        last_list.append ((door_pos_x, door_pos_y, 'room' ))

                #and the same for the hall
                hall_check = ( pygame.sprite.spritecollide(ms, hall_sprites, False) and pygame.sprite.spritecollide(ms, room_sprites, False) )
                if hall_check:
                    last_list.insert(0, (door_pos_x, door_pos_y, 'hall'))

            if len(last_list) >0:
                final_door_list.append (last_list)

        #and go throught the final list - prioritze the hallway doors first and then if the room is big enough (or lucy enough) pick one of the other doors
        for fdl in range (len(final_door_list)):
            door = (final_door_list[fdl])

            #see if the first entry is a hallway door - if it is, pick it and turn that bad boy into a sprite
            if (door[0][2]) == 'hall':
                pos_x, pos_y = int(door[0][0]), int(door[0][1])

            #otherwise, there's no hall doors in the list, pick one at random, add it to the sprite list
            else:
                door_list_len = (len(door)-1)
                po_x, pos_y = int (door[door_list_len][0]), int(door[door_list_len][1])

            col_col = (69,69,69)
            
            hd = Map(pos_x, pos_y, Map.pot_door_size, Map.pot_door_size, (col_col) )

            test_wall_test = ( pygame.sprite.spritecollide(hd, wall_sprites, False))
            if (len(test_wall_test)) > 30:
                col_col = (160,0,0)
                hd = Map(pos_x, pos_y, Map.pot_door_size, Map.pot_door_size, (col_col) )


            all_sprites.add (hd)

            #and then delete that fool
            final_door_check = ( pygame.sprite.spritecollide(hd, wall_sprites, False))
                           

#call methods
Map.entry_room()
Map.create_boundary()
Map.create_hallways(13, False)
Map.create_rooms()
Map.create_doors()


print ("length of wall sprites: ")
print (len(wall_sprites))
print ("length of wall list with duplicates:")
print (len(Map.final_wall_list))
butt = set(Map.final_wall_list)
print ("length of list with no duplicates:")
print (len(butt))
bum = list(butt)
     

#main game loop
game_continue = True
while game_continue:
    clock.tick(fps_rate)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_continue = False

    all_sprites.update()

    win.fill((231,226,211))
    all_sprites.draw(win)
    pygame.display.flip()

pygame.quit()



