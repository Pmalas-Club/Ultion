import pygame, sys
from settings import * 
from level import Level
from player import Player
from ui import UI

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
ui2 = UI(screen)
clock = pygame.time.Clock()
level = Level(level_map,screen)


#game_active = False

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		# if event.type == pygame.KEYDOWN:
		# 	if event.key == pygame.K_SPACE:
		# 		game_active = True
	
	#screen.fill('black')
	#if game_active:
	level.run()
	ui2.show_health()
	# else:
	# 	screen.fill((94, 129, 162))
	# 	screen.blit(player_stand, player_stand_rectangle)
	# 	screen.blit(title_game, title_game_rectangle)
	# 	if finale_score != 0:
	# 		final_score(finale_score)
	# 	else:
	# 		screen.blit(instruction, instruction_rectangle)

	# 	obstacle_rectangle_list.clear()
	# 	player_rectangle.bottom = 300
	# 	player_gravity = 0

	pygame.display.update()
	clock.tick(60)