import pygame, sys
from settings import screen_width, screen_height
from level import Level
from game_data import *
from ui import HealthBar

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game_active = False
is_victory = False
is_lose = False
levels = [level_0, level_1, level_2]
level_index = 0

# INTRO
title_font = pygame.font.Font('../font/Pixeltype.ttf', 100)
title = title_font.render('ULTION', False, 'lightblue')
title_rect = title.get_rect(center=(400,300))

instruction_font = pygame.font.Font('../font/Pixeltype.ttf', 50)

start_instruction = instruction_font.render('START!', False, 'black')
start_instruction_rect = start_instruction.get_rect(center=(400,450))

exit_instruction = instruction_font.render('EXIT', False, 'black')
exit_instruction_rect = exit_instruction.get_rect(center=(400,600))

victory = title_font.render('YOU WIN!', False, 'white')
victory_rect = victory.get_rect(center=(int(screen_width / 2),120))

lose = title_font.render('YOU LOSE!', False, 'white')
lose_rect = victory.get_rect(center=(int(screen_width / 2),120))

# WALLPAPER
wallpaper = pygame.image.load('../graphics/wallpaper/wallpaper.jpg').convert()
wallpaper = pygame.transform.scale_by(wallpaper, 1.7)
wallpaper_rect = wallpaper.get_rect(topleft=(0,0))

# # MUSIC
intro_game = pygame.mixer.Sound('../sounds/intro/intro.mp3')
lagu_intro = False
backsound = pygame.mixer.Sound('../sounds/play_scene/play_scene.mp3')
	
class Ultion:
	def __init__(self):
		self.__max_health = 100
		self.__health = 100
		self.score = 0
		self.health_bar = HealthBar(100, 50, self.__health, self.__max_health)

		self.level_index = 0
		self.level = None

		self.game_active = False
		self.is_victory = False
		self.is_lose = False
	# Health Abstraction
	def get_health(self):
		return self.__health
	def set_health(self, val):
		self.__health += val
	def run(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if start_instruction_rect.collidepoint(event.pos):
					self.game_active = True
					self.level = Level(levels[level_index],screen,self.get_health,self.set_health)
					self.is_victory = False
					self.is_lose = False
					intro_game.stop()
					backsound.play()
				elif exit_instruction_rect.collidepoint(event.pos):
					sys.exit()
		if self.game_active:
			self.level.run()
			self.health_bar.draw(screen,self.__health)
			self.is_victory = self.level.finish()
			self.is_lose = self.level.lose()
			if self.is_victory:
				if self.level_index == len(levels)-1:
					self.game_active = False
					self.__health = 100
				else:
					self.__health = self.level.get_health()
					self.level_index += 1
					self.level = None
					self.level = Level(levels[self.level_index],screen,self.get_health,self.set_health)
			if self.is_lose:
				self.game_active = False
				self.__health = 100
				self.score = 0
		else:
			screen.blit(wallpaper,wallpaper_rect)
			screen.blit(title, title_rect)
			if self.is_victory:
				screen.blit(victory, victory_rect)
				backsound.stop()
			elif self.is_lose:
				screen.blit(lose, lose_rect)
				backsound.stop()
			
			global lagu_intro
			if not lagu_intro:
				intro_game.play(-1)
				lagu_intro = True
			screen.blit(start_instruction, start_instruction_rect)
			screen.blit(exit_instruction, exit_instruction_rect)

game = Ultion()

while True:
	game.run()

	pygame.display.update()
	clock.tick(60)