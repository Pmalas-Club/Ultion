import pygame, sys
from settings import * 
from level import Level
from ui import UI

ui2 = UI(screen)
# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(level_map,screen)

# background = pygame.image.load('../graphics/Background/background.png').convert()
# background = pygame.transform.scale(background, (background.get_width() * 3, background.get_height() * 2))
# bg_rect = background.get_rect(topleft=(0,0))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	#screen.fill('black')
	level.run()

	pygame.display.update()
	clock.tick(60)