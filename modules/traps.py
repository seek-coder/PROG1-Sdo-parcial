import pygame
from .surface_and_rect_control import get_surface_and_rect
from config import *

class Traps():
    def __init__(self, x: float, y: float, t_dir: str):
        self.surface, self.rect = get_surface_and_rect(t_dir, (x, y))
        self.trap_rect = self.rect.inflate(-40, -40)

    def draw(self, window):
        # pygame.draw.rect(window, RED, self.trap_rect)
        window.blit(self.surface, (self.rect.x, self.rect.y - 25))



