import pygame
import random
import uuid

import SHAT_game_objects
#random.seed(33) # east
#random.seed(1) #north
#random.seed (21) #west
random.seed (9)

# sprite lists
all_sprites = pygame.sprite.Group()

wall_sprites = pygame.sprite.Group()
guide_walls = pygame.sprite.Group() #can delete
room_sprites = pygame.sprite.Group()
hall_sprites = pygame.sprite.Group()
possible_sprites = pygame.sprite.Group()
door_sprites = pygame.sprite.Group()
entry_sprite = pygame.sprite.Group()
possible_room_sprites = pygame.sprite.Group()
parking_lot_sprites = pygame.sprite.Group()
possible_wall_sprites = pygame.sprite.Group()

check_sprites = pygame.sprite.Group()
boundary_sprites = pygame.sprite.Group()
q1_sprite = pygame.sprite.Group()
q2_sprite = pygame.sprite.Group()
q3_sprite = pygame.sprite.Group()
q4_sprite = pygame.sprite.Group()

#display settings
screen_height = 800
screen_width = 600
fps_rate = 30

#initiialize display and import display settings
pygame.init()
pygame.mixer.init()
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Some Honor Among Thieves")
clock = pygame.time.Clock()

#fullscreen
# pygame.display.toggle_fullscreen()


# random.seed(0x12f20d620)

class Map (pygame.sprite.Sprite):
    
    #colours of rooms : 1- 7 not main entry , there will only be one main entry
    main_entry = (255, 255, 250)#white
    hallway = (100,100,150)
    waypoint  = (100,250,250)
    anchor = (200,0,0)

    room_type_dict = {'office': (158, 229, 240), #blue
                    'closet': (69,69,59), #brown
                    'storage':(240, 158, 158), # pink
                    'kitchen': (184, 158, 240), #brown
                    'bathroom': (191, 240, 158), #green
                    'industry': (240, 240, 158),
                    'locker': (10, 0, 150)
                    }
    room_type_count = {'office': 0,
                    'closet':    0,
                    'storage':   0,
                    'kitchen':   0,
                    'bathroom':  0,
                    'industry':  0,
                    'locker':    0 }
    
    default_room_size = 50
    hall_thin = default_room_size

    room_start_pos = random.randint (1,4)

    #wall variabless
    wall_width = int(default_room_size/10)

    #map variables
    map_mod = 1
    map_width = screen_width * map_mod
    map_height = screen_height *map_mod

    final_room_bp = []

    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((Map.wall_width, Map.wall_width ))
        self.image.fill(Map.anchor)  
        self.rect = self.image.get_rect()
        self.rect.width = Map.wall_width
        self.rect.height = Map.wall_width
        self.direction = 'N/A' 

    def create_boundaries():
        #create boundary on outskirt of map - will colide with walls if they're too far out
        b1,b2,b3,b4 = Map(), Map(), Map(), Map()
        b1.rect =  ( 0, -1000, 1000,1000) # north
        b2.rect =  ( 0, Map .map_height,1000,1000) # south
        b3.rect =  ( -1000, 0, 1000,1000) #west)
        b4.rect =  ( Map.map_width, 0,1000,1000) #east

        boundary_sprites.add (b1,b2,b3,b4)

        q1,q2,q3,q4 = Map(), Map(), Map(), Map()
        q1.rect = ( 0, screen_height/2, screen_width / 2,screen_height / 2 )
        q2.rect = ( 0, 0,screen_width / 2,screen_height / 2 )
        q3.rect = ( screen_width/ 2, 0, screen_width / 2,screen_height / 2 )
        q4.rect = ( screen_width/2, screen_height/2, screen_width / 2,screen_height / 2 )

        q1_sprite.add(q1)
        q2_sprite.add(q2)
        q3_sprite.add(q3)
        q4_sprite.add(q4)

    def create_check_blocks(self):

        cn = Hallway (self.rect.x + self.rect.width /2 - Map.wall_width/2, self.rect.y -Map.wall_width, Map.wall_width, Map.wall_width, 'north')
        cs = Hallway (self.rect.x + self.rect.width /2 - Map.wall_width/2, self.rect.y + self.rect.height, Map.wall_width, Map.wall_width, 'south')
        cw = Hallway (self.rect.x - Map.wall_width, self.rect.y + self.rect.height/2 - Map.wall_width/2, Map.wall_width, Map.wall_width, 'west')
        ce = Hallway (self.rect.x + self.rect.width , self.rect.y + self.rect.height/2 - Map.wall_width/2, Map.wall_width, Map.wall_width, 'east')

        check_sprites.add(cn,cs,ce,cw)
        return check_sprites

