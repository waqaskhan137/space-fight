import pygame
import math
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pass

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 100)  # Increased size
        self.original_image = pygame.image.load('assets/spaceArt/png/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (100, 100))  # Increased size
        self.damaged_image = pygame.image.load('assets/spaceArt/png/playerDamaged.png').convert_alpha()
        self.damaged_image = pygame.transform.scale(self.damaged_image, (100, 100))  # Increased size
        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 10  # Increased base speed
        self.speed = self.base_speed
        self.shield = False
        self.power_up_level = 0
        self.speed_boost_timer = 0
        self.rapid_fire_timer = 0

    def move(self, dx, dy):
        if dx != 0 and dy != 0:
            # Normalize diagonal movement
            dx *= 0.7071
            dy *= 0.7071
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, screen):
        if self.shield:
            screen.blit(self.image, self.rect)
            shield_image = pygame.image.load('assets/spaceArt/png/shield.png').convert_alpha()
            shield_image = pygame.transform.scale(shield_image, (self.rect.width + 20, self.rect.height + 20))
            screen.blit(shield_image, (self.rect.x - 10, self.rect.y - 10))
        else:
            screen.blit(self.damaged_image if self.power_up_level > 0 else self.image, self.rect)

class Enemy(GameObject):
    def __init__(self, x, y, is_ufo=False):
        super().__init__(x, y, 30, 40)
        image_path = 'assets/spaceArt/png/enemyUFO.png' if is_ufo else 'assets/spaceArt/png/enemyShip.png'
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 1
        self.speed = 2

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Bullet(GameObject):
    def __init__(self, x, y, angle, is_enemy=False):
        super().__init__(x, y, 5, 10)
        image_path = 'assets/spaceArt/png/laserRed.png' if is_enemy else 'assets/spaceArt/png/laserGreen.png'
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (5, 10))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = 7

    def move(self):
        self.rect.x += self.speed * math.sin(math.radians(self.angle))
        self.rect.y -= self.speed * math.cos(math.radians(self.angle))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class PowerUp(GameObject):
    def __init__(self, x, y, type):
        super().__init__(x, y, 20, 20)
        self.type = type
        self.speed = 2
        self.images = {
            0: pygame.image.load('assets/spaceArt/png/shield.png').convert_alpha(),
            1: pygame.image.load('assets/spaceArt/png/laserGreenShot.png').convert_alpha(),
            2: pygame.image.load('assets/spaceArt/png/meteorSmall.png').convert_alpha(),
            3: pygame.image.load('assets/spaceArt/png/life.png').convert_alpha()
        }
        self.image = pygame.transform.scale(self.images[type], (20, 20))
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)