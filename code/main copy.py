import pygame, sys
from settings import screen_width, screen_height
from level import Level
from game_data import *

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

class Ultion:
	def __init__(self) -> None:
		self.health = 100
		self.score = 0

		self.level_index = 0
		self.level = Level(levels[self.level_index],screen)

		self.game_active = False
		self.is_victory = False
		self.is_lose = False
	def run(self):
		if self.game_active:
			self.level.run()
			self.is_victory = self.level.finish()
			self.is_lose = self.level.lose()
			if self.is_victory:
				if self.level_index == len(levels)-1:
					self.game_active = False
				else:
					self.level_index += 1
					self.level = Level(levels[self.level_index],screen)
			if self.is_lose:
				game_active = False
		else:
			screen.blit(wallpaper,wallpaper_rect)
			screen.blit(title, title_rect)
			if self.is_victory:
				screen.blit(victory, victory_rect)
				backsound.stop()
			elif self.is_lose:
				screen.blit(lose, lose_rect)
				backsound.stop()
			
			if not lagu_intro:
				intro_game.play(-1)
				lagu_intro = True
			screen.blit(start_instruction, start_instruction_rect)
			screen.blit(exit_instruction, exit_instruction_rect)


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
	
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if start_instruction_rect.collidepoint(event.pos):
				game_active = True
				level = Level(levels[level_index],screen)
				is_victory = False
				is_lose = False
				intro_game.stop()
				backsound.play()
			elif exit_instruction_rect.collidepoint(event.pos):
				sys.exit()

	if game_active:
		level.run()
		is_victory = level.finish()
		is_lose = level.lose()
		if is_victory:
			if level_index == len(levels)-1:
				game_active = False
			else:
				level_index += 1
				level = Level(levels[level_index],screen)
		if is_lose:
			game_active = False
	else:
		screen.blit(wallpaper,wallpaper_rect)
		screen.blit(title, title_rect)
		if is_victory:
			screen.blit(victory, victory_rect)
			backsound.stop()
		elif is_lose:
			screen.blit(lose, lose_rect)
			backsound.stop()
		
		if not lagu_intro:
			intro_game.play(-1)
			lagu_intro = True
		screen.blit(start_instruction, start_instruction_rect)
		screen.blit(exit_instruction, exit_instruction_rect)

	pygame.display.update()
	clock.tick(60)