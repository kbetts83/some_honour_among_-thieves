
		collisions = pygame.sprite.spritecollide (self, sprite_group, False)
		if collisions :
			collision = collisions[0]

			#right
			if (collision.posx + self.rect.width) + self.posx > 1:
				print ('right')

			# #left
			# if (collision.posx - collision.rect.width) - self.posx < 1:
			# 	print ('left')

			# if self.acceleration.y > 0 and self.acceleration.x > 0:
			# 	self.posx = collision.posx - collision.rect.width
			# 	self.posy = collision.posy - collision.rect.height
			# 	self.acceleration.x, self.velocity.x = 0 ,0
			# 	self.acceleration.y, self.velocity.y = 0 ,0

			# if self.acceleration.y > 0:
			# 	self.posy = collision.posy - collision.rect.height
			# 	self.acceleration.x, self.velocity.x = 0 ,0
			# 	self.acceleration.y, self.velocity.y = 0 ,0

			# 	pass
			# 	# self.posy = collision.posy + Thief.player_size
			# 	# # self.acceleration.y, self.velocity.y = 0 ,0
			# 	# self.acceleration.x, self.velocity.x = 0 ,0
			# 	# collision.image.fill((200,0,0))  

			# if self.acceleration.x > 0:
			# 	self.posx = collision.posx - collision.rect.width
			# 	self.acceleration.x, self.velocity.x = 0 ,0
			# 	self.acceleration.y, self.velocity.y = 0 ,0

			# if self.direction == 'right':
			# 	self.rect.right = collision.rect.left

			# 	# self.posx = collision.posx + Thief.player_size
			# 	# self.acceleration.x, self.velocity.x = 0 ,0
			# 	# # self.acceleration.y, self.velocity.y = 0 ,0
			# 	# # collision.image.fill((200,0,0))  



			# print (collision.rect)
