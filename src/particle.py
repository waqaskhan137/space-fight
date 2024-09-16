import pygame
import random

class Particle:
    def __init__(self, x, y, color, size):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.dx = random.uniform(-2, 2)  # Increased speed range
        self.dy = random.uniform(-2, 2)  # Increased speed range
        self.lifetime = random.uniform(0.5, 1.5)  # Particle lifetime in seconds

    def update(self, dt):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= dt
        self.size -= dt * (self.size / self.lifetime)  # Gradually decrease size
        return self.lifetime <= 0 or self.size <= 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))