import pygame 
from support import import_folder
class Tile(pygame.sprite.Sprite):
	def __init__(self,size,x,y):
		super().__init__()
		# self.image = pygame.image.load('../graphics/tiles/1.png').convert_alpha()
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect(topleft = (x,y))

	def update(self,x_shift):
		self.rect.x += x_shift

class StaticTile(Tile):
	def __init__(self, size, x, y, surface):
		super().__init__(size, x, y)
		self.image = surface

class Enemy(StaticTile):
	def __init__(self, size, x, y):
		super().__init__(size, x, y, pygame.image.load('../graphics/Bandit/Attack/0.png').convert_alpha())
		offset_y = y + 75
		self.image = pygame.transform.scale_by(self.image, 3)
		self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class AnimatedTile(Tile):
	def __init__(self, size, x, y, path):
		super().__init__(size, x, y)
		self.frames = import_folder(path)
