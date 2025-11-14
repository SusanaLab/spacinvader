class Ship:
    def __init__(self, x: int, y: int, speed: int = 5):
        self.x = x
        self.y = y
        self.speed = speed

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed