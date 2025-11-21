import pygamme
import os
from game import Game
from enemy import Enemy

current_dir = os.path.dirname(__file__)
BACKGROUND = pygame.image.load(os.path.join('img', 'background.png'))

class Drawing:
    def __init__(self, window):
        self.window = window
    def drawing(self, game, player, enemies, FPS):
        # Drawing the background
        self.window.blit(BACKGROUND, (0,0))


        for enemy in enemies[:]:
            enemy.draw(self.window)
        
        game.draw_HUD()

        pygame.display.update()