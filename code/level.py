import pygame 
from tiles import Tile, StaticTile, Enemy
from settings import tile_size, screen_width
from player import Player
from particles import ParticleEffect
# from enemy import Enemy
from support import import_csv_layout, import_cut_graphics

class Level:
	def __init__(self,level_data,surface):
		
		# level setup
		self.display_surface = surface 
		self.setup_level(level_data)
		self.world_shift = 0
		self.current_x = 0

		# terrain setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
		enemy_layout = import_csv_layout(level_data['enemy'])
		self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemy')

		# dust 
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		# background
		self.bg_shift = 0
		bg = pygame.image.load('../graphics/Background/background.png').convert()
		self.bg = pygame.transform.scale(bg, (bg.get_width() * 4, bg.get_height() * 2))
		self.bg_rect = bg.get_rect(topleft=(0, 0))

	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.dust_sprite.add(fall_dust_particle)

	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index,row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = int(col_index * tile_size)
					y = int(row_index * tile_size)

					if type == 'terrain':
						# sprite = Tile(tile_size,x,y,self.display_surface)
						# sprite_group.add(sprite)
						terrain_tile_list = import_cut_graphics('../graphics/tiles/Mossy Tileset/Mossy_-_TileSet_edited.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)

					if type == 'enemy':
						# terrain_tile_list = import_cut_graphics('../graphics/tiles/Mossy Tileset/Mossy_-_TileSet_edited.png')
						# tile_surface = terrain_tile_list[int(val)]
						# sprite = StaticTile(tile_size, int(x), int(y), tile_surface)
						sprite = Enemy(tile_size,x,y)


					sprite_group.add(sprite)
		return sprite_group

	def setup_level(self,layout):
		self.tiles = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()
		self.enemies = pygame.sprite.Group()

		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				
				if cell == 'X':
					tile = Tile((x,y),tile_size)
					self.tiles.add(tile)
				if cell == 'P':
					player_sprite = Player((x,y),self.display_surface,self.create_jump_particles)
					self.player.add(player_sprite)
				if cell == 'Q':
					enemy_sprite = Enemy((x,y+75))
					self.enemies.add(enemy_sprite)

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.bg_shift = 2
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.bg_shift = -2
			self.world_shift = -8
			player.speed = 0
		else:
			self.bg_shift = 0
			self.world_shift = 0
			player.speed = 8

	def bg_update(self):
		self.bg_rect.x += self.bg_shift

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def enemy_collision(self):
			player = self.player.sprite
			for enemy in self.enemies.sprites():
				enemy.animate()
				if enemy.rect.colliderect(player) and player.status == 'attack':
					enemy.kill()

	def run(self):
		# dust particles 
		# self.dust_sprite.update(self.world_shift)
		# self.dust_sprite.draw(self.display_surface)

		# level tiles
		self.bg_update()
		self.display_surface.blit(self.bg, self.bg_rect)
		# self.tiles.update(self.world_shift)
		# self.tiles.draw(self.display_surface)
		# self.scroll_x()

		self.terrain_sprites.draw(self.display_surface)
		self.terrain_sprites.update(self.world_shift)
		self.enemy_sprites.draw(self.display_surface)

		# player
		# self.player.update()
		# self.horizontal_movement_collision()
		# self.get_player_on_ground()
		# self.vertical_movement_collision()
		# self.create_landing_dust()
		# self.player.draw(self.display_surface)

		# self.enemy_collision()
		# self.enemies.update(self.world_shift)
		# self.enemies.draw(self.display_surface)
