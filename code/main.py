import pygame, sys
from settings import * 
from level import Level
from ui import UI

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
ui2 = UI(screen)
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
	# pygame.draw.rect(self.display_surface, 'green', (20,10, 100, 10))
	level.run()
	ui2.show_health()

	pygame.display.update()
	clock.tick(60)