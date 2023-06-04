# Default Python modules, no need to check as it's definitely available*
# *as long as the user installs Python normally.
import sys
import os
import random

# Checks if the pygame module is installed on the user's device.
try:
    import pygame
except ImportError:
    print('\nYah, sepertinya ada masalah saat menjalankan game :(')
    print('Pastikan modul pygame telah tersedia di perangkatmu.')
    print('Kode Error: 0101/Main\n')
    print('Untuk informasi lebih lanjut, baca dokumentasi Ultion di sini: ')
    print('http://bit.ly/UltionDocs \n')
    sys.exit()

# Checks if Ultion modules are available on the user's device.
try:
    from settings import screen_width, screen_height
    from level import Level
    from game_data import *
    from ui import HealthBar
except ModuleNotFoundError:
    print('\nYah, sepertinya ada masalah saat menjalankan game :(')
    print('File game Ultion yang kamu miliki mungkin rusak atau berubah tempat.')
    print('Kode Error: 0102/Main\n')
    print('Untuk informasi lebih lanjut, baca dokumentasi Ultion di sini: ')
    print('http://bit.ly/UltionDocs \n')
    sys.exit()

# Checks if Ultion assets are available on the user's device with test file in each folder.
try:
    open('../font/.test','r')
    open('../graphics/.test','r')
    open('../levels/.test','r')
    open('../sounds/.test','r')
    open('../Tilesets/.test','r')
except FileNotFoundError:
    print('\nYah, sepertinya ada masalah saat menjalankan game :(')
    print('Tip: Ketik perintah "cd code" pada terminal IDE-mu, lalu tekan enter, dan jalankan kembali program.')
    print('Jika pesan ini masih tampil, file game Ultion yang kamu miliki mungkin rusak atau berubah tempat.')
    print('Kode Error: 0103/Main\n')
    print('Untuk informasi lebih lanjut, baca dokumentasi Ultion di sini: ')
    print('http://bit.ly/UltionDocs \n')
    sys.exit()

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game_active = False
is_victory = False
is_lose = False
levels = [level_0,level_1,level_2]
level_index = 0

# INTRO
title_font = pygame.font.Font('../font/Pixeltype.ttf', 100)
title = title_font.render('ULTION', False, 'lightblue')
title_rect = title.get_rect(center=(400, 300))

instruction_font = pygame.font.Font('../font/Pixeltype.ttf', 50)

start_instruction = instruction_font.render('START!', False, 'red')
start_instruction_rect = start_instruction.get_rect(center=(400, 450))

exit_instruction = instruction_font.render('EXIT', False, 'red')
exit_instruction_rect = exit_instruction.get_rect(center=(400, 600))

victory = title_font.render('TO BE CONTINUED', False, 'white')
victory_rect = victory.get_rect(center=(int(screen_width / 2), 120))

lose = title_font.render('YOU LOSE!', False, 'white')
lose_rect = victory.get_rect(center=(int(screen_width / 2), 120))

# # MUSIC
intro_game = pygame.mixer.Sound('../sounds/intro/intro.mp3')
lagu_intro = False
backsound = pygame.mixer.Sound('../sounds/play_scene/play_scene.mp3')


# Particle class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-5, -1)
        self.alpha = 255

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.alpha -= 5
        if self.alpha <= 0:
            self.alpha = 0

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 165, 0, self.alpha), (int(self.x), int(self.y)), 5)

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

        # Animation
        self.animation_folder = '../graphics/wallpaper'
        self.animation_files = os.listdir(self.animation_folder)
        self.animation_images = []
        for file in self.animation_files:
            image_path = os.path.join(self.animation_folder, file)
            image = pygame.image.load(image_path)
            image = pygame.transform.scale(image, (image.get_width() * 10, image.get_height() * 10))
            self.animation_images.append(image)
        self.animation_frame_index = 0
        self.animation_delay = 100  # Adjust this value to control the animation speed

        # Fire particles
        self.particles = []

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
                if self.game_active:
                    # If the game is active, handle game-related events
                    # self.level.handle_event(event)
                    print()
                else:
                    # If the game is not active, check for button clicks
                    if start_instruction_rect.collidepoint(event.pos):
                        self.game_active = True
                        self.level = Level(levels[self.level_index], screen, self.get_health, self.set_health)
                        self.is_victory = False
                        self.is_lose = False
                        intro_game.stop()
                        backsound.play()
                    elif exit_instruction_rect.collidepoint(event.pos):
                        sys.exit()

        if self.game_active:
            self.level.run()
            self.health_bar.draw(screen, self.__health)

            self.is_victory = self.level.finish()
            self.is_lose = self.level.lose()
            if self.is_victory:
                if self.level_index == len(levels) - 1:
                    self.game_active = False
                    self.__health = 100
                else:
                    self.__health = self.level.get_health()
                    self.level_index += 1
                    self.level = None
                    self.level = Level(levels[self.level_index], screen, self.get_health, self.set_health)
            if self.is_lose:
                print(self.level_index)
                self.game_active = False
                self.__health = 100
                self.score = 0

        else:
            # Draw the animation frame
            screen.blit(self.animation_images[self.animation_frame_index], (500, 100))

            # Update and draw fire particles
            for particle in self.particles:
                particle.update()
                particle.draw(screen)

            # Add new particles
            if random.random() < 0.5:
                x = random.uniform(0, screen_width)
                y = screen_height
                particle = Particle(x, y)
                self.particles.append(particle)

            # Remove faded out particles
            self.particles = [particle for particle in self.particles if particle.alpha > 0]

        # Delay to control the frame rate of the animation
            pygame.time.delay(self.animation_delay)

        # Increment the frame index for the next iteration
            self.animation_frame_index = (self.animation_frame_index + 1) % len(self.animation_images)


game = Ultion()

while True:
    # Clear the screen
    screen.fill((0, 0, 0))

    game.run()

    # Draw UI elements on top of the animation
    if not game.game_active:
        screen.blit(title, title_rect)
        if game.is_victory:
            screen.blit(victory, victory_rect)
            backsound.stop()
        elif game.is_lose:
            screen.blit(lose, lose_rect)
            backsound.stop()

        if not lagu_intro:
            intro_game.play(-1)
            lagu_intro = True
        screen.blit(start_instruction, start_instruction_rect)
        screen.blit(exit_instruction, exit_instruction_rect)

    pygame.display.update()
    clock.tick(60)
