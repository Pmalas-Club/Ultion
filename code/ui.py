import pygame

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, display_surface, hp):
        # UPDATE WITH NEW HEALTH
        self.hp = hp
        # CALCULATE HEALTH RATIO
        ratio = self.hp / self.max_hp
        pygame.draw.rect(display_surface, 'red', (self.x, self.y, 150, 20))
        pygame.draw.rect(display_surface, 'green', (self.x, self.y, 150 * ratio, 20))