# https://github.com/gerryjenkinslb/blit_article/blob/main/three_blits.py
# https://stackoverflow.com/questions/66665946/what-is-the-difference-between-pygame-sprite-and-surface
#https://www.youtube.com/watch?v=j2OhRUGQ1M8
import pygame

clock = pygame.time.Clock()
fps_rate = 30

blue = (0,0,200)
red = (150,0,0)

screen_width = 800
screen_height = 600

import random

# camera_width = int (screen_width/2)
# camera_height = int (screen_height/2)

pygame.init()
win = pygame.display.set_mode((screen_width, screen_height))

class Screen():

	screen_width = 800
	screen_height = 600

	def blit_screen():
		pass

		# win.blit(surface1, (0, 0))
		# win.blit(surface2, (0, 0))


class Thief (pygame.sprite.Sprite):

	def __init__(self,colour,posx, posy, name):

		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((22,22))
		self.image.fill(colour)  
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0
		self.posx = posx #actual position in the world
		self.posy = posy #actual position in the world
		self.name = name

	def move(self, keys):
		if keys[pygame.K_LEFT]:
			for sprites in all_sprites:
				self.posx += 5
		if keys[pygame.K_RIGHT]:
			for sprites in all_sprites:
				self.posx-=5
		if keys[pygame.K_UP]:
			for sprites in all_sprites:
				self.posy += 5
		if keys[pygame.K_DOWN]:
			for sprites in all_sprites:
				self.posy -= 5

class Camera():

	def __init__(self):

		self.height = int
		self.width = int
		self.x = int
		self.y = int
		self.color = (random.randint(1,100),2,100)
		self.player = 0

	def set_screen_size(self, players):
		if players == 1:
			self.width = Screen.screen_width
			self.height = Screen.screen_height
		if players == 2:
			self.width = Screen.screen_width
			self.height = Screen.screen_height / 2
		if players == 3 or players == 4:
			self.width = Screen.screen_width / 2
			self.height = Screen.screen_height / 2

	def set_screen_position(self, players, player):
		pos_list = { 1: (0,0),
					2 : [(0,0), (0, screen_height/ 2) ],
					3 : [(0,0),(screen_width/2, 0),(0, screen_height/ 2),( screen_width/2, screen_height/ 2)]}

		if players == 1:
			self.x = pos_list[1][0]
			self.y = pos_list[1][1]
		if players == 2:
			self.x = pos_list[2][player-1][0]
			self.y = pos_list[2][player-1][1]
		else:
			self.x = pos_list[3][player-1][0]
			self.y = pos_list[3][player-1][1]

	def create_surface(self):
		surface = pygame.Surface((self.width, self.height))
		surface.fill((self.color))
		return surface

	def calculate_offset(sprite, thief_sprite):
		x = thief_sprite.posx - sprite.posx
		y = thief_sprite.posy - sprite.posy

		print (x,y)

		return {'x' : x, 'y': y}

	def blit_action(self,surface, sprites, thief_sprite,camera):
		
		for sprite in sprites:
			if sprite == thief_sprite:
				sprite.rect.x = int (camera.width/2) 
				sprite.rect.y = int (camera.height/2)
			else:
				offset = Camera.calculate_offset(sprite, thief_sprite)
				sprite.rect.x = offset['x'] + int (camera.width/2)
				sprite.rect.y = offset['y'] + int (camera.height/2)

		# for sprite in all_sprites:
		# 	offset = Camera.calculate_offset(sprite, thief_sprite) 

		# 	if sprite == thief_sprite:

		# 		sprite.rect.x = int (camera.width/2)
		# 		sprite.rect.y = int (camera.height/2)


		# 	else:

		# 		sprite.rect.x = thief_sprite.posx + offset['x']
		# 		sprite.rect.y =  thief_sprite.posy + offset['y']

		all_sprites.draw(surface)
		win.blit(surface, (self.x, self.y))

players = 2

camera1 = Camera()
camera1.set_screen_size(players)
camera1.set_screen_position(players,1)

camera2 = Camera()
camera2.set_screen_size(players)
camera2.set_screen_position(players,2)


gio = Thief(red,50,50, 'butt')
big_jim =Thief (blue,50,50, 'head')

thief_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

thief_sprites.add(gio)  # Add Thief sprite to the group
thief_sprites.add(big_jim)

all_sprites.add(thief_sprites)

# Main game loop
running = True
while running:
	clock.tick(fps_rate)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	keys = pygame.key.get_pressed()
	gio.move(keys)

	# # Create a new surface each frame
	surface1 = camera1.create_surface()
	surface2 = camera2.create_surface()

	camera1.blit_action(surface1, all_sprites, gio, camera1)
	camera2.blit_action(surface2, all_sprites, big_jim, camera2)

	# Update the display
	pygame.display.flip()

pygame.quit()

