import pygame
import SHAT_map_gen_v2

class Thief (pygame.sprite.Sprite):

	name_list = ["Gio", "Big Jim", "Alex Tryhard", "Trevor"]
	default_control_scheme = {'up' : pygame.K_w, 'down' : pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d}
	player_size = int (SHAT_map_gen_v2.Map.wall_width * 0.6)
	acceleration = int (player_size / 2)
	max_speed = player_size * 2

	def __init__(self,colour,posx, posy, name):

		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((Thief.player_size,Thief.player_size))
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
		self.acceleration = pygame.math.Vector2(0,0)
		self.velocity = pygame.math.Vector2(0,0)
		self.speed = 0.3
		self.friction = -.09
		self.direction = 'neutral'
		self.controls_frozen = False
		self.butt = Thief.player_size

	def bounce(self):
		pass

	def detect_collision(self,sprite_group,camera):

		# print (self.posx, self.posy)

		collisions = pygame.sprite.spritecollide (self, sprite_group, False)
		if collisions :
			for collision in collisions:
				#left
				if self.velocity.x >= 0:
					if 0 <= collision.rect.right - self.rect.left  <= 5:
						self.velocity.x, self.velocity.y = 0, 0
						self.posx = collision.posx - collision.rect.width	

				#right
				if self.velocity.x <0 :
					if -1 <= self.rect.right - collision.rect.left  <= 5:
						self.velocity.x, self.velocity.y = 0, 0
						self.posx = collision.posx + Thief.player_size

				# #up
				if self.velocity.y >= 0:
					if 0 < collision.rect.bottom -self.rect.top <=5:
						self.velocity.x, self.velocity.y = 0, 0
						self.posy = collision.posy - collision.rect.height

				# # down
				if self.velocity.y <=0:
					if -1 <= self.rect.bottom - collision.rect.top  <= 5:
						self.velocity.x, self.velocity.y = 0, 0
						self.posy = collision.posy + Thief.player_size


	def assign_control_scheme(self):
		if self.control_method == 'keyboard':
			if  self.player_number == 2:
				self.control_scheme = {'up' : pygame.K_UP, 'down' : pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT }
			if self.player_number == 3 or self.player_number == 4:
				self.control_scheme = {'up' : pygame.K_0 , 'down' : pygame.K_1 , 'left': pygame.K_2 , 'right': pygame.K_3  }

	def stop_player(self):
		if self.velocity.x != 0 or self.velocity.y != 0:

			if -0.1 <= self.velocity.x <= 0.1:
				self.velocity.x = 0

			if -0.1 <= self.velocity.y <= 0.1:
				self.velocity.y = 0

	def horizontal_move(self, keys, event, delta_time, ):
		self.acceleration.x = 0
		self.acceleration.y = 0

		for key_pressed, key_code in self.control_scheme.items():
			if keys[key_code]:
				if key_pressed == 'left':
					self.acceleration.x += self.speed
					self.direction = 'left'
				if key_pressed == 'up':
					self.acceleration.y += self.speed
					self.direction = 'up'
					
				if key_pressed == 'down':
					self.acceleration.y -= self.speed
					self.direction = 'down'
				if key_pressed == 'right':
					self.acceleration.x -= self.speed
					self.direction = 'right'

		self.acceleration.x += self.velocity.x * self.friction
		self.velocity.x += self.acceleration.x * delta_time
		self.posx  += self.velocity.x * delta_time + (self.acceleration.x * .5) * (delta_time * delta_time)

		self.acceleration.y += self.velocity.y * self.friction
		self.velocity.y += self.acceleration.y * delta_time
		self.posy  += self.velocity.y * delta_time + (self.acceleration.x * .5) * (delta_time * delta_time)

		self.stop_player()

