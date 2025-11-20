from ship import ShipClass
import pygame
import random
import os

# Obtener el directorio actual del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))

# Cargar imágenes de enemigos
ENEMY_BLUE_IMAGE = pygame.image.load(os.path.join(current_dir, 'assets', 'enemy_blue_image.png'))
ENEMY_GREEN_IMAGE = pygame.image.load(os.path.join(current_dir, 'assets', 'enemy_green_image.png'))
ENEMY_PURPLE_IMAGE = pygame.image.load(os.path.join(current_dir, 'assets', 'enemy_purple_image.png'))

# Cargar imágenes de disparos
SHOT_BLUE_IMAGE = pygame.image.load(os.path.join(current_dir, 'assets', 'shot_blue.png'))
SHOT_GREEN_IMAGE = pygame.image.load(os.path.join(current_dir, 'assets', 'shot_green.png'))
SHOT_PURPLE_IMAGE = pygame.image.load(os.path.join(current_dir, 'assets', 'shot_purple.png'))


class Enemy(ShipClass):
    COLOR = {'blue':(ENEMY_BLUE_IMAGE,SHOT_BLUE_IMAGE),
             'green':(ENEMY_GREEN_IMAGE,SHOT_GREEN_IMAGE),
             'purple':(ENEMY_PURPLE_IMAGE,SHOT_PURPLE_IMAGE)}
    def __init__(self, x=50, y=50, salud_de_vida=100, color = 'blue',speed=10):
        super().__init__(x, y, salud_de_vida)
        self.ship_img, self.bullet_img = self.COLOR[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.spped = speed
    def move(self):
        self.y += self.spped
    def create(self,amount):
        enemies = []
        for _ in range(amount):
            enemy = Enemy(x=random.randrange(20, 1920-ENEMY_BLUE_IMAGE.get_width()-20),y=random.randrange(-1000,-100),color=random.choice(['blue','green','purple']),speed=self.spped)
            enemies.append(enemy)
        return enemies