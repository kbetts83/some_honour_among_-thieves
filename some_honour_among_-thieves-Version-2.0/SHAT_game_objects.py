import pygame
import random

class Spawn_Points():

	char_width = 10 #this is dirty, fix this

	def create_entry_spawn( entry_sprite):

		entry_sprite.orientation = 'west'

		if entry_sprite.orientation == 'north' or entry_sprite.orientation == 'south':
			starting_x = entry_sprite.posx
			starting_y = entry_sprite.posy

			if entry_sprite.orientation == "south":
				starting_y -= entry_sprite.rect.height - (Spawn_Points.char_width *2 )

			spawn_points = {
			1: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			2: {'posx': starting_x - Spawn_Points.char_width , 'posy': starting_y, 'taken': False},
			3: {'posx': starting_x - (Spawn_Points.char_width * 2) , 'posy': starting_y, 'taken': False},
			4: {'posx': starting_x, 'posy': starting_y - Spawn_Points.char_width , 'taken': False},
			5: {'posx': starting_x - Spawn_Points.char_width , 'posy': starting_y - Spawn_Points.char_width, 'taken': False},
			6: {'posx': starting_x - (Spawn_Points.char_width * 2), 'posy': starting_y - Spawn_Points.char_width, 'taken': False}
			}

		if entry_sprite.orientation == 'east' or entry_sprite.orientation == 'west':
			starting_x = entry_sprite.posx
			starting_y = entry_sprite.posy

			if entry_sprite.orientation == "west":
				starting_x -= entry_sprite.rect.width - (Spawn_Points.char_width *2 )

			spawn_points = {
			1: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			2: {'posx': starting_x, 'posy': starting_y - Spawn_Points.char_width , 'taken': False},
			3: {'posx': starting_x, 'posy': starting_y - (Spawn_Points.char_width * 2), 'taken': False},
			4: {'posx': starting_x - Spawn_Points.char_width , 'posy': starting_y, 'taken': False},
			5: {'posx': starting_x - Spawn_Points.char_width , 'posy': starting_y - Spawn_Points.char_width , 'taken': False},
			6: {'posx': starting_x - Spawn_Points.char_width , 'posy': starting_y - (Spawn_Points.char_width * 2), 'taken': False},
			}

		entry_sprite.spawn_points = spawn_points

	def assign_spawn_location( entry_sprite):

		selecting = True
		while selecting == True:
			location = entry_sprite.spawn_points[random.randint(1,6)]
			location = entry_sprite.spawn_points[6]
			if location['taken'] != True:
				location['taken'] = True
				selecting = False

		location_chosen = {'posx': location['posx'], 'posy': location['posy'], 'taken': True}

		return location_chosen
