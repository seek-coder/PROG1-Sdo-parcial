from os import listdir
from os.path import isfile, join
import pygame

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites] 

def load_sprite_sheets(dir_A: str, dir_B: str, width: float, height:float, direction = False) -> dict: 
    """Facilita carga de sprite sheets

    Args:
        dir_A (str): Dirección A
        dir_B (str): Dirección B
        width (float): Ancho
        height (float): Alto
_
    """
    path = join("assets", dir_A, dir_B)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(surface)

            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
    
    return all_sprites