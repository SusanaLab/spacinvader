import os
import sys
import pygame
pygame.init()

from game import Game
from enemy import EnemySpawner
from player import Player
from drawing import Drawing


def load_image_or_fallback(path, size=None, fill=(255, 255, 255)):
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            return img
        except Exception:
            pass
    w, h = size if size else (40, 30)
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    surf.fill(fill)
    return surf


def show_game_over(window, screen_w, screen_h, enemy_hits, bullets_fired, tiempo_jugado):
    """Muestra la pantalla de Game Over con estadísticas."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Intentar cargar el fondo de game_over
    game_over_bg_path = os.path.join(current_dir, 'assets', 'game_over.jpg')
    if os.path.exists(game_over_bg_path):
        try:
            bg = pygame.image.load(game_over_bg_path).convert_alpha()
            bg = pygame.transform.scale(bg, (screen_w, screen_h))
        except Exception:
            bg = None
    else:
        bg = None
    
    # Crear fuente para el texto
    try:
        if not pygame.font.get_init():
            pygame.font.init()
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
    except Exception:
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        
        # Dibujar fondo
        if bg:
            window.blit(bg, (0, 0))
        else:
            window.fill((0, 0, 0))
        
        # Título GAME OVER
        game_over_label = font_large.render('GAME OVER', True, (0, 0, 0))
        game_over_x = (screen_w - game_over_label.get_width()) // 2
        game_over_y = screen_h // 4
        window.blit(game_over_label, (game_over_x, game_over_y))
        
        # Estadísticas
        stats_y = screen_h // 2
        line_spacing = 60
        
        # Enemigos alcanzados
        enemies_label = font_medium.render(f'Enemigos Alcanzados: {enemy_hits}', True, (255, 255, 255))
        enemies_x = (screen_w - enemies_label.get_width()) // 2
        window.blit(enemies_label, (enemies_x, stats_y))
        
        # Balas disparadas
        bullets_label = font_medium.render(f'Balas Disparadas: {bullets_fired}', True, (255, 255, 255))
        bullets_x = (screen_w - bullets_label.get_width()) // 2
        window.blit(bullets_label, (bullets_x, stats_y + line_spacing))
        
        # Precisión
        if bullets_fired > 0:
            precision = int((enemy_hits / bullets_fired) * 100)
        else:
            precision = 0
        precision_label = font_medium.render(f'Precisión: {precision}%', True, (255, 255, 255))
        precision_x = (screen_w - precision_label.get_width()) // 2
        window.blit(precision_label, (precision_x, stats_y + line_spacing * 2))
        
        # Tiempo jugado
        minutos = tiempo_jugado // 60
        segundos = tiempo_jugado % 60
        time_label = font_medium.render(f'Tiempo: {minutos:02d}:{segundos:02d}', True, (255, 255, 255))
        time_x = (screen_w - time_label.get_width()) // 2
        window.blit(time_label, (time_x, stats_y + line_spacing * 3))
        
        # Instrucción de continuar
        continue_label = font_small.render('Presiona cualquier tecla para salir...', True, (200, 200, 200))
        continue_x = (screen_w - continue_label.get_width()) // 2
        window.blit(continue_label, (screen_h - 100, 100))
        
        pygame.display.flip()
    
    return True


def main():
    screen_w, screen_h = 1280, 720

    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Cargar bullet.png sin fallback blanco (si no existe, usar None)
    bullet_path = os.path.join(current_dir, 'assets', 'bullet.png')
    if os.path.exists(bullet_path):
        try:
            bullet_img = pygame.image.load(bullet_path).convert_alpha()
            bullet_img = pygame.transform.scale(bullet_img, (8, 16))
        except Exception:
            bullet_img = None
    else:
        bullet_img = None

    game = Game(screen_width=screen_w, screen_height=screen_h, image=bullet_img)
    game.lives = 10  # Iniciar con 10 vidas

    # Crear nave transparente (no visible) como fallback
    ship_img = pygame.Surface((60, 48), pygame.SRCALPHA)
    ship_img.fill((0, 0, 0, 0))  # completamente transparente

    player = Player(
        x=screen_w // 2 - ship_img.get_width() // 2,
        y=screen_h - 120,
        health=3,
        ship_img=ship_img,
        bullet_img=bullet_img
    )
    # Balas infinitas: indicamos None para que el HUD muestre ∞
    game.bullets = None

    enemies = []
    spawner = EnemySpawner()
    drawing = Drawing(game.window)  # Inicializar la clase Drawing para el background

    running = True
    while running:
        game.clock.tick(game.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Disparar con click del ratón: se crean balas desde la parte baja de la pantalla
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.request_fire = True

        player.move(game.screen_height, game.screen_width)
        # Disparo por click (infinitas balas): create_bullets leerá player.request_fire
        player.create_bullets(game)
        player.cooldown(game)
        # Actualizar contador de balas disparadas desde el jugador
        game.bullets_fired = player.total_bullets_fired

        for b in player.fired_bullets[:]:
            b.move(-player.bullet_speed)
            if b.y < -50:
                player.fired_bullets.remove(b)

        spawner.update(enemies, game.screen_width)
        for e in enemies[:]:
            e.move()
            if e.y > game.screen_height + 100:
                # Enemigo salió por abajo: perder una vida
                game.lives -= 1
                enemies.remove(e)

        player.hit(enemies, game)

        # Usar Drawing para renderizar todo con el background
        drawing.drawing(game, player, enemies, game.fps)
        game.contador += 1
        
        # Terminar si se acaban las vidas
        if game.lives <= 0:
            running = False

    # Mostrar pantalla de Game Over con estadísticas
    tiempo_jugado = game.contador // game.fps
    show_game_over(game.window, screen_w, screen_h, game.enemy_hits, game.bullets_fired, tiempo_jugado)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