class Entry_Room(Map):
    entry = None

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((Map.default_room_size , Map.default_room_size))
        self.image.fill (Map.main_entry)
        self.entry_roll = random.randint (1,4)
        self.rect = self.image.get_rect()
        self.move_amount_x = 0
        self.move_amount_y = 0
        self.vertical_door_count = 1
        self.horizontal_door_count = 1
        self.door_list =  [] #probably dont need these but let's fix this
        self.orientation = None
        self.spawn_points = {}
        self.posy = 0
        self.posx = 0

    def create_entry(self):
        #north
        if self.entry_roll == 1:
            self.rect.x =random.randrange (0, Map.map_width - 60, 50)
            self.rect.y = 0
            Room.create_parking_lot(self.entry_roll, self)
            self.move_amount_y = self.rect.y - Map.wall_width
            self.move_amount_x = self.rect.x
            self.orientation = 'north'
        #east
        if self.entry_roll == 2:
            self.rect.x = screen_width - 50
            self.rect.y = random.randrange(0, Map.map_height - 100, 50)
            Room.create_parking_lot(self.entry_roll, self)
            self.move_amount_x = self.rect.x + Map.wall_width
            self.move_amount_y = self.rect.y
            self.orientation = 'east'
        # south
        if self.entry_roll == 3:
            self.rect.x= random.randrange(0, Map.map_height - 50, 50)
            self.rect.y = screen_height - 50
            Room.create_parking_lot(self.entry_roll, self)
            self.move_amount_y = self.rect.y + Map.wall_width
            self.move_amount_x = self.rect.x
            self.orientation = 'south'
        #west
        if self.entry_roll == 4:
            self.rect.x = 0
            self.rect.y= random.randrange (0, Map.map_height - 50, 50)
            Room.create_parking_lot(self.entry_roll, self)
            self.move_amount_x = self.rect.x - Map.wall_width
            self.move_amount_y = self.rect.y
            self.orientation = 'west'

        self.posx = self.rect.x
        self.posy = self.rect.y

        entry_sprite.add(self)
        Entry_Room.room = self

        #create spawn points for entry room
        SHAT_game_objects.Spawn_Points.create_entry_spawn(self)

    def shuffle_entry_pos(self):
        self.rect.x = self.move_amount_x
        self.rect.y = self.move_amount_y

    def check_around_entry(entry):
        hall_count = 0
        room_count = 0
        delete_room_choice = None
        pot_room_list = []

        check_blocks = Map.create_check_blocks(entry)
        for block in check_blocks:
            check_for_rooms_around_entry = pygame.sprite.spritecollide (block, room_sprites, False)
            if len(check_for_rooms_around_entry) > 0:  
                for r in check_for_rooms_around_entry:
                    pot_room_list.append(r)

            check_for_hall_round_entry = pygame.sprite.spritecollide (block, hall_sprites, False)
            if len(check_for_hall_round_entry) > 0:
                hall_count +=1

        #if the entry is surrounded on all sides - delete the biggest one
        room_count = len(pot_room_list)

        if hall_count + room_count == 4:
            deleted_room = None
            for pr in range (len(pot_room_list)):
                room = (pot_room_list[pr])
                if deleted_room == None:
                    deleted_room = room
                if room.rect.height * room.rect.width >= deleted_room.rect.width * deleted_room.rect.height:
                    deleted_room = room

            pygame.sprite.Sprite.kill(room)   

