import pygame
from modules.player import Player
from modules.enemies import Enemies
from modules.chickens import Chickens
from modules.fruit import Fruit
from modules.tiles import Tiles
from modules.boss import Boss
from modules.surface_and_rect_control import get_surface_and_rect
from modules.clouds_animation import animate_clouds
from modules.traps import Traps
from config import *

MUSIC_OFF = False

class Levels:
    def __init__(self, game_instance, background_image, tileset_image, farm_image, chickens_positions, player_position, enemies_positions, boxes_positions, box_large_positions, trap_positions, fruit_positions, sky_color, boss_position):
        """Controlador principal de niveles del juego. Todos los parámetros esperan LISTAS.
        """
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background_left, self.background_rect_left = get_surface_and_rect(background_image, (-(WIDTH // 2), 0))
        self.background_right, self.background_rect_right = get_surface_and_rect(background_image, (WIDTH // 2, 0))
        self.background_list = [self.background_rect_left, self.background_rect_right]
        self.tileset, self.tileset_rect = get_surface_and_rect(tileset_image, (0, HEIGHT - 60))
        self.farm, self.farm_rect = get_surface_and_rect(farm_image, (20, HEIGHT - 370))
        self.chicken_list = [Chickens(*pos) for pos in chickens_positions] 
        self.player = Player(*player_position) 
        self.enemy_list = [Enemies(*pos, "right") for pos in enemies_positions] 
        self.tile_list = [Tiles(*pos, "assets/img/box.png") for pos in boxes_positions] 
        self.tile_list += [Tiles(*pos, "assets/img/box_tile_large.png") for pos in box_large_positions] 
        self.tile_rect_list = [tile.rect for tile in self.tile_list]
        self.traps_list = [Traps(*pos, "assets/img/lousy.png") for pos in trap_positions]
        self.fruit_list = [Fruit(*pos, "assets/img/apple.png") for pos in fruit_positions]
        self.bullet_list_right = []
        self.bullet_list_left = []
        self.boss_position = boss_position

        self.lost_game, self.lost_game_rect = get_surface_and_rect("assets/img/game_over.png")

        self.boss = [Boss(*pos, "right") for pos in boss_position]
        self.last_info, self.last_info_rect = get_surface_and_rect("assets/img/last_info.png", (760, 360))

        self.sky_color = sky_color
        self.pause_bg, self.pause_bg_rect = get_surface_and_rect("assets/img/pause.png")

        self.game_over_flag = False
        self.game_instance = game_instance

        self.chickens_saved = False

        self.music_on, self.music_on_rect = get_surface_and_rect("assets/img/musica_on.png", (450, 150))
        self.music_off_m, self.music_off_rect_m = get_surface_and_rect("assets/img/musica_off.png", (450, 300))
        self.sound_on, self.sound_on_rect = get_surface_and_rect("assets/img/sonido_on.png", (450, 450))
        self.sound_off, self.sound_off_rect = get_surface_and_rect("assets/img/sonido_off.png", (450, 600))

        self.sounds_effect = True

        bullet_lists = self.player.movement()

        self.bullet_list_right, self.bullet_list_left = bullet_lists

        self.options_mode = False

    def options(self):
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
            
            self.screen.fill(WHITE)

            self.screen.blit(self.music_on, self.music_on_rect)
            self.screen.blit(self.music_off_m, self.music_off_rect_m)
            self.screen.blit(self.sound_on, self.sound_on_rect)
            self.screen.blit(self.sound_off, self.sound_off_rect)

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

    def pause(self):
        clock = pygame.time.Clock()
        paused = True

        while paused:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    paused = False
                
                elif pygame.key.get_pressed()[pygame.K_q]:
                    pygame.quit()
                    exit()

                elif pygame.key.get_pressed()[pygame.K_o]:
                    self.options()

            self.screen.fill(WHITE)
            self.screen.blit(self.pause_bg, self.pause_bg_rect)
            pygame.display.flip()

    def game_over_detect(self):
        if self.player.lives_count == 0:
            self.game_over_flag = True
            self.dead_wav.play()
    
    def chickens_detect(self):
        if len(self.chicken_list) == 0:
            self.chickens_saved = True
            self.goal_wav.play()

    def main(self):
        pygame.mixer.init()
        pygame.mixer.music.load("./assets/sound/ost.wav")
        pygame.mixer.music.set_volume(0.4) 
        pygame.mixer.music.play(-1)


        self.hit_wav = pygame.mixer.Sound("assets/sound/hit.wav")
        self.goal_wav = pygame.mixer.Sound("assets/sound/goal.wav")
        self.dead_wav = pygame.mixer.Sound("assets/sound/dead.wav")
        self.food_wav = pygame.mixer.Sound("assets/sound/food.wav")
        pygame.mixer.music.unpause()
        clock = pygame.time.Clock()
        running = True

        while running and not self.game_over_flag:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.pause()

            self.update_entities()
            self.draw()

            if self.chickens_saved:
                self.next_level(self.game_instance.current_level_index)
        
        if self.game_over_flag:
            self.show_game_over_screen()

    def next_level(self, current_level_i):
            global MUSIC_OFF

            next_level_i = (current_level_i + 1) % len(self.game_instance.levels)
            self.game_instance.reset_level(next_level_i)
            self.game_instance.current_level.main()
            if MUSIC_OFF == False:
                pygame.mixer.music.pause()

    def show_game_over_screen(self):
        self.screen.blit(self.lost_game, self.lost_game_rect)
        pygame.mixer.music.pause()
        waiting = True

        while waiting:
            clock = pygame.time.Clock()
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if pygame.key.get_pressed()[pygame.K_r]:
                waiting = False
                self.game_over_flag = False
                self.game_instance.main_menu()

            pygame.display.flip()

    def update_entities(self):
        self.player.movement()
        self.player.update_sprite()
        self.player.collision(self.tile_rect_list, self.traps_list, self.enemy_list, self.boss)

        for chicken in self.chicken_list:
            chicken.collision(self.player.rect, self.player)
            if self.player.rect.colliderect(chicken):
                self.chicken_list.remove(chicken)
                self.goal_wav.play()
            
        for enemy in self.enemy_list:
            enemy.update_sprite()
            enemy.movement(350, 980)
        
        if self.boss_position != None:
            for boss in self.boss:
                boss.update_sprite()
                boss.movement(100, 900)
            
        for fruit in self.fruit_list:
            fruit.collision(self.player.rect, self.player)

        bullets_to_remove = []
        enemies_to_remove = []
        
        for bullet, bullet_rect in self.bullet_list_right + self.bullet_list_left:
            for enemy in self.enemy_list:
                if bullet_rect.colliderect(enemy.rect):
                    bullets_to_remove.append((bullet, bullet_rect))
                    enemies_to_remove.append(enemy)
        
        if self.player.melee_attack:
            for enemy in self.enemy_list:
                if self.player.rect.colliderect(enemy.rect):
                    self.enemy_list.remove(enemy)
                    self.player.points_count += 300
        
        for bullet, bullet_rect in bullets_to_remove:
            if (bullet, bullet_rect) in self.bullet_list_right:
                self.bullet_list_right.remove((bullet, bullet_rect))
            elif (bullet, bullet_rect) in self.bullet_list_left:
                self.bullet_list_left.remove((bullet, bullet_rect))
        
        for enemy in enemies_to_remove:
            self.enemy_list.remove(enemy)
            self.goal_wav.play()
            self.player.points_count += 100

        print(self.player.points_count)
        self.game_over_detect()
        self.chickens_detect()
    
    def draw(self):
        self.screen.fill(self.sky_color)
        animate_clouds(self.background_list, 3)
        self.screen.blit(self.background_left, self.background_rect_left)
        self.screen.blit(self.background_right, self.background_rect_right)
        self.screen.blit(self.tileset, self.tileset_rect)
        self.screen.blit(self.farm, self.farm_rect)

        for tile in self.tile_list:
            tile.draw(self.screen)

        for chicken in self.chicken_list:
            chicken.draw(self.screen)

        self.player.draw(self.screen)

        for enemy in self.enemy_list:
            enemy.draw(self.screen)

        for trap in self.traps_list:
            trap.draw(self.screen)
        
        for fruit in self.fruit_list:
            fruit.draw(self.screen)

        for boss in self.boss:
            boss.draw(self.screen)

        pygame.display.flip()