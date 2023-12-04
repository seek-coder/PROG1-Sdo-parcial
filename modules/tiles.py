import pygame
from .surface_and_rect_control import get_surface_and_rect
from .spritesheet_control import *
from config import *

class Tiles():
    def __init__(self, x: float, y: float, t_dir: str):
        self.surface, self.rect = get_surface_and_rect(t_dir, (x, y))

    def draw(self, window):
        # pygame.draw.rect(window, RED, self.rect)
        window.blit(self.surface, (self.rect.x, self.rect.y))




