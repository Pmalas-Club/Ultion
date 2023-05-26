from tiles import AnimatedTile
from random import randint
from support import import_folder

class Enemy(AnimatedTile):
	def __init__(self, size, x, y, character, damage):
			super().__init__(size, x, y, f'../graphics/{character}/Idle')
			self.character = character
			self.rect.y -= size + 10
			self.fix_pos_x = x 
			self.status = 'idle'
			self.__damage = damage # private

	def attack_animation(self):
		self.frames = import_folder(f'../graphics/{self.character}/Attack')
		self.status = 'attack'

	def hit_attack(self, set_health):
		set_health(-self.__damage)

	def idle_animation(self):
		self.frames = import_folder(f'../graphics/{self.character}/Idle')
		self.status = 'idle'

	def death_animation(self):
		self.frames = import_folder(f'../graphics/{self.character}/Death')
		self.status = 'death'

	# Overriding polymorphism to AnimatedTile
	def update(self, shift, target, set_health):
		self.rect.x += shift
		self.fix_pos_x += shift
		self.animation()
		if self.status == 'attack' and self.frame_index == 4.5:
			self.hit_attack(set_health)
			target.hurt_scene = True			