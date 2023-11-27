import pygame
from config import *
from .surface_and_rect_control import *


class Chickens(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float):
        """Gallinas del juego

        Args:
            x (float): Coordenadas en x
            y (float): Coordenadas en y
        """

        self.surface, self.rect = get_surface_and_rect("assets/img/chicken.png", (x, y))
        self.chickens_saved = []

    def draw(self, window):
        window.blit(self.surface, (self.rect.x, self.rect.y))

    def collision(self, collider, player):
            if collider.colliderect(self.rect):
                if self.rect not in self.chickens_saved:
                    self.surface.set_alpha(0)
                    player.points_count += 300
                self.chickens_saved.append(self.rect)

