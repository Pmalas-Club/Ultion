import pygame

from tiles import StaticTile
from settings import tile_size, screen_width, screen_height
from player import Player
from particles import ParticleEffect
from enemy import Enemy
from support import import_csv_layout, import_cut_graphics

class Level:
	def __init__(self,level_data,surface,get_health,set_health):
		# level setup
		self.display_surface = surface 
		self.world_shift = 0
		self._current_x = 0

		# player
		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.get_health = get_health
		self.set_health = set_health
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout)

		# dust 
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		# terrain setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

		# enemy setup
		enemy_layout = import_csv_layout(level_data['enemy'])
		self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemy')

		# background
		self.bg_shift = 0
		bg = pygame.image.load(level_data['background']).convert()
		if level_data['level'] == 1 or level_data['level'] == 3:
			self.bg = pygame.transform.scale(bg, (bg.get_width() * 2.2, bg.get_height() * 3))
		if level_data['level'] == 2:
			self.bg = pygame.transform.scale(bg, (bg.get_width() / 1.5, bg.get_height() / 1.42))
		self.bg_rect = bg.get_rect(topleft=(0, 0))

		self.map  = pygame.image.load(level_data['bg']).convert_alpha()
		self.map_rect = self.map.get_rect(topleft=(0, 0))
  
		self.over  = pygame.image.load(level_data['over']).convert_alpha()
		self.over_rect = self.over.get_rect(topleft=(0, 0))

		self.collidable_sprites = self.terrain_sprites.sprites()

	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,35)
		else:
			pos += pygame.math.Vector2(10,-35)
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
				offset = pygame.math.Vector2(10,50)
			else:
				offset = pygame.math.Vector2(-10,50)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.dust_sprite.add(fall_dust_particle)

	def player_setup(self, layout):
		for row_index,row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = int(col_index * tile_size)
				y = int(row_index * tile_size)
				if val == '0':
					sprite = Player((x,y), self.display_surface, self.create_jump_particles, 100)
					self.player.add(sprite)
					#self.health_bar = HealthBar(100, 50, sprite.get_hp(), sprite.max_hp)
				elif val == '1':
					v_surface = pygame.image.load('../graphics/Icons/goal.png').convert_alpha()
					sprite = StaticTile(tile_size, x, y, v_surface)
					sprite.image = pygame.transform.scale(sprite.image, (sprite.image.get_width(), sprite.image.get_height()))
					self.goal.add(sprite)

	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index,row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = int(col_index * tile_size)
					y = int(row_index * tile_size)

					if type == 'terrain':
						tile_surface = pygame.image.load('../graphics/tiles/collision.png').convert_alpha()
						sprite = StaticTile(tile_size, x, y, tile_surface)

					if type == 'enemy':
						sprite = Enemy(tile_size,x,y,'Bandit',5)


					sprite_group.add(sprite)
		return sprite_group

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

	def map_update(self):
		self.map_rect.x += self.world_shift
	def over_update(self):
		self.over_rect.x += self.world_shift

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.on_left = True
					self._current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self._current_x = player.rect.right

		if player.on_left and (player.rect.left < self._current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self._current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.collidable_sprites:
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
			for enemy in self.enemy_sprites.sprites():
				if enemy.rect.colliderect(player):
					enemy.attack_animation()
					if player.status == 'attack' and player.attack_frame_index >= 2:
						enemy.death_animation()
				
				if enemy.status == 'attack':
					if (enemy.rect.centerx + 100) <= player.rect.centerx or (enemy.rect.centerx - 100) >= player.rect.centerx:
						enemy.idle_animation()

				# if enemy.rect.colliderect(player) and player.status == 'attack':
				# 	if player.attack_frame_index >= 2:
				# 		enemy.death_animation()
				if enemy.status == 'death' and enemy.frame_index >= 9:
					enemy.kill()

	def finish(self):
		if self.goal.sprite.rect.colliderect(self.player.sprite):
			if not self.enemy_sprites:
				return True
		else:
			return False

	def lose(self):
		player = self.player.sprite
		if player.rect.y > screen_height or self.get_health() < 1:
			return True
		else:
			return False

	def run(self):
		# level tiles
		self.bg_update()
		self.display_surface.blit(self.bg, self.bg_rect)

		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)

		self.map_update()
		self.display_surface.blit(self.map, self.map_rect)


		self.enemy_collision()
		
		self.enemy_sprites.update(self.world_shift, self.player.sprite, self.set_health)
		self.enemy_sprites.draw(self.display_surface)

		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)

		# PLAYER
		self.player.update()
		self.horizontal_movement_collision()
		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.create_landing_dust()

		#self.health_bar.draw(self.display_surface, self.player.sprite.get_hp())
		self.player.draw(self.display_surface)
		self.goal.update(self.world_shift)
		self.over_update()
		self.display_surface.blit(self.over, self.over_rect)
		self.scroll_x()
		self.goal.draw(self.display_surface)