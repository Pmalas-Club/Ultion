import pygame, sys
from settings import screen_width, screen_height
from level import Level
from player import Player
from ui import UI
from game_data import level_0

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
# ui2 = UI(screen)
clock = pygame.time.Clock()
# level = Level(level_map,screen)
level = Level(level_0,screen)
game_active = False

# INTRO
title_font = pygame.font.Font('../font/Pixeltype.ttf', 100)
title = title_font.render('ULTION', False, 'lightblue')
title_rect = title.get_rect(center=(400,200))

instruction_font = pygame.font.Font('../font/Pixeltype.ttf', 50)
start_instruction = instruction_font.render('START!', False, 'black')
start_instruction_rect = start_instruction.get_rect(center=(400,450))
exit_instruction = instruction_font.render('EXIT', False, 'black')
exit_instruction_rect = exit_instruction.get_rect(center=(400,600))
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if start_instruction_rect.collidepoint(event.pos):
				game_active = True
			elif exit_instruction_rect.collidepoint(event.pos):
				sys.exit()
	
	screen.fill('black')
	if game_active:
		level.run()
	# ui2.show_health()
	else:
		screen.fill((94, 129, 162))
		screen.blit(title, title_rect)
		# if finale_score != 0:
		# 	final_score(finale_score)
		# else:
		screen.blit(start_instruction, start_instruction_rect)
		screen.blit(exit_instruction, exit_instruction_rect)

		#obstacle_rectangle_list.clear()
		#player_rectangle.bottom = 300
		#player_gravity = 0

	pygame.display.update()
	clock.tick(60)