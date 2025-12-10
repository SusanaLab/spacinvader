import pygame 
class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        # Si la imagen es None, crear una superficie simple como fallback
        if self.img is None:
            self.img = pygame.Surface((8, 16), pygame.SRCALPHA)
            pygame.draw.circle(self.img, (255, 215, 0), (4, 8), 3)
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        if self.img:
            window.blit(self.img, (self.x, self.y))
    def move(self, speed):
        self.y += speed
    def collision(self, obj):
        offset = (int(self.x - obj.x - 30), int(self.y - obj.y - 20))
        return self.mask.overlap(obj.mask, (offset))