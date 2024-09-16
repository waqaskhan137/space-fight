from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

class GameObject(Widget):
    def move(self):
        pass

class Player(GameObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (100, 100)
        self.base_speed = 10
        self.speed = self.base_speed
        self.shield = False
        self.power_up_level = 0
        self.speed_boost_timer = 0
        self.rapid_fire_timer = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 1
        self.max_speed = 15
        self.deceleration = 0.9
        
        with self.canvas:
            self.player_color = Color(1, 1, 1, 1)
            self.player_image = Rectangle(source='assets/spaceArt/png/player.png', pos=self.pos, size=self.size)
            self.shield_color = Color(0, 0, 1, 0)
            self.shield_image = Rectangle(source='assets/spaceArt/png/shield.png', pos=self.pos, size=(120, 120))
        
        self.bind(pos=self.update_rect_pos)

    def update_rect_pos(self, *args):
        self.player_image.pos = self.pos
        self.shield_image.pos = (self.x - 10, self.y - 10)

    def update(self, dt):
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Apply deceleration
        self.velocity_x *= self.deceleration
        self.velocity_y *= self.deceleration
        
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= dt
            if self.speed_boost_timer <= 0:
                self.speed = self.base_speed
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= dt
            if self.rapid_fire_timer <= 0:
                self.power_up_level = max(0, self.power_up_level - 1)
        self.shield_color.a = 1 if self.shield else 0

class Enemy(GameObject):
    def __init__(self, is_ufo=False, **kwargs):
        super().__init__(**kwargs)
        self.size = (60, 80)
        self.speed = 2
        image_path = 'assets/spaceArt/png/enemyUFO.png' if is_ufo else 'assets/spaceArt/png/enemyShip.png'
        with self.canvas:
            self.enemy_image = Rectangle(source=image_path, pos=self.pos, size=self.size)

    def move(self):
        self.y -= self.speed
        self.enemy_image.pos = self.pos

class Bullet(GameObject):
    def __init__(self, angle=0, is_enemy=False, **kwargs):
        super().__init__(**kwargs)
        self.size = (5, 10)
        self.speed = 7
        self.angle = angle
        image_path = 'assets/spaceArt/png/laserRed.png' if is_enemy else 'assets/spaceArt/png/laserGreen.png'
        with self.canvas:
            self.bullet_image = Rectangle(source=image_path, pos=self.pos, size=self.size)

    def move(self):
        self.x += self.speed * math.sin(math.radians(self.angle))
        self.y += self.speed * math.cos(math.radians(self.angle))
        self.bullet_image.pos = self.pos

class PowerUp(GameObject):
    def __init__(self, power_up_type, **kwargs):
        super().__init__(**kwargs)
        self.size = (20, 20)
        self.speed = 2
        self.type = power_up_type
        power_up_images = {
            0: 'assets/spaceArt/png/shield.png',
            1: 'assets/spaceArt/png/laserGreenShot.png',
            2: 'assets/spaceArt/png/meteorSmall.png',
            3: 'assets/spaceArt/png/life.png'
        }
        with self.canvas:
            self.power_up_image = Rectangle(source=power_up_images[self.type], pos=self.pos, size=self.size)

    def move(self):
        self.y -= self.speed
        self.power_up_image.pos = self.pos

class Particle(Widget):
    def __init__(self, x, y, color, **kwargs):
        super().__init__(**kwargs)
        self.pos = (x, y)
        self.color = color
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)
        self.initial_size = 5
        self.size = (self.initial_size, self.initial_size)
        with self.canvas:
            Color(*color)
            self.particle = Rectangle(pos=self.pos, size=self.size)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.initial_size -= 0.1
        if self.initial_size <= 0:
            return True
        new_size = (self.initial_size, self.initial_size)
        self.size = new_size
        self.particle.pos = (self.x, self.y)
        self.particle.size = new_size
        return False

class GameOverScreen(BoxLayout):
    def __init__(self, score, restart_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='Game Over', font_size='40sp'))
        self.add_widget(Label(text=f'Score: {score}', font_size='30sp'))
        restart_button = Button(text='Restart', on_press=restart_callback)
        quit_button = Button(text='Quit', on_press=lambda x: App.get_running_app().stop())
        self.add_widget(restart_button)
        self.add_widget(quit_button)

class SpaceFighterGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player(pos=(Window.width/2 - 50, 100))
        self.add_widget(self.player)
        self.enemies = []
        self.bullets = []
        self.power_ups = []
        self.particles = []
        self.score = 0
        self.score_label = Label(text=f"Score: {self.score}", pos=(10, Window.height - 30))
        self.add_widget(self.score_label)

        self.shoot_sound = SoundLoader.load('assets/sounds/shoot.mp3')
        self.explosion_sound = SoundLoader.load('assets/sounds/explosion.mp3')
        self.power_up_sound = SoundLoader.load('assets/sounds/powerup.mp3')
        self.background_music = SoundLoader.load('assets/sounds/background.mp3')
        if self.background_music:
            self.background_music.loop = True
            self.background_music.play()

        with self.canvas.before:
            self.background = Rectangle(source='assets/spaceArt/png/Background/starBackground.png', pos=(0, 0), size=Window.size)

        Clock.schedule_interval(self.update, 1.0/FPS)
        Clock.schedule_interval(self.spawn_enemy, 2)
        Clock.schedule_interval(self.spawn_power_up, 10)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        self.shoot_timer = 0
        self.shoot_delay = 0.2  # 200ms between shots
        self.spacebar_held = False

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.player.velocity_x = max(self.player.velocity_x - self.player.acceleration, -self.player.max_speed)
        elif keycode[1] == 'right':
            self.player.velocity_x = min(self.player.velocity_x + self.player.acceleration, self.player.max_speed)
        elif keycode[1] == 'up':
            self.player.velocity_y = min(self.player.velocity_y + self.player.acceleration, self.player.max_speed)
        elif keycode[1] == 'down':
            self.player.velocity_y = max(self.player.velocity_y - self.player.acceleration, -self.player.max_speed)
        elif keycode[1] == 'spacebar':
            self.spacebar_held = True
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] in ('left', 'right'):
            self.player.velocity_x = 0
        elif keycode[1] in ('up', 'down'):
            self.player.velocity_y = 0
        elif keycode[1] == 'spacebar':
            self.spacebar_held = False
        return True

    def shoot(self):
        angles = self.get_bullet_angles()
        for angle in angles:
            bullet = Bullet(angle=angle, pos=(self.player.center_x, self.player.top))
            self.bullets.append(bullet)
            self.add_widget(bullet)
        if self.shoot_sound:
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

    def spawn_enemy(self, dt):
        is_ufo = random.random() < 0.2
        enemy = Enemy(is_ufo=is_ufo, pos=(random.randint(0, Window.width - 60), Window.height))
        self.enemies.append(enemy)
        self.add_widget(enemy)

    def spawn_power_up(self, dt):
        if len(self.power_ups) < 3:
            power_up = PowerUp(random.randint(0, 3), pos=(random.randint(0, Window.width - 20), Window.height))
            self.power_ups.append(power_up)
            self.add_widget(power_up)

    def update(self, dt):
        self.player.update(dt)
        
        # Handle continuous shooting
        self.shoot_timer += dt
        if self.spacebar_held and self.shoot_timer >= self.shoot_delay:
            self.shoot()
            self.shoot_timer = 0
        
        # Keep player within screen bounds
        self.player.x = max(0, min(self.player.x, Window.width - self.player.width))
        self.player.y = max(0, min(self.player.y, Window.height - self.player.height))

        for enemy in self.enemies[:]:
            enemy.move()
            if enemy.top < 0:
                self.remove_widget(enemy)
                self.enemies.remove(enemy)

        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y > Window.height:
                self.remove_widget(bullet)
                self.bullets.remove(bullet)

        for power_up in self.power_ups[:]:
            power_up.move()
            if power_up.top < 0:
                self.remove_widget(power_up)
                self.power_ups.remove(power_up)

        for particle in self.particles[:]:
            if particle.update():
                self.remove_widget(particle)
                self.particles.remove(particle)

        self.check_collisions()

    def check_collisions(self):
        for enemy in self.enemies[:]:
            for bullet in self.bullets[:]:
                if self.check_collision(enemy, bullet):
                    self.remove_widget(enemy)
                    self.enemies.remove(enemy)
                    self.remove_widget(bullet)
                    self.bullets.remove(bullet)
                    self.score += 1
                    self.score_label.text = f"Score: {self.score}"
                    self.create_explosion(enemy.center)
                    if self.explosion_sound:
                        self.explosion_sound.play()
                    break

            if self.check_collision(self.player, enemy):
                if self.player.shield:
                    self.player.shield = False
                    self.remove_widget(enemy)
                    self.enemies.remove(enemy)
                    self.create_explosion(enemy.center)
                    if self.explosion_sound:
                        self.explosion_sound.play()
                else:
                    self.game_over()

        for power_up in self.power_ups[:]:
            if self.check_collision(self.player, power_up):
                self.apply_power_up(power_up.type)
                self.remove_widget(power_up)
                self.power_ups.remove(power_up)
                if self.power_up_sound:
                    self.power_up_sound.play()

    def check_collision(self, obj1, obj2):
        return obj1.collide_widget(obj2)

    def apply_power_up(self, power_up_type):
        if power_up_type == 0:  # Shield
            self.player.shield = True
        elif power_up_type == 1:  # Rapid Fire
            self.player.power_up_level = min(self.player.power_up_level + 1, 3)
            self.player.rapid_fire_timer = 10  # 10 seconds
        elif power_up_type == 2:  # Bomb
            for enemy in self.enemies[:]:
                self.remove_widget(enemy)
                self.create_explosion(enemy.center)
            self.enemies = []
        elif power_up_type == 3:  # Speed Boost
            self.player.speed = 8
            self.player.speed_boost_timer = 5  # 5 seconds

    def create_explosion(self, pos):
        for _ in range(20):
            particle = Particle(pos[0], pos[1], (1, 0.5, 0))
            self.particles.append(particle)
            self.add_widget(particle)

    def game_over(self):
        self.clear_widgets()
        game_over_screen = GameOverScreen(self.score, self.restart_game)
        self.add_widget(game_over_screen)

    def restart_game(self, *args):
        App.get_running_app().stop()
        App.get_running_app().run()

class SpaceFighterApp(App):
    def build(self):
        game = SpaceFighterGame()
        Window.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        return game

if __name__ == '__main__':
    SpaceFighterApp().run()