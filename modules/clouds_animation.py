from config import WIDTH

def animate_clouds(list: list, speed: int = 1):
    """Animar el fondo del juego en sí

    Args:
        list (list): de imagenes
        speed (int, optional): velocidad del movimiento del slide del fondo
    """

    for rect in list:
        rect.x += speed
        if rect.left >= WIDTH:
            rect.x = -WIDTH
        