class Hallway(Map):

    def __init__(self,posx, posy,x,y, direction):
        super().__init__()
        self.image = pygame.Surface((x,y))
        self.rect.x = posx
        self.rect.y = posy
        self.rect.width = x
        self.rect.height = y
        self.hall_size_mod = random.randint (2,4)
        self.image.fill(Map.hallway)  
        self.direction = direction
        self.ph_weight = 0

    def build_potential_halls(self):

        hall_size_mod = random.randint (2,4)
        n = Hallway (self.rect.x  ,self.rect.y - Map.default_room_size * hall_size_mod , Map.default_room_size , Map.default_room_size * hall_size_mod, "north" )
        e = Hallway (self.rect.x + Map.default_room_size  , self.rect.y   , Map.default_room_size * hall_size_mod,  Map.default_room_size,  'east')
        s = Hallway (self.rect.x , self.rect.y + Map.default_room_size  , Map.default_room_size ,  Map.default_room_size * hall_size_mod ,'south')
        w = Hallway (self.rect.x - Map.default_room_size *hall_size_mod , self.rect.y , Map.default_room_size * hall_size_mod, Map.default_room_size, 'west')
        possible_sprites.add(n,e,s,w)

        return [n,e,s,w]

    def deter_extreme_hall_pos(hall, entry):

        if Room.entry.entry_roll == 1: #north
            if hall.rect.y <= entry.rect.y:
                return 10 
            else:
                return 0
        if Room.entry.entry_roll == 2: #east
            if hall.rect.x >= entry.rect.x:
                return 10    
            else:
                return 0
        if Room.entry.entry_roll == 3: #south
            if hall.rect.y >= entry.rect.y:
                return 10     
            else:
                return 0
        if Room.entry.entry_roll == 4: #west
            if hall.rect.x <=  entry.rect.x:
                return 10
            else:
                return 0

    def select_hallway(last_direction):

        #iterate through each hallway option
        for hall in possible_sprites:
            #create the potential hall

            #check to see if potential hall goes out of bounds#good
            ph_boundary_test = pygame.sprite.spritecollide(hall, boundary_sprites, False)
            if ph_boundary_test:
                hall.ph_weight -= 100
            if not ph_boundary_test:
                hall.ph_weight += 0

            #check for neighbors
            Map.create_check_blocks(hall)

            next_door_wall_check = pygame.sprite.groupcollide(check_sprites, hall_sprites, False, False) # should sneak this back under map
            if next_door_wall_check:
                if (len(next_door_wall_check)) >1:
                    hall.ph_weight -= 1000
                else:
                    hall.ph_weight += 1   
            check_sprites.empty()

            second_mod = 1 #maybedelete

            #check to see if last direction is current direction, if so weight it
            if hall.direction == last_direction:
                hall.ph_weight -= random.randint (0,2)
            else:
                hall.ph_weight -= random.randint (0,2)

            #check to see if there's a collision with an exisiting hall 
            ph_hall_collision_test =  pygame.sprite.spritecollide(hall, hall_sprites, False)
            if ph_hall_collision_test:
                hall.ph_weight -= random.randint (3,5)
            if not ph_hall_collision_test:
                hall.ph_weight += random.randint (0,1)

            #and the same thing but for the entry hall if it hits the entry room, kill that hall with fire
            ph_entry_test = pygame.sprite.spritecollide(hall, entry_sprite, False,)
            if ph_entry_test:
                hall.ph_weight -= 10000

        #give positive weight for halls going away from the intial spawn room
        #also if the hall is way past the walls n/e/s/w side depending on on entry roll, squash it too
            if entry.entry_roll == 1:
                hall.ph_weight -= Hallway.deter_extreme_hall_pos(hall, entry)
                if last_direction == "south":
                    hall.ph_weight += random.randint (0,2)
            #east
            if entry.entry_roll == 2:
                hall.ph_weight -= Hallway.deter_extreme_hall_pos(hall, entry)
                if last_direction == "west":
                    hall.ph_weight += random.randint (0,2)
            # south
            if entry.entry_roll == 3:
                hall.ph_weight -= Hallway.deter_extreme_hall_pos(hall, entry)
                if last_direction == "north":
                    hall.ph_weight += random.randint (0,2)
            #west
            if entry.entry_roll == 4:
                hall.ph_weight -= Hallway.deter_extreme_hall_pos(hall, entry)
                if last_direction == "east":
                    hall.ph_weight += random.randint (0,2)

        #and if it collides with the parking lot, nuke it
        parking_lot_test = pygame.sprite.spritecollide (hall, parking_lot_sprites, False)
        if parking_lot_test:
            hall.ph_weight -= 10

        #and select the biggest one #covert it to a  list first seems like the easiest way
        possible_hall_list = []
        for hall in possible_sprites:
            possible_hall_list.append((hall.rect, hall.ph_weight, hall.direction))

        possible_hall_list.sort(key=lambda x:x[1], reverse= True)
        #create roll if positive - which is the sum of the first two potential hall list's weighed numbers
        # if its positive, make it 1 so that it could be either the first or the 2nd in the list
        if (possible_hall_list[0][1] + possible_hall_list[1][1]) >0:
            roll_if_pos = 1
        else:
            roll_if_pos = 0

        #select the hall - either the first or second entry
        hall_att = possible_hall_list [random.randint (0,roll_if_pos)]
        hall = Hallway (hall_att[0][0],hall_att[0][1],hall_att[0][2], hall_att[0][3], hall_att[2])
        hall_sprites.add (hall)
        #and delete the potential hall sprites
        possible_sprites.empty()

        return hall

    def plot_hallway(first_hall):
    #build a hallway set if we have a less than the required amount of hallways

        if len(hall_sprites) >20:
            return

        else:
            Hallway.build_potential_halls (first_hall)
            hall = Hallway.select_hallway(first_hall.direction)

            for x in range (random.randint(1,5)):
                Hallway.build_potential_halls (hall)
                hall = Hallway.select_hallway(entry.direction)
                hall_random_roll = random.randint(1,5)
                if hall_random_roll >3:
                    first_hall = hall

            return Hallway.plot_hallway(first_hall)

