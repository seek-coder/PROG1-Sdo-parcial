import pygame
from .spritesheet_control import *
from config import *
from .player import *

class Enemies(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, width: float, height: float, x_speed: float = 1, direction_default: str = "left"):
        """Enemigos y métodos.

        Args:
            x (float): Coordenadas en x
            y (float): Coordenadas en y
            width (float): Ancho
            height (float): Alto
            x_speed (float, optional): Velocidad en X. Predeterminado en 1
            direction_default (str, optional): Movimiento lateral predeterminado en 'izquierda'
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.rect = self.rect.inflate(-20, -20)
        self.x_speed = x_speed
        self.animation_delay = 10
        self.direction = direction_default
        self.animation_count = 0
        self.initial_y = y

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

    def update_sprite(self):
        sprite_sheet = "fox_walk"
        self.sprites = load_sprite_sheets("img", "enemies", 69, 63, False)

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites_animate = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // self.animation_delay) % len(sprites_animate) # actualización del spritesheet

        self.sprite = sprites_animate[sprite_index]
        self.animation_count += 1

    def draw(self, window):
        window.blit(self.sprite, (self.rect.x - 12, self.rect.y))
        if self.x_speed == 2 or self.x_speed == 4:
            if self.rect.y < floor_inicial_y + 8:
                self.rect.y += 6


