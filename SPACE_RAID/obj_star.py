from CONSTANTES import *

class Star:
    def __init__(self):
        self.x = random.randint(0, ANCHO)
        self.y = random.randint(0, ALTO)
        self.speed = random.randint(1, 2)

    def move(self):
        self.y += self.speed
        if self.y > ALTO:
            self.y = 0
            self.x = random.randint(0, ANCHO)

    def draw(self, screen):
        pygame.draw.circle(screen, BLANCO, (self.x, self.y), 2)
        