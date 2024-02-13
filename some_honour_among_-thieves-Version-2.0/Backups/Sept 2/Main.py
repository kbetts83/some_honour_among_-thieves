#Main File for Some Honor Among Thieves?

import pygame
import random

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

    #room  variables
    small_room_area = (0 , 9999)
    med_room_area = (10000, 19999)
    large_room_area = (20000, 10000000)

    hall_thin = 50
    default_room_size = 50

    room_start_pos = random.randint (1,4)

    #wall variabless
    wall_width = 10

    #map variables
    map_mod = 1
    map_width = screen_width * map_mod
    map_height = screen_height *map_mod

    #set up lists
    room_list = []
    hall_list = []
    potential_hall_list = []

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
    def anchor_block(posx,posy,x,y, list_to_add, build, direction ):
        
        if build == "hall":
            size_mod = random.randint (2,4)

        else:
            size_mod = 1

        for ab in range (1,5): 
            ab_posx, ab_posy, ab_x, ab_y = posx , posy , x , y
            direction = 'null'
            
            if ab == 1:
                #create the block on the north side #works
                direction = 'north'
                ab_y = (ab_y * size_mod)
                ab_posy -= ( ab_y )
                if build in ["dump" , "potential room"]:
                    ab_posx = posx + (x/2)
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

                    if last_direction == "east":
                        pass

                    if last_direction == "west":
                        pass
                    
            if ab == 4:
                #create the block on the west side
                direction = 'west'
                ab_x = (ab_x * size_mod)
                ab_posx -= (ab_x )
                if build in ["dump" , "potential room"]:
                    ab_posy = posy + (y/2)
                    ab_posx = posx - 5
                if build == "hall":
                    ab_y = 50

                if build == "potential room":
                    ab_x = 10
                    ab_y = 10
                    ab_posx -= 5

            if ab == 2: 
                #create the block on the east side
                direction = 'east'
                ab_x = (ab_x * size_mod)
                ab_posx += (x)
                if build in ["dump" , "potential room"]:
                    ab_posy = posy + ( y /2)
                    ab_posx -= 5
                if build == "hall":
                    ab_y = 50
                    if last_direction == "south":
                        ab_posy += (last_y-last_x)

                if build == "potential room":
                    ab_x = 10
                    ab_y = 10
                    ab_posx += 5

            if ab == 3: 
                #create the block on the south side
                direction = 'south'
                ab_y = (ab_y * size_mod)
                ab_posy += (y)
                if build in ["dump" , "potential room"]:
                    ab_posx = posx + ( x /2)
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
                    
            #add to whichever list necessary and sprite list
            list_to_add.append ([ab_posx,ab_posy,ab_x,ab_y, Map.waypoint, direction])



    def Grow(posx_grow,posy_grow,x_grow,y_grow, direction , mod):

        north_check = False
        south_check = False
        east_check = False
        west_check = False

        mod += 10
        
        if direction == "north" :
            r = Map (posx_grow,posy_grow - mod ,x_grow ,y_grow + mod, (100,0,0) )

        if direction == "east":

            x_grow += mod
            
            r = Map (posx_grow  ,posy_grow, x_grow  ,y_grow, (100,0,0) )

            check = pygame.sprite.spritecollide(r, boundary_sprites, False)
            if check:
                east_check = True
        
            check = pygame.sprite.spritecollide(r, hall_sprites, False)
            if check:
                east_check = True
            
            if east_check == False:
                x_grow = x_grow + mod
                pygame.sprite.Sprite.kill(r)

                

            if east_check == True:
                r = Map (posx_grow,posy_grow ,10 ,10 , (100,0,0) )
                #r = Map (100,100 ,100 ,100 , (100,0,0) )
                possible_room_sprites.add(r)
                all_sprites.add(r)


        if direction == "south":
            r = Map (posx_grow,posy_grow,x_grow,y_grow + mod, (100,0,0) )

        if direction == "west":
            r = Map (posx_grow - mod ,posy_grow,x_grow,y_grow + mod, (100,100,0) )




        

            

            
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

    def create_rooms():
        #set up output list for the anchor method
        potential_room_list = []

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
            Map.anchor_block(current_hall[0], current_hall[1], current_hall[2], current_hall[3], potential_room_list, "potential room", current_hall[5] )
            for pr in range (len(potential_room_list)):

                pr_room_continue = True
                current_pr = potential_room_list[pr]

                #set the initial variables to grow
              
                r = Map (current_pr[0], current_pr[1],current_pr[2] ,current_pr[3] ,(100,0,0))
                possible_room_sprites.add (r)
                all_sprites.add (r)

                #delete any potential rooms thare are inside of a hallway
                r_hall_collision_test = pygame.sprite.spritecollide(r, hall_sprites, False)
                if r_hall_collision_test:
                    pygame.sprite.Sprite.kill(r)
                    pr_room_continue = False

                #or if collides with the main entry
                r_main_collision_test = pygame.sprite.spritecollide(r, entry_sprite, False)
                if r_main_collision_test:
                    pygame.sprite.Sprite.kill(r)
                    pr_room_continue = False

                if pr_room_continue == True:    

                    # if it's good, make it grow in all directions - if it hits  a hall sprite, make it stop going in that direction
                    #first delete that badboy
                    pygame.sprite.Sprite.kill(r)

                    #get initial stats
                    pr_posx, pr_posy, pr_x, pr_y = current_pr[0], current_pr[1],current_pr[2] ,current_pr[3]

                    for x in range (5):
                        #use the Grow function to grow in every direction
                     #   Map.Grow(pr_posx, pr_posy, pr_x, pr_y, "north" ,x )
                        Map.Grow(pr_posx, pr_posy, pr_x, pr_y, "east" , x)
 #                       Map.Grow(pr_posx, pr_posy, pr_x, pr_y, "south" , x)
                        #Map.Grow(pr_posx, pr_posy, pr_x, pr_y, "west" , x)



                    
                



#call methods
Map.entry_room()
Map.create_boundary()
Map.create_hallways(13, False)
Map.create_rooms()


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
