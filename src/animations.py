import pygame
import random

class Confetti:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        self.x = random.randint(0, width)
        self.y = random.randint(-height, 0)
        self.size = random.randint(2, 6)
        self.color = random.choice(self.colors)
        self.speed = random.uniform(1, 4)

    def update(self):
        self.y += self.speed
        if self.y > self.height:
            self.y = random.randint(-100, -10)
            self.x = random.randint(0, self.width)
            self.speed = random.uniform(1, 4)
            self.color = random.choice(self.colors)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

class Rain:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.colors = [(0, 0, 255), (0, 0, 200), (0, 0, 100), (0, 0, 50)]
        self.x = random.randint(0, width)
        self.y = random.randint(-height, 0)
        self.rain_width = random.randint(2, 3)
        self.rain_height = random.randint(2, 12)
        self.color = random.choice(self.colors)
        self.speed = random.uniform(4, 8)

    def update(self):
        self.y += self.speed
        if self.y > self.height:
            self.y = random.randint(-100, -10)
            self.x = random.randint(0, self.width)
            self.speed = random.uniform(4, 8)
            self.color = random.choice(self.colors)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.rain_width, self.rain_height))