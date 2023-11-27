def get_surface_and_rect(dir: str, position = (0, 0)):
    """Facilita carga de superficies y rectángulos
    """
    from pygame import image

    surface = image.load(dir).convert_alpha()
    rect = surface.get_rect()
    rect.topleft = position
    
    return surface, rect