class Room(pygame.sprite.Sprite):

    room_list = []

    def __init__(self,posx, posy,x,y):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((x,y))
        self.image.fill(Map.anchor)  
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.room_size = None
        self.horizontal_door_count = 1
        self.vertical_door_count = 1
        self.horizontal_door_attempts = 1
        self.vertical_door_attempts = 1
        self.east_grow = True
        self.west_grow = True
        self.south_grow = True
        self.north_grow = True
        self.collided_room = None
        self.door_list = []

    def create_parking_lot(roll_number, entry):
        height =  entry.rect.height * 3
        width = entry.rect.width  * 3

        if roll_number == 1: #n
            parking_lot = Room (entry.rect.x - height/ 3 ,entry.rect.y -height, width,height)
        if roll_number == 2: #e
            parking_lot = Room (entry.rect.x + entry.rect.width ,entry.rect.y - height/ 3 , width,height)
        if roll_number == 3: #s
            parking_lot = Room (entry.rect.x - width /3 ,entry.rect.y  + entry.rect.height, width,height)
        if roll_number == 4: #w
            parking_lot = Room (entry.rect.x - width ,entry.rect.y - height / 3 , width,height)

        parking_lot.image.fill ((200,0,0))
        parking_lot_sprites.add(parking_lot)

    def calculate_door_amount(self):

        #horizontal
        if self.rect.width > Map.hall_thin:
            repeat = random.randint(1,2)
        else:
            repeat = random.randint (1,1)
        self.horizontal_door_count = repeat
        self.horizontal_door_attempts = repeat * 2

        #vertical
        if room.rect.height > Map.hall_thin:
            repeat = random.randint(1,2)
        else:
            repeat = random.randint(1,1)
        self.vertical_door_count = repeat
        self.vertical_door_attempts = repeat * 2

    def initial_room_placement(self):
        #determine the approrpirate aammout of potential rooms
        ns_repeat = 1
        if self.rect.width > Map.hall_thin:
            ns_repeat = random.randint(1,2)

        #create the sprite
        for ns in range(ns_repeat):
            n = Room(random.randrange (self.rect.x + Map.wall_width, self.rect.x + self.rect.width - (Map.wall_width *1) ,Map.wall_width), self.rect.y - (Map.wall_width * 2), Map.wall_width, Map.wall_width)
            n.south_grow = False
            s = Room(random.randrange (self.rect.x + Map.wall_width, self.rect.x + self.rect.width - (Map.wall_width *1) ,Map.wall_width), self.rect.y + (self.rect.height) + Map.wall_width, Map.wall_width, Map.wall_width)
            s.north_grow = False
            possible_room_sprites.add (n,s)

        we_repeat = 1
        if self.rect.height > Map.hall_thin:
            we_repeat = random.randint(1,2)

        #create the sprite
        for we in range(we_repeat):
            e = Room (self.rect.x + (self.rect.width ) + Map.wall_width   ,random.randrange(self.rect.y + Map.wall_width, self.rect.y + self.rect.height - Map.wall_width ,Map.wall_width) , Map.wall_width, Map.wall_width)
            e.west_grow = False
            w = Room (self.rect.x - (Map.wall_width) - Map.wall_width, random.randrange(self.rect.y + Map.wall_width, self.rect.y + self.rect.height - Map.wall_width ,Map.wall_width) , Map.wall_width, Map.wall_width)
            w.east_grow = False
            possible_room_sprites.add (e,w)

        return n,e,s,w

    def create_initial_room(self):

        n,e,s,w = Room.initial_room_placement(self)

        #i can clean this up with a group collide but it's being weird
        n_check = Room.hall_collision_check(n)
        if n_check == False:
            self.orientation = 'n'
            room_sprites.add(n)
        e_check =Room.hall_collision_check(e)
        if e_check == False:
            self.orientation = 'e'
            room_sprites.add(e)
        s_check = Room.hall_collision_check(s)
        if s_check == False:
            self.orientation = 's'
            room_sprites.add(s)
        w_check = Room.hall_collision_check(w)
        if w_check == False:
            self.orientation = 'w'
            room_sprites.add(w)

    def hall_collision_check(potential_room):

        hall_collision_test = ( pygame.sprite.spritecollide(potential_room, hall_sprites, False) 
                             or pygame.sprite.spritecollide(potential_room, entry_sprite, False))

        if hall_collision_test:
            return True
        else: 
            return False # if it's false, keep on growing

    def room_collision_check(potential_room):
        room_collision_test = pygame.sprite.spritecollide(potential_room, room_sprites, False)

        if room_collision_test:
            potential_room.collided_room = room_collision_test
            return True
        else:
            return False

    def parking_lot_collision_check(potential_room):
        parking_lot_test = pygame.sprite.spritecollide(potential_room, parking_lot_sprites, False)
        if parking_lot_test:
            potential_room.collided_room = parking_lot_test
            return True
        else:
            return False

    def delete_small_collided_room(self):

        for room in self.collided_room:
            if room.rect.height < Map.default_room_size + Map.wall_width or room.rect.width < Map.default_room_size + Map.wall_width:
                pygame.sprite.Sprite.kill(room)
                self.east_grow, self.west_grow, self.north_grow, self.south_grow = True, True, True, True

    def grow_room_space (self):

        #first make a copy of the sprite, and kill the original sprite
        #and kill the original sprite
        pygame.sprite.Sprite.kill(self)   

        if self.north_grow == True:
            self.rect.height += Map.wall_width
            self.rect.y -= Map.wall_width
            collision = Room.hall_collision_check(self)
            room_collision = Room.room_collision_check(self)
            parking_collision = Room.parking_lot_collision_check(self)
            if collision or room_collision or parking_collision: 
                #go back to the last position
                self.rect.height -= Map.wall_width 
                self.rect.y += Map.wall_width 
                self.north_grow = False

                if self.collided_room:
                    Room.delete_small_collided_room(self)

        if self.south_grow == True:
            self.rect.height +=Map.wall_width 
            collision = Room.hall_collision_check(self)
            room_collision = Room.room_collision_check(self)
            parking_collision = Room.parking_lot_collision_check(self)
            if collision or room_collision or parking_collision:     
                self.rect.height -= Map.wall_width 
                self.south_grow = False

                if self.collided_room:
                    Room.delete_small_collided_room(self)

        if self.east_grow == True:
            self.rect.width += Map.wall_width
            collision = Room.hall_collision_check(self)
            room_collision = Room.room_collision_check(self)
            parking_collision = Room.parking_lot_collision_check(self)
            if collision or room_collision or parking_collision:
                self.rect.width -= Map.wall_width
                self.east_grow = False

                if self.collided_room:
                    Room.delete_small_collided_room(self)

        if self.west_grow == True:
            self.rect.x -= Map.wall_width
            self.rect.width += Map.wall_width
            collision = Room.hall_collision_check(self)
            room_collision = Room.room_collision_check(self)
            parking_collision = Room.parking_lot_collision_check(self)
            if collision or room_collision or parking_collision:     
                self.rect.x += Map.wall_width 
                self.rect.width -= Map.wall_width   
                self.west_grow = False

                if self.collided_room:
                    Room.delete_small_collided_room(self)

        #stop the room from getting too small
        if self.north_grow == False and self.south_grow == False and self.east_grow == False and self.west_grow == False:
            if self.rect.width <= Map.default_room_size - Map.wall_width or self.rect.height <= Map.default_room_size - Map.wall_width :
                return #maybe I can cycle this back in and make it grow, but for now this'll do

        new_room = Room( self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        new_room.east_grow, new_room.west_grow, new_room.north_grow, new_room.south_grow = self.east_grow, self.west_grow, self.north_grow, self.south_grow
        room_sprites.add (new_room)

    def assign_room_size(self):
        room_size = room.rect.height * room.rect.width
        binary_room_roll = random.randint(0,1)

        if room_size <= Map.default_room_size:
            self.room_size = 'small'
        if room_size > Map.default_room_size * 100 and room_size <= Map.default_room_size * 800:
            self.room_size = "medium"
            if room_size <Map.default_room_size * 300:
                if binary_room_roll ==1:
                    self.room_size = "medium"
            if room_size > Map.default_room_size * 300:
                if binary_room_roll == 1:
                    self.room_size = "large"
        if room_size > Map.default_room_size * 800:
            self.room_size = "large"

    def assign_room_type(self):

        room_choices = []

        #put each room type in the room choices list if it makes sense
        #if there's too many offices, delete it
        if self.room_size == "small":
            if Map.room_type_count.get("kitchen") < Map.room_type_count.get("bathroom"):
                room_choices.append(Map.room_type_dict.get('kitchen'))
                room_choices.append(Map.room_type_dict.get('bathroom'))
                room_choices.append(Map.room_type_dict.get('office'))
                room_choices.append(Map.room_type_dict.get('closet'))

            if Map.room_type_count.get("locker") < Map.room_type_count.get("kitchen"):
                room_choices.append(Map.room_type_dict.get('locker'))

        if self.room_size == "medium":
            if Map.room_type_count.get("locker") < Map.room_type_count.get("kitchen"):
                room_choices.append(Map.room_type_dict.get('locker'))
            if Map.room_type_count.get("kitchen") < Map.room_type_count.get("bathroom"):
                room_choices.append(Map.room_type_dict.get('kitchen'))
            room_choices.append(Map.room_type_dict.get('office'))

        if self.room_size == "large":
            room_choices.append(Map.room_type_dict.get('storage'))
            room_choices.append(Map.room_type_dict.get('industry'))

        # if there's too many choices, take out the office if appropriate
        if (Map.room_type_dict.get('office')) in room_choices:
            if len(room_choices) >1:
                if sum(Map.room_type_count.values()) > 8:
                    if (Map.room_type_count['office']) / sum(Map.room_type_count.values()) > 0.4: # if it's more than 40 percent
                        room_choices.remove (Map.room_type_dict.get('office'))

        if len(room_choices) == 0:
            room_choices.append(Map.room_type_dict.get('closet')) #fix this, too small room

        room_picked = random.choice(room_choices)
        self.image.fill (room_picked)
       
        #and update the count
        room_key = [key for key, value in Map.room_type_dict.items() if value == room_picked][0]
        Map.room_type_count[room_key] += 1

    def trim_room(self):
        #first make a copy of the sprite, and kill the original sprite
        # and kill the original sprite
        pygame.sprite.Sprite.kill(self) 

        #adjust the size/position
        self.rect.height -= Map.wall_width
        self.rect.width -= Map.wall_width
        self.rect.y += Map.wall_width / 2
        self.rect.x += Map.wall_width / 2

        new_room = Room( self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        Room.assign_room_size(new_room)
        Room.assign_room_type(new_room)

        room_sprites.add (new_room)

class Door(Map):

    #door variables
    door_size = Map.wall_width * 2
    door_size_long =  Map.wall_width * 3
    door = (192,192,192)

    def __init__(self,x,y, width, height):
        super().__init__()
        self.image = pygame.Surface((width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.orientation = None
        self.cardinal = None
        self.image.fill  ((200,200,200))
        self.room_check = True

    def check_doors(door):

        #make sure it connects with at least 2 rooms $toot
        room_collide_test = pygame.sprite.spritecollide (door, room_sprites, False)
        if len(room_collide_test) < 2:
            door.room_check = False

        #or one room and one door
        hall_collide_test = pygame.sprite.spritecollide(door,hall_sprites, False)
        if len(room_collide_test) >= 1 and len(hall_collide_test) >= 1:
            door.room_check = True

        #check for a door
        door_collide = pygame.sprite.spritecollide(door, door_sprites, False)
        if door_collide:
            door.room_check = False

        #check to make sure the door doesn't extend past any room it hits
        if door.orientation == 'vertical':
            for room in room_collide_test:
                if door.rect.top <= room.rect.top:
                    door.room_check = False
                if door.rect.bottom > room.rect.bottom:
                    door.room_check = False

                #do one more check to see if the door isn't too low or to high
                if door.rect.bottom > (room.rect.bottom + Map.wall_width) or door.rect.top < (room.rect.top + Map.wall_width):
                    door.room_check = False

            for hall in hall_collide_test:
                if door.rect.top <= hall.rect.top:
                    door.room_check = False
                if door.rect.bottom > hall.rect.bottom:
                    door.room_check = False

        if door.orientation == 'horizontal':
            for room in room_collide_test:
                if door.rect.left <= room.rect.left:
                    door.room_check = False
                if door.rect.right > room.rect.right:
                    door.room_check = False

                #do one more check to see if the door isn't too low or to high
                if door.rect.right > (room.rect.right - Map.wall_width) or door.rect.left < (room.rect.left + Map.wall_width):
                    door.room_check = False

            for hall in hall_collide_test:
                if door.rect.left <= hall.rect.left:
                    door.room_check = False
                if door.rect.right > hall.rect.right:
                    door.room_check = False



    def create_vertical_doors(room): 

        x = room.rect.right
        y =random.randint (room.rect.top + Map.wall_width * 2, room.rect.bottom - Door.door_size)
        east_door = Door(x - Map.wall_width ,y, Door.door_size_long , Door.door_size)
        east_door.orientation = 'vertical'
        Door.check_doors(east_door)

        x = room.rect.left - Map.wall_width
        y =random.randint (room.rect.top + Map.wall_width * 2, room.rect.bottom - Door.door_size)
        west_door = Door(x - Map.wall_width ,y, Door.door_size_long , Door.door_size)
        west_door.orientation = 'vertical'
        Door.check_doors(west_door)

        if room not in entry_sprite:
            if east_door.room_check == True:
                room.door_list.append(east_door)

            if west_door.room_check == True:
                room.door_list.append(west_door)

    def create_horizontal_doors(room):
        y = room.rect.top - Map.wall_width * 2
        x =random.randint (room.rect.left + Map.wall_width * 2 , room.rect.right - Door.door_size)
        north_door = Door(x - Map.wall_width ,y, Door.door_size , Door.door_size_long)
        north_door.orientation = 'horizontal'
        Door.check_doors(north_door)

        y = room.rect.bottom - Map.wall_width 
        x =random.randint (room.rect.left + Map.wall_width * 2, room.rect.right - Door.door_size)
        south_door = Door(x - Map.wall_width ,y, Door.door_size , Door.door_size_long)
        south_door.orientation = 'horizontal'
        Door.check_doors(south_door)

        if room not in entry_sprite:
            if north_door.room_check == True:
                room.door_list.append(north_door)

            if south_door.room_check == True:
                room.door_list.append(south_door)

    def choose_doors(room):

        vertical_list = [d for d in room.door_list if d.orientation == 'vertical' ]
        horizontal_list = [d for d in room.door_list if d.orientation == 'horizontal']

        if len(vertical_list) <  room.vertical_door_count:
            room.vertical_door_count = len(vertical_list)

        if len(horizontal_list) <  room.horizontal_door_count:
            room.horizontal_door_count = len(horizontal_list)

        vertical_choices = random.sample(vertical_list, room.vertical_door_count)
        horizontal_choices = random.sample(horizontal_list, room.horizontal_door_count)

        door_sprites.add(horizontal_choices)
        door_sprites.add(vertical_choices)

    
    def create_entry_rooms(entry): 

        door_list = ((entry.rect.right - Map.wall_width ,entry.rect.centery - Door.door_size /2, Door.door_size_long , Door.door_size),
                    (entry.rect.left - Map.wall_width - Map.wall_width ,entry.rect.centery - Door.door_size /2 , Door.door_size_long , Door.door_size),
                    (entry.rect.centerx - Map.wall_width ,entry.rect.top - Map.wall_width * 2, Door.door_size , Door.door_size_long),
                    (entry.rect.centerx - Map.wall_width ,entry.rect.bottom - Map.wall_width , Door.door_size , Door.door_size_long))

        for dl in door_list:
            x,y,width, height = dl[0],dl[1], dl[2],dl[3]
            entry_door = Door(x,y,width, height)

            test = pygame.sprite.spritecollide(entry_door, hall_sprites, False)
            if test :
                door_sprites.add(entry_door)

class Wall(Map):

    def __init__(self, width,height, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        if width  * height > 0:
            self.image = pygame.Surface((width,height))
            self.valid = True
        else:
            self.image = pygame.Surface((0,0))
            self.valid = False
        self.image.fill((0,0,0))  
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    def check_door_collision( wall):

        #check for a door - if there is build walls around it
        door_collision =  pygame.sprite.spritecollide(wall, door_sprites, False)
        return door_collision

    def check_valid_wall(width,height):
        if width * height > 0:
            return True
        else:
            return False

    def create_vertical_walls(self,room):
        proto_east_wall = Wall(Map.wall_width, room.rect.height - Map.wall_width, room.rect.left , room.rect.top)
        proto_west_wall = Wall(Map.wall_width, room.rect.height - Map.wall_width, room.rect.right - Map.wall_width, room.rect.top )
        horizontal_walls = [proto_east_wall,proto_west_wall]

        for wall in horizontal_walls:
            door_collisions = Wall.check_door_collision(wall)

            segments = len(door_collisions)
            for collision in range(segments): 
                door = door_collisions[collision]
                if collision == 0: # if it's the first one
                    next_wall = Wall(wall.rect.width,  door.rect.top - room.rect.top , wall.rect.x, room.rect.y )
                    if next_wall.valid == True:
                        wall_sprites.add(next_wall)

                if collision == segments-1: #last one
                    next_wall = Wall(wall.rect.width , room.rect.bottom - door.rect.bottom , wall.rect.x, door.rect.bottom )
                    if next_wall.valid == True:
                        wall_sprites.add(next_wall)

                else:

                    next_door = door_collisions[collision + 1] 
                    next_wall = Wall(Map.wall_width , next_door.rect.top- door.rect.bottom , wall.rect.left, door.rect.bottom )
                    if next_wall.valid == True:
                        wall_sprites.add(next_wall)

            if segments == 0 :
                next_wall = Wall(wall.rect.width, wall.rect.height + Map.wall_width   , wall.rect.x, wall.rect.y )
                wall_sprites.add(next_wall)

    def create_horizontal_walls(self,room):
        proto_north_wall = Wall(room.rect.width, Map.wall_width, room.rect.left, room.rect.top )
        proto_south_wall = Wall(room.rect.width, Map.wall_width, room.rect.left, room.rect.bottom)
        vertical_walls = [proto_north_wall, proto_south_wall]

        for wall in vertical_walls:
            door_collisions = Wall.check_door_collision(wall)

            segments = len(door_collisions)
            for collision in range(segments): 
                door = door_collisions[collision]

                if collision == 0: # if it's the first one
                    next_wall = Wall(door.rect.right - room.rect.left, Map.wall_width,room.rect.left, door.rect.top + Map.wall_width)
                    if next_wall.valid == True:
                        wall_sprites.add(next_wall)

                if collision == segments-1: #last 'one
                    next_wall = Wall(room.rect.right - door.rect.left, Map.wall_width,door.rect.left, door.rect.top + Map.wall_width )
                    if next_wall.valid == True:
                        wall_sprites.add(next_wall)

                else:
                    next_door = door_collisions[collision + 1] 
                    next_wall = Wall( next_door.rect.left - door.rect.right, Map.wall_width , door.rect.right ,door.rect.top + Map.wall_width)
                    if next_wall.valid == True:
                        wall_sprites.add(next_wall)

            if segments == 0 :
                next_wall = Wall(room.rect.width, Map.wall_width,wall.rect.x, wall.rect.y  )
                wall_sprites.add(next_wall)

#create boundaries
Map.create_boundaries

#create entry
entry = Entry_Room()
Entry_Room.create_entry(entry)
Entry_Room.check_around_entry(entry)

entry.direction = "n/a"
Room.entry = entry

#build the halls
Hallway.plot_hallway(entry)
Entry_Room.shuffle_entry_pos(entry)

#and the doors for hte entry
Door.create_entry_rooms(entry)

# #now build the rooms
for hall in hall_sprites:
    Room.create_initial_room(hall)

#and expand the rooms
#determine the amount of growth cycles
grow_cycles = random.randint (20,35)

#grow the room
for rgi in range (grow_cycles):
    for room in room_sprites:
        Room.grow_room_space(room)

#trim the room and assign size/room types
for room in room_sprites:
    room_proto_wall= Wall(0,0,0,0)

    Room.trim_room(room)

room_sprites.add(entry_sprite)

#and add doors
for room in room_sprites:
    Room.calculate_door_amount(room) #figure out how many doors to make
    for d in range (room.vertical_door_count):
        Door.create_vertical_doors(room)
    for d in range (room.horizontal_door_count):
        Door.create_horizontal_doors(room)

    Door.choose_doors(room)

# #build walls for entry room
intitial_entry_wall= Wall(0,0,0,0)
intitial_entry_wall.create_vertical_walls(entry)
intitial_entry_wall.create_horizontal_walls(entry)

#build walls for rooms
for room in room_sprites:
    intitial_entry_wall= Wall(0,0,10,10)
    intitial_entry_wall.create_vertical_walls(room)
    intitial_entry_wall.create_horizontal_walls(room)

#add entry sprite
def get_entry_sprites():
    return entry

def get_sprites(sprite_group):
    for sprite in sprite_group:
        sprite.posx = sprite.rect.right
        sprite.posy = sprite.rect.bottom

    return sprite_group

#export all the sprite lists
hall_sprites = get_sprites(hall_sprites)
room_sprites = get_sprites(room_sprites)
door_sprites = get_sprites(door_sprites)

# #add the sprites
all_sprites.add(entry_sprite) 
all_sprites.add(hall_sprites)
all_sprites.add(room_sprites)
all_sprites.add(guide_walls)
all_sprites.add(wall_sprites)
all_sprites.add(door_sprites)

#main game loop
game_continue = True
while game_continue:
    clock.tick(fps_rate)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_continue = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprites in all_sprites:
                sprites.rect.x += Map.wall_width * 5
        if keys[pygame.K_RIGHT]:
            for sprites in all_sprites:
                sprites.rect.x -= Map.wall_width * 5
        if keys[pygame.K_UP]:
            for sprites in all_sprites:
                sprites.rect.y += Map.wall_width * 5
        if keys[pygame.K_DOWN]:
            for sprites in all_sprites:
                sprites.rect.y -= Map.wall_width * 5
        if keys[pygame.K_ESCAPE]:
            game_continue = False

    all_sprites.update()

    win.fill((231,226,211))
    all_sprites.draw(win)
    pygame.display.flip()

#{'office': 29, 'closet': 0, 'storage': 5, 'kitchen': 0, 'bathroom': 0, 'industry': 3, 'locker': 0}


