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

        for room in room_list:
            x = room[0]
            y = room[1]
            posx = room[2]
            posy = room[3]
            col = room[4]
            
            r = Room(x,y,posx, posy, col)
            
            if col == (100,100,150):
                hall_sprites.add(r)

            else:
                room_sprites.add(r)
                
            all_sprites.add(hall_sprites, room_sprites)
            room_and_hall_sprites.add (hall_sprites, room_sprites)
  
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
          
            
                #add to the horizontal waypoint list

                #shift spot over by 10, detect if there's any collision
                #if there is a collision, shift it back 10 over to it's original spot
                #if there's not a collision, it's on the edge of the map, shift if over so it's in the middle

            if col == (100,100,150):

                if x > y:

                    #check left side
                    check_left = Waypoint (10, 10, posx - 10 , posy + y/2  , Waypoint.wp)
                    check_sprites.add (check_left)

                    left_way_col = pygame.sprite.spritecollide(check_left, hall_sprites, False)

                    if left_way_col:
                        
                        way = Waypoint (10, 10, posx , posy + y/2  , Waypoint.wp)
                        way_sprites.add(way)

                        pygame.sprite.Sprite.kill(check_left)

                    else:

                        way = Waypoint (10, 10, posx + 25 , posy + y/2  , Waypoint.wp)
                        way_sprites.add (way)
                        pygame.sprite.Sprite.kill(check_left)


                    #check right side
                    check_right = Waypoint (10, 10, posx+x + 10, posy + y/2,Waypoint.wp)
                    check_sprites.add (check_right)

                    right_way_col = pygame.sprite.spritecollide(check_right, hall_sprites, False)

                    if right_way_col:

                        way =   Waypoint (10, 10, posx+x , posy + y/2,Waypoint.wp)
                        way_sprites.add (way)
                        pygame.sprite.Sprite.kill(check_right)

                    else:

                        way =   Waypoint (10, 10, posx+x - 25 , posy + y/2,Waypoint.wp)
                        way_sprites.add (way)
                        pygame.sprite.Sprite.kill(check_right)


                #add the vertical waypoint list
                if y > x:

                    #check top
                    check_top = Waypoint (10, 10, posx + x/2, posy + 10 , Waypoint.wp)
                    check_sprites.add (check_top)

                    top_way_col = pygame.sprite.spritecollide(check_top, hall_sprites, False)

                    if top_way_col:

                        way =   Waypoint (10, 10, posx + x/2, posy   , Waypoint.wp)
                        way_sprites.add (way)

                        pygame.sprite.Sprite.kill(check_top)

                    else:

                        way =   Waypoint (10, 10, posx + x/2, posy -25  , Waypoint.wp)
                        way_sprites.add (way)

                        pygame.sprite.Sprite.kill(check_top)

                    #check bottom

                    check_bot = Waypoint(10, 10, posx + x/2, posy + y + 10   , Waypoint.wp)
                    check_sprites.add (check_bot)

                    bot_way_col = pygame.sprite.spritecollide(check_bot, hall_sprites, False)

                    if bot_way_col:

                        way =   Waypoint (10, 10, posx + x/2, posy + y  , Waypoint.wp)
                        way_sprites.add (way)

                        pygame.sprite.Sprite.kill(check_bot)

                    else:
                        
                        way =   Waypoint (10, 10, posx + x/2, posy+y -25   , Waypoint.wp)
                        way_sprites.add (way)

                        pygame.sprite.Sprite.kill(check_bot)

                all_sprites.add(way_sprites)

        #delete walls that collide with waypoints
        wayp_wall_col = pygame.sprite.groupcollide(way_sprites, wall_sprites, False, True)


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

        for w in range (0, len (room_list)):
            current_room = room_list[w]
            x =    current_room [0]
            y=     current_room [1]
            posx = current_room [2]
            posy = current_room [3]
            col =  current_room [4]

            wall_list.append ((x, Wall.wall_width, posx, posy, Wall.wall))
            wall_list.append ((x, Wall.wall_width, posx, (posy+ y) , Wall.wall))
            wall_list.append ((x, Wall.wall_width, posx, posy+ y , Wall.wall))
            wall_list.append ((Wall.wall_width, y , (posx+ x), posy , Wall.wall))

            w1 = Wall (x, Wall.wall_width, posx, posy, Wall.wall)
            w2 = Wall (x, Wall.wall_width, posx, (posy+ y ) , Wall.wall)
            w3 = Wall (Wall.wall_width, y, posx, posy , Wall.wall)
            w4 = Wall (Wall.wall_width, y+Wall.wall_width, (posx+ x ), posy , Wall.wall)

            wall_sprites.add (w1, w2, w3, w4)

            #add to the waypoint list 
            all_sprites.add (wall_sprites)



            
