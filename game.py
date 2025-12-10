import pygame
import os


class Game:
    def __init__(self, screen_width: int = 800, screen_height: int = 600, fps: int = 60,
                 lives: int = 3, nivel: int = 1, font_size: int = 36,
                 caption: str = "Space Invader", image=None):

        # Dimensiones y ventana
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Gameplay
        self.fps = fps
        self.lives = lives
        self.nivel = nivel

        # Estado dinámico
        self.bullets = 0
        self.contador = 0  # contador de frames
        self.bullets_image = image
        self.enemy_hits = 0  # enemigos alcanzados por el jugador
        self.bullets_fired = 0  # total de balas disparadas por el jugador
        self.total_time_sec = 4 * 60  # 4 minutos
        self.start_ticks = pygame.time.get_ticks()

        # Reloj
        self.clock = pygame.time.Clock()

        # Inicializar/crear ventana
        # Asumimos que el llamador ya hizo pygame.init() cuando corresponda; de todos modos
        # creamos la surface de display aquí para tener el atributo Window.
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(caption)

        # Fuente: intentamos inicializar la fuente; si falla dejamos None
        try:
            if not pygame.font.get_init():
                pygame.font.init()
            self.font = pygame.font.Font(None, font_size)
        except Exception:
            self.font = None

    def escape(self):
        """Revisa eventos y retorna True sólo si hay QUIT."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def time_left(self):
        """Devuelve tiempo restante en segundos (no negativo)."""
        elapsed_ms = pygame.time.get_ticks() - self.start_ticks
        elapsed_sec = elapsed_ms // 1000
        remaining = max(0, self.total_time_sec - int(elapsed_sec))
        return remaining

    def over(self):
        """Retorna True si el jugador no tiene vidas; muestra "GAME OVER" brevemente."""
        if self.lives <= 0:
            self.contador = 0
            if self.font:
                gameover_label = self.font.render('GAME OVER', 1, (255, 255, 255))
                x = (self.screen_width - gameover_label.get_width()) // 2
                y = (self.screen_height - gameover_label.get_height()) // 2
                self.window.blit(gameover_label, (x, y))
                pygame.display.update()
                # breve pausa visual
                self.clock.tick(self.fps)
            return True
        return False

    def reload_bullet(self, bullet_count: int):
        self.bullets = int(bullet_count)

    def drawHud(self):
        """Dibuja HUD con vidas, balas, nivel, tiempo restante y enemigos alcanzados."""
        if self.font is None:
            return

        # Vidas
        lives_label = self.font.render(f'Vidas: {self.lives}', True, (255, 255, 255))
        self.window.blit(lives_label, (10, 10))

        # Balas (texto + número de balas disparadas)
        bullets_text_label = self.font.render('Balas:', True, (255, 255, 255))
        text_x, text_y = 10, 50
        self.window.blit(bullets_text_label, (text_x, text_y))
        bullets_fired_label = self.font.render(str(self.bullets_fired), True, (255, 255, 0))
        self.window.blit(bullets_fired_label, (text_x + bullets_text_label.get_width() + 6, text_y))

        # Nivel
        level_label = self.font.render(f'Nivel: {self.nivel}', True, (255, 255, 255))
        self.window.blit(level_label, (10, 90))

        # Tiempo restante en formato MM:SS
        remaining = self.time_left()
        minutes = remaining // 60
        seconds = remaining % 60
        tiempo_label = self.font.render(f'Tiempo: {minutes:02d}:{seconds:02d}', True, (255, 255, 255))
        self.window.blit(tiempo_label, (self.screen_width - 180, 10))

        # Enemigos alcanzados
        hits_label = self.font.render(f'Enemigos: {self.enemy_hits}', True, (255, 255, 255))
        self.window.blit(hits_label, (self.screen_width - 180, 40))


