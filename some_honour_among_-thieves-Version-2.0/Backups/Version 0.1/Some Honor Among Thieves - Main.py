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
door_sprites = pygame.sprite.Group()
possible_door_sprites = pygame.sprite.Group()
check_sprites = pygame.sprite.Group()

#lists for rooms, walls, etc
wall_list = []
room_list = map.rooms
way_list = []

screen_width = display.screen_width
screen_height = display.screen_height

###set up Room class
class Room (pygame.sprite.Sprite):
    col = (0,0,0,)
    
    def __init__(self,x,y,posx,posy,col):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((x , y ))
        self.image.fill(col)  # the colour
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.x = x
        self.y = y
        col = Room.col

    def draw():

        #create entryway
        room_start_pos = random.randint (1,4)
        x = 50
        y = 50

        room_start_pos = 4

        if room_start_pos == 1:
            posx =random.randrange (0,screen_width - 60,50)
            posy = 0
            
        if room_start_pos == 2:
            posx = screen_width - 60
            posy = random.randrange(0, screen_height - 100, 50)

        if room_start_pos == 3:
            posx= random.randrange(0, screen_height - 60, 50)
            posy = screen_height - 60

        if room_start_pos == 4:
            posx = 0
            posy= random.randrange(0, screen_height - 60, 50)

        room = (x,y,posx, posy,map.main_entry)
        room_list.append (room)

  
#set up waypoint class
class Waypoint (pygame.sprite.Sprite):
    wp = (0,100,100)

    def __init__(self,x,y,posx,posy,col):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10 , 10 ))
        self.image.fill(col)  # the colour
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy

    def hall_waypoint():

        wp = []
        
        #build waypoints
        #if it's a hallway, add the coordinates to the waylist map for later
        for room in room_list:
            x = room[0]
            y = room[1]
            posx = room[2]
            posy = room[3]
            col = room[4]
          
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
                
                if map.small_room_area[0] <= room_area <= map.small_room_area[1]:
                    room_doors = 1 + extra_door

                if map.med_room_area[0] <= room_area <= map.med_room_area[1]:
                    room_doors = 2 + extra_door
                    
                if map.large_room_area[0] <= room_area <= map.large_room_area[1]:
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
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((character.default_character_width , character.default_character_height))
        self.image.fill(50)  # the colour
        self.rect = self.image.get_rect()
        self.x = character.theif_x_start
        self.y = character.theif_y_start
        self.x_speed = 0
        self.y_speed = 0
        self.acceleration = 0
        self.player_dir = "unknown"

    def update(self):

        #get key input
        keys = pygame.key.get_pressed()

        #define what key inputs do
        if keys[pygame.K_LEFT] or keys[pygame.K_a] :
            self.x_speed = character.default_character_speed * -1
            self.player_dir = 'x'

        if keys[pygame.K_RIGHT] or keys[pygame.K_d] :
            self.x_speed = character.default_character_speed
            self.player_dir = 'x'

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y_speed = character.default_character_speed * -1
            self.player_dir = 'y'

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_speed = character.default_character_speed
            self.player_dir= 'y'

        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # check wall collision
        wall_col = pygame.sprite.spritecollide(self, wall_sprites, False)

        for wa in wall_col:
            if self.player_dir == "x":
                if self.x_speed > 0 :
                    self.rect.right = wa.rect.left
                    self.x_speed = 0
                if self.x_speed < 0 :
                    self.rect.left = wa.rect.right
                    self.x_speed = 0

            if self.player_dir == "y":
                if self.y_speed > 0:
                    self.rect.bottom = wa.rect.top
                    self.y_speed = 0
                if self.y_speed < 0 :
                    self.rect.top = wa.rect.bottom
                    self.y_speed = 0

        self.x_speed = 0
        self.y_speed = 0

#call classes and functions to build
Room.draw()
Wall.create_wall()
Door.create_door()

#sprite stuff and add in theifs, geo and enemies        
gio = Thief()
all_sprites.add(gio)

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
