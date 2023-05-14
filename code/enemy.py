import pygame
from tiles import AnimatedTile
from random import randint
class Enemy(AnimatedTile):
	def __init__(self, size, x, y):
		super().__init__(size, x, y, '../graphics/Bandit/Idle')
		self.rect.y -= size
		self.speed = randint(3,5)

	def move(self):
		self.rect.x += self.speed

	def update(self, shift):
		self.rect.x += shift
		self.animation()
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