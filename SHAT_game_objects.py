import pygame
import random

class Spawn_Points():


	char_width = 10 #this is dirty, fix this
	buffer = int (char_width / 2)
	wall_width = 56 #fix this  

	def create_entry_spawn( entry_sprite):

		if entry_sprite.orientation == 'north' or entry_sprite.orientation == 'south':
			starting_x = entry_sprite.rect.right - Spawn_Points.wall_width
			starting_y = entry_sprite.rect.top + Spawn_Points.buffer + Spawn_Points.wall_width

			if entry_sprite.orientation == "south":
				starting_y += entry_sprite.rect.height

			spawn_points = {
			1: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			2: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			3: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			4: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			5: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			6: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			}

		if entry_sprite.orientation == 'east' or entry_sprite.orientation == 'west':
			starting_x = entry_sprite.rect.right 
			starting_y = entry_sprite.rect.bottom

			if entry_sprite.orientation == "west":
				starting_x -= entry_sprite.rect.width - Spawn_Points.buffer
				pass

			spawn_points = {
			1: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			2: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			3: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			4: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			5: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			6: {'posx': starting_x, 'posy': starting_y, 'taken': False},
			}

		entry_sprite.spawn_points = spawn_points

	def assign_spawn_location( entry_sprite):

		selecting = True
		while selecting == True:
			location = entry_sprite.spawn_points[random.randint(1,6)]
			if location['taken'] != True:
				location['taken'] = True
				selecting = False

		location = {'posx': location['posx'], 'posy': location['posy'], 'taken': False}

		# location_chosen = {'posx': starting_x, 'posy': starting_y, 'taken': False}

		return location
