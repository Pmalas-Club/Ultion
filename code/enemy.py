import pygame
from tiles import AnimatedTile
from random import randint
from support import import_folder

class Enemy(AnimatedTile):
	def __init__(self, size, x, y):
			super().__init__(size, x, y, '../graphics/Bandit/Idle')
			self.rect.y -= size
			self.speed = randint(2,5)
			self.fix_pos_x = x 
			self.follow_pos_x = 0
			self.status = 'idle'
			
	def move(self):
		self.rect.x += self.speed
  
	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image, True, False)
   
	def reverce(self):
		self.speed *= -1
  
	def patrol(self):
		if self.rect.x > self.fix_pos_x + 100 or self.rect.x < self.fix_pos_x - 100:
			self.reverce()

	def attack_animation(self):
		self.frames = import_folder('../graphics/Bandit/Attack')

	def update(self, shift):
		self.rect.x += shift
		self.fix_pos_x += shift
		self.animation()
		self.reverse_image()
		self.patrol()
		self.move()

























# import pygame
# from support import import_folder
#
# class Enemy(pygame.sprite.Sprite):
# 	def __init__(self,pos):
# 		super().__init__()
# 		self.import_character_assets()
# 		self.image = pygame.image.load('../graphics/Bandit/Attack/0.png').convert_alpha()
# 		self.image = pygame.transform.scale_by(self.image,4)
# 		self.rect = self.image.get_rect(midbottom = pos)
# 		self.status = 'Idle'
# 		self.direction = pygame.math.Vector2(0,0)
# 		self.frame_index = 0
# 		self.animation_speed = 0.15
# 	def update(self,x_shift):
# 		self.rect.x += x_shift
#
# 	def import_character_assets(self):
# 		character_path = '../graphics/Bandit/'
# 		self.animations = {'Attack':[],'Death':[],'Hurt':[],'Idle':[]}
#
# 		for animation in self.animations.keys():
# 			full_path = character_path + animation
# 			self.animations[animation] = import_folder(full_path)
# 			for count, value in enumerate(self.animations[animation]):
# 				self.animations[animation][count] = pygame.transform.scale_by(value,2)
# 	def get_status(self):
# 		if self.direction.y < 0:
# 			self.status = 'jump'
# 		elif self.direction.y > 1:
# 			self.status = 'fall'
# 		else:
# 			if self.direction.x != 0:
# 				self.status = 'run'
# 			elif self.set_attack:
# 				self.status = 'attack'
# 			else:
# 				self.status = 'idle'
#
# 	def animate(self):
# 		animation = self.animations[self.status]
# 		self.frame_index += self.animation_speed
# 		if self.status == 'attack':
# 			self.attack_scene = True
# 			done = self.attack_animation(animation)
# 			if not done:
# 				return
# 			else:
# 				self.attack_frame_index = 0
# 				self.attack_scene = False
# 		if self.frame_index >= len(animation):
# 			self.frame_index = 0
#
# 		image = animation[int(self.frame_index)]
# 		self.image = image
		# if self.facing_right:
		# 	self.image = image
		# else:
		# 	flipped_image = pygame.transform.flip(image, True, False)
		# 	self.image = flipped_image

	#def update(self):
		# self.get_input()
		# self.get_status()
		# if self.attack_scene:
		# 	self.status = 'attack'
		# self.animate()
        # self.run_dust_animation()