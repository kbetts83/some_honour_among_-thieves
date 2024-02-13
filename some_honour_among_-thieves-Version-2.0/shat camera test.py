# https://github.com/gerryjenkinslb/blit_article/blob/main/three_blits.py
# https://stackoverflow.com/questions/66665946/what-is-the-difference-between-pygame-sprite-and-surface
#https://www.youtube.com/watch?v=j2OhRUGQ1M8
import pygame

thief_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()
fps_rate = 30

blue = (0,0,200)
red = (150,0,0)
yellow = (255, 255, 0)
green = (0,255,0)

color_list = [blue, red, yellow, green]

# screen_width = 800
# screen_height = 600

import random

class Setup():

	screen_width = 800
	screen_height = 600

	def __init__ (self):
		self.player_camera_surface_list = []

	def setup_player_list(self,number_of_players, thief_sprites):
		
		for player in range(number_of_players):
			#set up thief, camera and surface
			thief = Thief(color_list[player], 0 ,0 , Thief.name_list[player])
			thief_sprites.add(thief)

			camera= Camera()
			camera.set_screen_size(number_of_players)
			camera.set_screen_position(number_of_players,player)

			self.player_camera_surface_list.append ({'thief': thief, 'camera' : camera})


class Thief (pygame.sprite.Sprite):

	name_list = ["Gio", "Big Jim", "Alex Tryhard", "Trevor"]

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
		self.player_number = int
		self.camera_number = int

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
			self.width = Setup.screen_width
			self.height = Setup.screen_height
		if players == 2:
			self.width = Setup.screen_width
			self.height = Setup.screen_height / 2
		if players == 3 or players == 4:
			self.width = Setup.screen_width / 2
			self.height = Setup.screen_height / 2

	def set_screen_position(self, players, player):

		pos_list = { 1: (0,0),
					2 : [(0,0), (0, Setup.screen_height/ 2) ],
					3 : [(0,0),(Setup.screen_width/2, 0),(0, Setup.screen_height/ 2),( Setup.screen_width/2, Setup.screen_height/ 2)]}

		if players == 1:
			self.x = 0
			self.y = 0
		if players == 2:
			self.x = pos_list[2][player-1][0]
			self.y = pos_list[2][player-1][1]
		if players == 3 or players == 4:
			self.x = pos_list[3][player-1][0]
			self.y = pos_list[3][player-1][1]

	def create_surface(self):
		surface = pygame.Surface((self.width, self.height))
		surface.fill((self.color))
		return surface

	def calculate_offset(sprite, thief_sprite):
		x = thief_sprite.posx - sprite.posx
		y = thief_sprite.posy - sprite.posy

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

		all_sprites.draw(surface)
		win.blit(surface, (self.x, self.y))

pygame.init()
win = pygame.display.set_mode((Setup.screen_width, Setup.screen_height))

number_of_players = 4

setup = Setup()
setup.setup_player_list(number_of_players,thief_sprites)

#add sprites to all sprite list
all_sprites.add(thief_sprites)


# Main game loop
running = True
while running:
	clock.tick(fps_rate)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	keys = pygame.key.get_pressed()

	for player in range(number_of_players):

		current_player = setup.player_camera_surface_list[player]
		# if current_player['thief'].name == "Gio":
		# 	player['thief'].move(keys)


		thief = current_player['thief']
		camera = current_player['camera']

		surface = camera.create_surface()

		camera.blit_action(surface, all_sprites, thief, camera)

	# Update the display
	pygame.display.flip()

pygame.quit()

