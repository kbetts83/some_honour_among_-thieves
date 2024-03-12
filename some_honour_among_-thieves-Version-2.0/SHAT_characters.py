import pygame

class Thief (pygame.sprite.Sprite):

	name_list = ["Gio", "Big Jim", "Alex Tryhard", "Trevor"]
	default_control_scheme = {'up' : pygame.K_w, 'down' : pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d}

	def __init__(self,colour,posx, posy, name):

		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10,10))
		self.image.fill(colour)  
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0
		self.posx = posx #actual position in the world
		self.posy = posy #actual position in the world
		self.name = name
		self.player_number = int
		self.camera_number = int
		self.control_method = 'keyboard'
		self.control_scheme = Thief.default_control_scheme
		self.direction = 'neutral'

	def assign_control_scheme(self):
		if self.control_method == 'keyboard':
			if  self.player_number == 2:
				self.control_scheme = {'up' : pygame.K_UP, 'down' : pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT }
			if self.player_number == 3 or self.player_number == 4:
				self.control_scheme = {'up' : pygame.K_0 , 'down' : pygame.K_1 , 'left': pygame.K_2 , 'right': pygame.K_3  }

	def move(self, keys, event):

# Check if any key from the control scheme is pressed
		for key_pressed, key_code in self.control_scheme.items():
			if keys[key_code]:
				if key_pressed == 'up':
					self.posy += 1
				if key_pressed == 'down':
					self.posy -= 1
				if key_pressed == 'left':
					self.posx -= 1
				if key_pressed == 'right':
					self.posx += 1

		#resnt to neutral
		if event.type == pygame.KEYUP:
			self.direction = 'neutral'
