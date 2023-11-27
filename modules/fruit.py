import pygame
from config import *
from .surface_and_rect_control import *


class Fruit(pygame.sprite.Sprite):
    def __init__(self, x: float, y:float, t_dir:str):
        """Frutas como objetos especiales que aumentan puntos

        Args:
            x (float): Coordenadas en x
            y (float): Coordenadas en y
            t_dir (str): Dirección
        """
        self.surface, self.rect = get_surface_and_rect(t_dir, (x, y))
        self.fruit_eaten = []
        pygame.mixer.init()
        self.goal_wav = pygame.mixer.Sound("assets/sound/goal.wav")

    def draw(self, window):
        window.blit(self.surface, (self.rect.x, self.rect.y))

    def collision(self, collider, player):
            if collider.colliderect(self.rect):
                if self.rect not in self.fruit_eaten:
                    self.surface.set_alpha(0)
                    player.points_count += 500
                    self.goal_wav.play()
                self.fruit_eaten.append(self.rect)
                

