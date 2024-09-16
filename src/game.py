import pygame
import random
import math
import os
from src.game_objects import Player, Enemy, Bullet, PowerUp
from src.particle import Particle
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, ENEMY_SPAWN_RATE, POWER_UP_SPAWN_RATE

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Space Fighter Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        
        # Load sound effects
        try:
            self.shoot_sound = pygame.mixer.Sound('assets/sounds/shoot.mp3')
            self.explosion_sound = pygame.mixer.Sound('assets/sounds/explosion.mp3')
            self.power_up_sound = pygame.mixer.Sound('assets/sounds/powerup.mp3')
            pygame.mixer.music.load('assets/sounds/background.mp3')
        except pygame.error as e:
            print(f"Error loading sound files: {e}")
            sys.exit(1)
        
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        
        # Initialize power-up spawn timer and interval
        self.power_up_spawn_timer = 0
        self.power_up_spawn_interval = 10000  # Spawn a power-up every 10 seconds
        
        self.difficulty_timer = 0
        self.difficulty_interval = 30000  # Increase difficulty every 30 seconds
        
        # Load background image
        try:
            self.background = pygame.image.load('assets/spaceArt/png/Background/starBackground.png').convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            sys.exit(1)
        
        self.reset_game()

    def reset_game(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.enemies = [Enemy(random.randint(0, SCREEN_WIDTH - 30), random.randint(-150, -50)) for _ in range(5)]
        self.bullets = []
        self.power_ups = []
        self.particles = []
        self.score = 0
        self.last_power_up_spawn = pygame.time.get_ticks()

    def run(self):
        running = True
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        return  # Exit the run method immediately
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.shoot()
                        elif event.key == pygame.K_ESCAPE:  # Add an escape key to quit
                            running = False
                            return  # Exit the run method immediately

                if not self.update():
                    running = False
                self.draw()
                self.clock.tick(FPS)
        except pygame.error:
            print("Pygame error occurred. The game window may have been closed.")
        finally:
            pygame.mixer.music.stop()  # Stop the music when the game ends
            pygame.quit()

    def update(self):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        # Check if moving diagonally
        if dx != 0 and dy != 0:
            # Normalize the movement vector to maintain consistent speed
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071

        self.player.move(dx, dy)

        for enemy in self.enemies[:]:
            enemy.move()  # Use the enemy's move method
            if enemy.rect.top > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.enemies.append(Enemy(random.randint(0, SCREEN_WIDTH - 30), random.randint(-150, -50)))

        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        self.power_up_spawn_timer += self.clock.get_time()
        if self.power_up_spawn_timer >= self.power_up_spawn_interval:
            self.spawn_power_up()
            self.power_up_spawn_timer = 0

        for power_up in self.power_ups[:]:
            power_up.move()
            if power_up.rect.top > SCREEN_HEIGHT:
                self.power_ups.remove(power_up)

        collisions_ok = self.check_collisions()

        # Update particles
        dt = self.clock.get_time() / 1000.0  # Convert milliseconds to seconds
        for particle in self.particles[:]:
            if particle.update(dt):
                self.particles.remove(particle)
        
        # Update difficulty
        self.difficulty_timer += self.clock.get_time()
        if self.difficulty_timer >= self.difficulty_interval:
            self.increase_difficulty()
            self.difficulty_timer = 0

        if not collisions_ok:
            self.game_over()
            return False  # Signal to end the game loop

        return True  # Continue the game

    def shoot(self):
        angles = self.get_bullet_angles()
        for angle in angles:
            self.bullets.append(Bullet(self.player.rect.centerx, self.player.rect.top, angle))
        self.shoot_sound.play()

    def get_bullet_angles(self):
        if self.player.power_up_level == 0:
            return [0]
        elif self.player.power_up_level == 1:
            return [-15, 0, 15]
        elif self.player.power_up_level == 2:
            return [-30, -15, 0, 15, 30]
        else:
            return [-45, -30, -15, 0, 15, 30, 45]

    def spawn_power_up(self):
        if len(self.power_ups) < 3:  # Limit the number of power-ups on screen
            x = random.randint(0, SCREEN_WIDTH - 20)
            y = -20
            power_up_type = random.randint(0, 3)
            self.power_ups.append(PowerUp(x, y, power_up_type))

    def check_collisions(self):
        # Check bullet-enemy collisions
        for enemy in self.enemies[:]:
            for bullet in self.bullets[:]:
                if enemy.rect.colliderect(bullet.rect):
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    self.score += 1
                    self.enemies.append(Enemy(random.randint(0, SCREEN_WIDTH - 30), random.randint(-150, -50)))
                    self.explosion_sound.play()
                    break  # Break to avoid checking removed bullet against other enemies

        # Check player-enemy collisions
        for enemy in self.enemies[:]:
            if self.player.rect.colliderect(enemy.rect):
                if self.player.shield:
                    self.player.shield = False
                    self.enemies.remove(enemy)
                    self.explosion_sound.play()
                else:
                    return False  # End the game if player collides with enemy

        # Check player-powerup collisions
        for power_up in self.power_ups[:]:
            if self.player.rect.colliderect(power_up.rect):
                self.apply_power_up(power_up.type)
                self.power_ups.remove(power_up)

        return True  # Continue the game

    def apply_power_up(self, power_up_type):
        if power_up_type == 0:  # Shield
            self.player.shield = True
        elif power_up_type == 1:  # Rapid Fire
            self.player.power_up_level = min(self.player.power_up_level + 1, 3)
        elif power_up_type == 2:  # Bomb
            for enemy in self.enemies[:]:
                self.create_explosion(enemy.rect.center)
                self.enemies.remove(enemy)
                self.score += 1
            self.enemies = [Enemy(random.randint(0, SCREEN_WIDTH - 30), random.randint(-150, -50)) for _ in range(5)]
        elif power_up_type == 3:  # Speed Boost
            self.player.speed = 8
            self.player.speed_boost_timer = pygame.time.get_ticks()
        self.power_up_sound.play()

    MAX_PARTICLES = 500  # Define a reasonable limit

    def create_explosion(self, position):
        if len(self.particles) < self.MAX_PARTICLES:
            for _ in range(30):
                size = random.uniform(5, 15)
                color = random.choice([(255, 165, 0), (255, 69, 0), (255, 0, 0)])
                self.particles.append(Particle(position[0], position[1], color, size))

    def game_over(self):
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render('Game Over', True, (255, 255, 255))
        score_text = self.font.render(f'Final Score: {self.score}', True, (255, 255, 255))
        restart_text = self.font.render('Press R to Restart or Q to Quit', True, (255, 255, 255))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # Quit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pygame.mixer.music.play(-1)  # Restart the music
                        self.reset_game()
                        return True  # Restart the game
                    elif event.key == pygame.K_q:
                        return False  # Quit the game
            self.clock.tick(FPS)  # Add a tick to prevent the loop from running too fast

        return False  # If we get here, the game should end

    def increase_difficulty(self):
        for enemy in self.enemies:
            enemy.speed *= 1.1
        self.power_up_spawn_interval *= 0.9

    def draw(self):
        self.screen.blit(self.background, (0, 0))  # Draw background first
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for power_up in self.power_ups:
            power_up.draw(self.screen)
        
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        for particle in self.particles:
            particle.draw(self.screen)
        
        pygame.display.flip()