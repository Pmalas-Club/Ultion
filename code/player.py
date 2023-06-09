import pygame 
from support import import_folder

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface,create_jump_particles, max_hp):
		super().__init__()
		self.import_character_assets()

		self.frame_index = 0
		self.attack_frame_index = 0
		self.attack_scene = False
		self.hurt_frame_index = 0
		self.hurt_scene = False
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(center = pos)



		# dust particles 
		self.import_dust_run_particles()
		self.dust_frame_index = 0
		self.dust_animation_speed = 0.15
		self.display_surface = surface
		self.create_jump_particles = create_jump_particles

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0.8
		self.jump_speed = -16
		self.set_attack = False

		# player status
		self.status = 'idle'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

		#load sound
		self.jump_sound = pygame.mixer.Sound('../sounds/character/jump_1.mp3')
		self.landing_sound = pygame.mixer.Sound('../sounds/character/landing.mp3')
		self.attack_sound = pygame.mixer.Sound('../sounds/character/slash.mp3')
		self.hurt_sound = pygame.mixer.Sound('../sounds/character/get hurt.mp3')
		self.in_air = False

	def import_character_assets(self):
		character_path = '../graphics/character/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[], 'attack':[], 'Hurt':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def import_dust_run_particles(self):
		self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

	def animate(self):
		animation = self.animations[self.status]
		self.frame_index += self.animation_speed
		if self.status == 'attack':
			self.attack_scene = True
			done = self.attack_animation(animation)
			if not done:
				return
			else:
				self.attack_frame_index = 0
				self.attack_scene = False
				self.frame_index = 0
				return

		if self.hurt_scene:		
			self.status = 'Hurt'
			done = self.hurt_animation(animation)
			if not done:
				return
			else:
				self.hurt_frame_index = 0
				self.hurt_scene = False
				self.status = 'idle'
				self.frame_index = 0
				return
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		if self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image, True, False)
			self.image = flipped_image

		# set the rect
		if self.on_ground and self.on_right:
			self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
		elif self.on_ground and self.on_left:
			self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
		elif self.on_ground:
			self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
		elif self.on_ceiling and self.on_right:
			self.rect = self.image.get_rect(topright=self.rect.topright)
		elif self.on_ceiling and self.on_left:
			self.rect = self.image.get_rect(topleft=self.rect.topleft)
		elif self.on_ceiling:
			self.rect = self.image.get_rect(midtop=self.rect.midtop)

	def attack_animation(self, frame):
		self.attack_frame_index += 0.15
		if self.attack_frame_index > len(frame):
			return True
		image = frame[int(self.attack_frame_index)]
		if self.attack_frame_index == 1.05:
			self.attack_sound.play()
		if self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image, True, False)
			self.image = flipped_image

		self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
		
		# if self.attack_frame_index >= 1:
		# 	self.attack_sound.play()

		return False

	def hurt_animation(self, frame):
		self.hurt_frame_index += 0.15
		if self.hurt_frame_index > len(frame):
			return True
		image = frame[int(self.hurt_frame_index)]
		if self.hurt_frame_index == 0.3:
			self.hurt_sound.play()
		if self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image, True, False)
			self.image = flipped_image

		self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
		return False

	def run_dust_animation(self):
		if self.status == 'run' and self.on_ground:
			self.dust_frame_index += self.dust_animation_speed
			if self.dust_frame_index >= len(self.dust_run_particles):
				self.dust_frame_index = 0

			dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

			if self.facing_right:
				pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
				self.display_surface.blit(dust_particle,pos)
			else:
				pos = self.rect.bottomright - pygame.math.Vector2(6,10)
				flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
				self.display_surface.blit(flipped_dust_particle,pos)

	def get_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:
			self.set_attack = True
		elif keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.facing_right = True
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.facing_right = False
		else:
			self.direction.x = 0
			self.set_attack = False

		if keys[pygame.K_UP] and self.on_ground:
			self.jump()
			self.create_jump_particles(self.rect.midbottom)

	def get_status(self):
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if self.direction.x != 0:
				self.status = 'run'
			elif self.set_attack:
				self.status = 'attack'
			elif self.hurt_scene:
				self.status = 'Hurt'
			else:
				self.status = 'idle'

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jump_speed
		self.jump_sound.play()
		self.in_air = True


	def update(self):
		self.get_input()
		self.get_status()

		#saat landing
		if self.in_air and self.on_ground:
			self.landing_sound.play()
			self.in_air = False
		if self.attack_scene:
			self.status = 'attack'
		self.animate()
		self.run_dust_animation()
