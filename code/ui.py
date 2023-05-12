import pygame

class UI:
    def __init__(self, surface) -> None:
        self.display_surface = surface
        self.health_bar = pygame.Surface((100,5))
        self.health_bar.fill('red')
    def show_health(self,current,full):
        self.display_surface.blit(self.health_bar,(20, 10))

