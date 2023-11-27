from config import *
from modules.levels import *
from modules.surface_and_rect_control import get_surface_and_rect
import json

MUSIC_OFF = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))
class Game():
    def __init__(self):
        with open("data/levels.json", "r") as json_file:
            self.levels = json.load(json_file)
            print(self.levels)
        
        self.music_off = False
        self.play, self.play_rect = get_surface_and_rect("assets/img/jugar.png", (450, 150))
        self.options, self.options_rect = get_surface_and_rect("assets/img/opciones.png", (450, 450))
        self.quit, self.quit_rect = get_surface_and_rect("assets/img/salir.png", (450, 600))
        self.bg, self.bg_rect = get_surface_and_rect("assets/img/main_bg.png")
        self.player, self.player_rect = get_surface_and_rect("assets/img/player.png", (540, 331))

        self.level_1, self.level_1_rect = get_surface_and_rect("assets/img/nivel1.png", (450, 200))
        self.level_2, self.level_2_rect = get_surface_and_rect("assets/img/nivel2.png", (450, 350))
        self.level_3, self.level_3_rect = get_surface_and_rect("assets/img/nivel3.png", (450, 500))

        self.selector_bg, self.selector_bg_rect = get_surface_and_rect("assets/img/level_selector.png")

        self.background_left, self.background_rect_left = get_surface_and_rect("assets/img/clouds.png", (-(WIDTH // 2), 0))
        self.background_right, self.background_rect_right = get_surface_and_rect("assets/img/clouds.png", (WIDTH // 2, 0))
        self.background_list = [self.background_rect_left, self.background_rect_right]

        self.info_left, self.info_left_rect = get_surface_and_rect("assets/img/info1.png", (100, 300))
        self.info_right, self.info_right_rect = get_surface_and_rect("assets/img/info2.png", (800, 300))

        self.title, self.title_rect = get_surface_and_rect("assets/img/title.png", (94, 40))

        self.game_over, self.game_over_rect = get_surface_and_rect("assets/img/game_over.png")
        self.game_over_flag = False

        self.current_level_index = 0
        self.current_level = Levels(self, **self.levels[self.current_level_index])

        self.music_on, self.music_on_rect = get_surface_and_rect("assets/img/musica_on.png", (450, 150))
        self.music_off_m, self.music_off_rect_m = get_surface_and_rect("assets/img/musica_off.png", (450, 300))
        self.sound_on, self.sound_on_rect = get_surface_and_rect("assets/img/sonido_on.png", (450, 450))
        self.sound_off, self.sound_off_rect = get_surface_and_rect("assets/img/sonido_off.png", (450, 600))

    def reset_level(self, level_index):
        self.current_level_index = level_index
        self.current_level = Levels(self, **self.levels[self.current_level_index])

    def main_menu(self):
        global MUSIC_OFF
        clock = pygame.time.Clock()
        running = True

        pygame.mixer.init()
        if MUSIC_OFF == False:
            pygame.mixer.music.load("./assets/sound/ost.wav")
            pygame.mixer.music.set_volume(0.4) 
            # inicio de música
            pygame.mixer.music.play(-1) # -1 es para dejar en bucle infinito
        else:
            pygame.mixer.music.pause()

        while running:
            clock.tick(FPS)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            screen.fill(WHITE)

            screen.blit(self.bg, self.bg_rect)
            animate_clouds(self.background_list, 1)
            screen.blit(self.background_left, self.background_rect_left)
            screen.blit(self.background_right, self.background_rect_right)
            screen.blit(self.title, self.title_rect)

            screen.blit(self.play, self.play_rect)
            screen.blit(self.options, self.options_rect)
            screen.blit(self.quit, self.quit_rect)
            screen.blit(self.player, self.player_rect)

            if self.play_rect.collidepoint(mouse_x, mouse_y):
                self.play.set_alpha(200)
                if pygame.mouse.get_pressed()[0]:
                    self.level_selector()

            elif self.options_rect.collidepoint(mouse_x, mouse_y):
                self.options.set_alpha(200)
                if pygame.mouse.get_pressed()[0]:
                    self.options_M()

            elif self.quit_rect.collidepoint(mouse_x, mouse_y):
                self.quit.set_alpha(200)
                if pygame.mouse.get_pressed()[0]:
                    pygame.quit()
                    exit()

            else:
                self.play.set_alpha(255)
                self.options.set_alpha(255)
                self.quit.set_alpha(255)
            pygame.display.flip()

    def level_selector(self):
        clock = pygame.time.Clock()
        gameplay = True

        while gameplay:
            clock.tick(FPS)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
            screen.fill(WHITE)
            screen.blit(self.selector_bg, self.selector_bg_rect)
            screen.blit(self.level_1, self.level_1_rect)
            screen.blit(self.level_2, self.level_2_rect)
            screen.blit(self.level_3, self.level_3_rect)
            screen.blit(self.info_left, self.info_left_rect)
            screen.blit(self.info_right, self.info_right_rect)

            if self.current_level_index == 1:
                print("OJO!")

            if self.level_1_rect.collidepoint(mouse_x, mouse_y):
                self.level_1.set_alpha(200)
                if pygame.mouse.get_pressed()[0]:
                    self.reset_level(0)
                    self.current_level.main()
            elif self.level_2_rect.collidepoint(mouse_x, mouse_y):
                self.level_2.set_alpha(200)
                if pygame.mouse.get_pressed()[0]:
                    self.reset_level(1)
                    self.current_level.main()
            elif self.level_3_rect.collidepoint(mouse_x, mouse_y):
                self.level_3.set_alpha(200)
                if pygame.mouse.get_pressed()[0]:
                    self.reset_level(2)
                    self.current_level.main()
            else:
                self.level_1.set_alpha(255)
                self.level_2.set_alpha(255)
                self.level_3.set_alpha(255)

            pygame.display.flip()

    def options_M(self):
        global MUSIC_OFF
        clock = pygame.time.Clock()
        self.options_mode = True

        while self.options_mode:
            clock.tick(FPS)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                elif pygame.key.get_pressed()[pygame.K_o]:
                    self.options_mode = False
                
                elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.options_mode = False
            
            screen.fill(WHITE)

            screen.blit(self.music_on, self.music_on_rect)
            screen.blit(self.music_off_m, self.music_off_rect_m)
            screen.blit(self.sound_on, self.sound_on_rect)
            screen.blit(self.sound_off, self.sound_off_rect)

            if self.music_on_rect.collidepoint(mouse_x, mouse_y):
                self.music_on.set_alpha(200)
                if pygame.mouse.get_pressed()[0]:
                    pygame.mixer.music.unpause()
                    MUSIC_OFF = False
            elif self.music_off_rect_m.collidepoint(mouse_x, mouse_y):
                self.music_off_m.set_alpha(200)
                if pygame.mouse.get_pressed()[0]:
                    pygame.mixer.music.pause()
                    MUSIC_OFF = True
            elif self.sound_on_rect.collidepoint(mouse_x, mouse_y):
                self.sound_on.set_alpha(200)
                if pygame.mouse.get_pressed()[0]:
                    self.sounds_effect = True
            elif self.sound_off_rect.collidepoint(mouse_x, mouse_y):
                self.sound_off.set_alpha(200)
                if pygame.mouse.get_pressed()[0]:
                    self.sounds_effect = False
            else:
                self.music_on.set_alpha(255)
                self.music_off_m.set_alpha(255)
                self.sound_off.set_alpha(255)
                self.sound_on.set_alpha(255)

            pygame.display.flip()

game_manager = Game()
game_manager.main_menu()

