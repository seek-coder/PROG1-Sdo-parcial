import pygame
from .spritesheet_control import *
from config import *
from .player import *

class Boss(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, width: float, height: float, x_speed: float = 1, direction_default: str = "left"):
        """Jefe final y métodos.

        Args:
            x (float): Coordenadas en x
            y (float): Coordenadas en y
            width (float): Ancho
            height (float): Alto
            x_speed (float, optional): Velocidad en X. Predeterminado en 1
            direction_default (str, optional): Movimiento lateral predeterminado en 'izquierda'
        """

        self.rect = pygame.Rect(x, y, width, height)
        self.sprite = pygame.Surface((width, height))
        self.rect = self.rect.inflate(-20, -20)
        self.x_speed = x_speed
        self.animation_delay = 10
        self.direction = direction_default
        self.animation_count = 0
        self.initial_y = y

        # ───── VIDAS ───── #
        self.boss_lives_count = 5
        self.boss_live, self.boss_live_rect = get_surface_and_rect("assets/img/boss_live.png")

        # ───── SONIDOS ───── #
        pygame.mixer.init()
        self.boss_killed_wav = pygame.mixer.Sound("assets/sound/boss_killed.wav")
        self.hit_wav = pygame.mixer.Sound("assets/sound/hit.wav")

        # ───── DISPAROS ───── #
        self.shoot_to_bottom = []
        self.last_shot_time = 0
        self.shoot_cooldown = 600

    def movement(self, left_limit: float = 0, right_limit: float = WIDTH):
        """Movimientos de la clase.

        Args:
            left_limit (float, optional): Límite por izquierda
            right_limit (float, optional): Límite por derecha
        """
        if self.direction == "right":
            self.rect.x -= self.x_speed
            if self.rect.x <= left_limit:
                self.direction = "left"
        else:
            self.rect.x += self.x_speed
            if self.rect.x >= right_limit:
                self.direction = "right"

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
                self.last_shot_time = current_time

                # ───── CARGA DE BALAS ───── #
                self.boss_shoot, self.boss_shoot_rect = get_surface_and_rect("assets/img/boss_shoot.png", (self.rect.x + 24, self.rect.y + 64))
                self.shoot_to_bottom.append((self.boss_shoot, self.boss_shoot_rect))
            

    def update_sprite(self):
        sprite_sheet = "boss_walk"
        self.sprites = load_sprite_sheets("img", "enemies", 140, 128, False)

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites_animate = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // self.animation_delay) % len(sprites_animate) # actualización del spritesheet

        self.sprite = sprites_animate[sprite_index]
        self.animation_count += 1

    def draw(self, window, player):
        window.blit(self.sprite, (self.rect.x - 12, self.rect.y))

        for surface, rect in self.shoot_to_bottom:
                window.blit(surface, rect)
                rect.y += 5

        if self.boss_lives_count == 1:
            window.blit(self.boss_live, (self.boss_live_rect.x + 530, self.boss_live_rect.y + 50))
        if self.boss_lives_count == 2:
            window.blit(self.boss_live, (self.boss_live_rect.x + 530, self.boss_live_rect.y + 50))
            window.blit(self.boss_live, (self.boss_live_rect.x + 610, self.boss_live_rect.y + 50))
        if self.boss_lives_count == 3:
            window.blit(self.boss_live, (self.boss_live_rect.x + 530, self.boss_live_rect.y + 50))
            window.blit(self.boss_live, (self.boss_live_rect.x + 610, self.boss_live_rect.y + 50))
            window.blit(self.boss_live, (self.boss_live_rect.x + 690, self.boss_live_rect.y + 50))
        if self.boss_lives_count == 4:
            window.blit(self.boss_live, (self.boss_live_rect.x + 530, self.boss_live_rect.y + 50))
            window.blit(self.boss_live, (self.boss_live_rect.x + 610, self.boss_live_rect.y + 50))
            window.blit(self.boss_live, (self.boss_live_rect.x + 690, self.boss_live_rect.y + 50))
            window.blit(self.boss_live, (self.boss_live_rect.x + 770, self.boss_live_rect.y + 50))
        if self.boss_lives_count == 5:
            window.blit(self.boss_live, (self.boss_live_rect.x + 530, self.boss_live_rect.y + 50))
            window.blit(self.boss_live, (self.boss_live_rect.x + 610, self.boss_live_rect.y + 50))
            window.blit(self.boss_live, (self.boss_live_rect.x + 690, self.boss_live_rect.y + 50))
            window.blit(self.boss_live, (self.boss_live_rect.x + 770, self.boss_live_rect.y + 50))
            window.blit(self.boss_live, (self.boss_live_rect.x + 850, self.boss_live_rect.y + 50))
        
        for boss_bullet, boss_bullet_rect in self.shoot_to_bottom:
            if player.rect.colliderect(boss_bullet_rect):
                player.lives_count -= 1
                player.hit = True
                self.shoot_to_bottom.remove((boss_bullet, boss_bullet_rect))
                self.hit_wav.play()