class Door(pygame.sprite.Sprite):

    door = (237, 252, 146)
    
    def __init__(self, way_pos_x,way_pos_y):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill (Door.door)
        self.rect = self.image.get_rect()
        self.rect.x = way_pos_x
        self.rect.y = way_pos_y


    def create_door():

        possible_door_list = []


        for d in range (0, len (room_list)):
            current_room = room_list[d]
            x =    current_room [0]
            y=     current_room [1]
            posx = current_room [2]
            posy = current_room [3]
            col =  current_room [4]

            #resent counters
            extra_door = 0

        
            #roll to decide if the room gets an extra +1 room

            extra_door_roll = random.randint (1,10)
            if extra_door_roll >= 8:
                extra_door = 1

            #if it's not a hallway, calculate the area of the room and decide how many doors that room should have.
            if col != (100,100,150):

                room_area = x * y
                
                if map.small_room_area[0] <= room_area <= map.small_room_area[1]:
                    room_doors = 1 + extra_door

                if map.med_room_area[0] <= room_area <= map.med_room_area[1]:
                    room_doors = 2 + extra_door
                    
                if map.large_room_area[0] <= room_area <= map.large_room_area[1]:
                    room_doors = 3 + extra_door

                #check to see if the room hits a hallway.
                #if it hits a hallway, that should be the default door if there's only one door
                # then check to see if the door hits at least 2 rooms, if it does, plaace a temporary door there as well
                # unless that door hits more than 2 walls

                north_door = [random.randint (posx + Wall.wall_width , posx + x - Wall.wall_width *3), posy  - Wall.wall_width]
                south_door = [random.randint (posx + Wall.wall_width , posx + x - Wall.wall_width *3), posy + y - Wall.wall_width]
                east_door =  [posx+x - Wall.wall_width, random.randint (posy + Wall.wall_width * 3, posy + y - Wall.wall_width)]
                west_door =  [posx - Wall.wall_width, random.randint (posy + Wall.wall_width * 3, posy + y - Wall.wall_width)]

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
                        possible_door_list.append ((d, door_entry, col))

                    else:
                        door_room_check = pygame.sprite.spritecollide(door, room_sprites, False)
                        if (len(door_room_check)) > 1:
                            possible_door_sprites.add (door)
                            all_sprites.add (door)
                            possible_door_list.append ((d, door_entry, col))

                    #fix this up - find a way to try and move the sprite
                    room_wall_check = pygame.sprite.spritecollide(door, wall_sprites, False)
                    if  (len(room_wall_check)) > 2:
                        pygame.sprite.Sprite.kill (door)
                        possible_door_list.remove ((d, door_entry, col))

        print (possible_door_list)



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
                if self.x_speed < 0 :
                    self.rect.left = wa.rect.right

            if self.player_dir == "y":
                if self.y_speed > 0:
                    self.rect.bottom = wa.rect.top
                if self.y_speed < 0 :
                    self.rect.top = wa.rect.bottom

        self.x_speed = 0
        self.y_speed = 0


Room.draw()
Wall.create_wall()
Door.create_door()
Waypoint.hall_waypoint()



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
