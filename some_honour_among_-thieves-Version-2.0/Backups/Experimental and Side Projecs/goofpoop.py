import pygame
import random

screen_height = 1000
screen_width = 1000

#initiialize display and import display settings
pygame.init()
pygame.mixer.init()
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Some Honor Among Thieves - Map - Test")
clock = pygame.time.Clock()

# sprite lists
all_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()
room_sprites = pygame.sprite.Group()
way_sprites = pygame.sprite.Group()
hall_sprites = pygame.sprite.Group()



    
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


#room list - too be updated with randomly generated list



rooms = (
        (100,100, 50,50, industry),
        (100,100,100,50, kitchen),
        (100,100,150,50, hallway),
        (100,100,200,50, main_entry),
        )





list_list = []

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
        
    list_length = len (rooms) 
    def draw():

        for room in rooms:
            x = room[0]
            y = room[1]
            posx = room[2]
            posy = room[3]
            col = room[4]

            for rooms2 in rooms:
                x2 = room[0]
                y2 = room[1]
                posx2 = room[2]
                posy2 = room[3]
                col2 = room[4]

                print (rooms2)

                

                
            
            r = Room(x,y,posx, posy, col)
            room_sprites.add(r)

            room_hit = pygame.sprite.spritecollide(r, room_sprites, False)
            list_list.append ((room_hit,posx,posy))
            
        all_sprites.add(hall_sprites, room_sprites)


        


#make loop - if bottom of door == top of room thats not a hallway, delete that sprite

Room.draw()

#main game loop
game_continue = True
while game_continue:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_continue = False

    all_sprites.update()

    win.fill((231,226,211))
    all_sprites.draw(win)
    pygame.display.flip()

pygame.quit()
