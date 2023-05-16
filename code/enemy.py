from tiles import AnimatedTile
from random import randint
from support import import_folder

class Enemy(AnimatedTile):
	def __init__(self, size, x, y, damage):
			super().__init__(size, x, y, '../graphics/Bandit/Idle')
			self.rect.y -= size + 10
			self.fix_pos_x = x 
			self.status = 'idle'
			self.__damage = damage # private

	def attack_animation(self):
		self.frames = import_folder('../graphics/Bandit/Attack')
		self.status = 'attack'

	def hit_attack(self, target):
		target.set_hp(-self.__damage)

	def idle_animation(self):
		self.frames = import_folder('../graphics/Bandit/Idle')
		self.status = 'idle'

	def death_animation(self):
		self.frames = import_folder('../graphics/Bandit/Death')
		self.status = 'death'
		print(self.frame_index)

	# Overriding polymorphism to AnimatedTile
	def update(self, shift, target):
		self.rect.x += shift
		self.fix_pos_x += shift
		self.animation()
		if self.status == 'attack' and self.frame_index == 4.5:
			self.hit_attack(target)
			target.hurt_scene = True			