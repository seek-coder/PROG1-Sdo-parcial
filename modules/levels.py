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
import sqlite3

class Levels:
    
    def __init__(self, game_instance, background_image, tileset_image, farm_image, chickens_positions, player_position, enemies_positions, boxes_positions, box_large_positions, trap_positions, fruit_positions, sky_color, boss_position, daytime_image, straw_positions, straw_large_positions):
        """Controlador principal de niveles del juego. Todos los parámetros esperan LISTAS. Trabaja en conjunto al JSON
        """  
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background_left, self.background_rect_left = get_surface_and_rect(background_image, (-(WIDTH // 2), 0))
        self.background_right, self.background_rect_right = get_surface_and_rect(background_image, (WIDTH // 2, 0))
        self.background_list = [self.background_rect_left, self.background_rect_right]
        self.tileset, self.tileset_rect = get_surface_and_rect(tileset_image, (0, HEIGHT - 60))
        self.farm, self.farm_rect = get_surface_and_rect(farm_image, (20, HEIGHT - 370))
        self.daytime, self.daytime_rect = get_surface_and_rect(daytime_image)
        self.chicken_list = [Chickens(*pos) for pos in chickens_positions] 
        self.player = Player(*player_position) 
        self.enemy_list = [Enemies(*pos, "right") for pos in enemies_positions] 
        self.tile_list = [Tiles(*pos, "assets/img/box.png") for pos in boxes_positions] 
        self.tile_list += [Tiles(*pos, "assets/img/box_tile_large.png") for pos in box_large_positions] 
        self.tile_list += [Tiles(*pos, "assets/img/straw_tile.png") for pos in straw_positions] 
        self.tile_list += [Tiles(*pos, "assets/img/straw_tile_large.png") for pos in straw_large_positions] 
        self.tile_rect_list = [tile.rect for tile in self.tile_list]
        self.traps_list = [Traps(*pos, "assets/img/lousy.png") for pos in trap_positions]
        self.fruit_list = [Fruit(*pos, "assets/img/apple.png") for pos in fruit_positions]
        self.bullet_list_right = []
        self.bullet_list_left = []

        self.boss_position = boss_position

        self.selector_bg, self.selector_bg_rect = get_surface_and_rect("assets/img/level_selector.png")

        self.lost_game, self.lost_game_rect = get_surface_and_rect("assets/img/game_over.png")
        self.lost_time_game, self.lost_game_time_rect = get_surface_and_rect("assets/img/game_over_time.png")

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

        self.hit_wav = pygame.mixer.Sound("assets/sound/hit.wav")
        self.goal_wav = pygame.mixer.Sound("assets/sound/goal.wav")
        self.dead_wav = pygame.mixer.Sound("assets/sound/dead.wav")
        self.food_wav = pygame.mixer.Sound("assets/sound/food.wav")
        self.boss_killed_wav = pygame.mixer.Sound("assets/sound/boss_killed.wav")
        self.menu_wav = pygame.mixer.Sound("assets/sound/menu.wav")

        # ───── FUENTES ───── #
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

        # ───── TIMER POR NIVEL ───── #
        self.countdown_table, self.countdown_table_rect = get_surface_and_rect("assets/img/timer.png")
        self.time_countdown = 60

        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)

        # ───── DETECTOR DE NIVELES ───── #
        self.victory, self.victory_rect = get_surface_and_rect("assets/img/level_complete.png")
        self.victory_mode = False

    def victory_screen(self):
        pygame.mixer.music.stop()
        self.menu_wav.play()
        clock = pygame.time.Clock()
        self.victory_mode = True
        user_text = ""

        while self.victory_mode:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if len(user_text) < 10:
                        if event.key == pygame.K_RETURN:
                            print("El usuario escribe:", user_text)
                        elif event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]
                        else:
                            user_text += event.unicode
                    
                    if event.key == pygame.K_RETURN:
                        if user_text.strip():
                            user_text += event.unicode
                            # ───── SQL ───── #
                            try:
                                my_connect = sqlite3.connect("data/bd_segundo_parcial_programacion.db")
                                cursor = my_connect.cursor()
                                cursor.execute('INSERT INTO ranking(nombre, points) VALUES (?, ?)', (user_text, self.game_instance.total_points))
                                
                                my_connect.commit()
                                my_connect.close() # terminar conexión
                            except Exception as ex:
                                print(ex)
                        user_text = ""
                        self.menu_wav.stop()
                        self.game_instance.main_menu()

            self.screen.fill(WHITE)
            self.screen.blit(self.victory, self.victory_rect)
            text_surface = self.font.render(user_text, True, WHITE)
            points_surface = self.font.render(str(self.game_instance.total_points), True, WHITE)
            self.screen.blit(points_surface, (660, 330))
            self.screen.blit(text_surface, (590, 380))


            pygame.display.flip()

    def options(self):
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

            self.screen.blit(self.selector_bg, self.selector_bg_rect)
            self.screen.blit(self.music_on, self.music_on_rect)
            self.screen.blit(self.music_off_m, self.music_off_rect_m)
            self.screen.blit(self.sound_on, self.sound_on_rect)
            self.screen.blit(self.sound_off, self.sound_off_rect)

            if self.music_on_rect.collidepoint(mouse_x, mouse_y):
                self.music_on.set_alpha(200)
                if pygame.mouse.get_pressed()[0]:
                    pygame.mixer.music.unpause()
                    self.pause_music = False
                    print(self.pause_music)
            elif self.music_off_rect_m.collidepoint(mouse_x, mouse_y):
                self.music_off_m.set_alpha(200)
                if pygame.mouse.get_pressed()[0]:
                    pygame.mixer.music.pause()
                    self.pause_music = True
                    print(self.pause_music)
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

                elif pygame.key.get_pressed()[pygame.K_m]:
                    self.game_instance.main_menu()

            self.screen.fill(WHITE)
            self.screen.blit(self.pause_bg, self.pause_bg_rect)
            pygame.display.flip()

    def game_over_detect(self):
        if self.player.lives_count == 0:
            self.game_over_flag = True
            if self.sounds_effect:
                self.dead_wav.play()
    
    def chickens_detect(self):
        if len(self.chicken_list) == 0:
            self.game_instance.total_points += self.player.points_count
            print(self.game_instance.total_points)
            self.chickens_saved = True
            if self.sounds_effect:
                self.goal_wav.play()

    def main(self):
        clock = pygame.time.Clock()
        running = True

        while running and not self.game_over_flag:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == self.timer_event:
                    if self.time_countdown >= 0:
                        self.time_countdown -= 1
                        self.draw()
                        if self.time_countdown == 0:
                            self.show_game_over_by_time_screen()

                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.pause()

            self.update_entities()
            self.draw()

            if self.chickens_saved:
                self.next_level(self.game_instance.current_level_index)

            if self.game_instance.current_level_index == 2:
                if self.time_countdown > 30:
                    self.time_countdown = 30

        if self.victory_mode:
            self.victory_screen()

        if self.game_over_flag:
            self.show_game_over_screen()

    def next_level(self, current_level_i):
            next_level_i = (current_level_i + 1) % len(self.game_instance.levels)
            self.game_instance.reset_level(next_level_i)
            self.game_instance.current_level.main()

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

    def show_game_over_by_time_screen(self):
        self.screen.blit(self.lost_time_game, self.lost_game_time_rect)
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
        self.player.collision(self.tile_rect_list, self.traps_list, self.enemy_list, self.boss, self.sounds_effect)

        if self.boss:
            boss = self.boss[0]
            boss.update_sprite()
            boss.movement(100, 900)

        for chicken in self.chicken_list:
            chicken.collision(self.player.rect, self.player)
            if self.player.rect.colliderect(chicken):
                self.chicken_list.remove(chicken)
                if self.sounds_effect:
                    self.goal_wav.play()
            
        for enemy in self.enemy_list:
            enemy.update_sprite()
            if enemy.x_speed != 4:
                enemy.movement(350, 980)
            if enemy.x_speed == 4:
                enemy.movement(350, 520)
            if enemy.x_speed > 4:
                enemy.movement(640, 980)
        
        if self.boss_position != None:
            for boss in self.boss:
                boss.update_sprite()
                boss.movement(100, 900)
            
        for fruit in self.fruit_list:
            fruit.collision(self.player.rect, self.player, self.sounds_effect)

        bullets_to_remove = []
        enemies_to_remove = []
        
        for bullet, bullet_rect in self.bullet_list_right + self.bullet_list_left:
            for enemy in self.enemy_list:
                if bullet_rect.colliderect(enemy.rect):
                    bullets_to_remove.append((bullet, bullet_rect))
                    enemies_to_remove.append(enemy)
            if self.boss and boss.boss_lives_count > 0 and bullet_rect.colliderect(boss.rect):
                bullets_to_remove.append((bullet, bullet_rect))
                self.goal_wav.play()
                boss.boss_lives_count -= 1

        if self.boss and boss.boss_lives_count == 0:
            self.boss_killed_wav.play()
            self.player.points_count += 1200
            self.boss.clear()
        
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
            if self.sounds_effect:
                self.goal_wav.play()
            self.player.points_count += 100

        self.game_over_detect()
        self.chickens_detect()
    
    def draw(self):
        # print(self.game_instance.current_level_index)
        if self.game_instance.current_level_index > 2:
            self.victory_screen()
            self.menu_wav.play()

        self.screen.fill(self.sky_color)
        animate_clouds(self.background_list, 3)
        self.screen.blit(self.daytime, self.daytime_rect)
        self.screen.blit(self.background_left, self.background_rect_left)
        self.screen.blit(self.background_right, self.background_rect_right)
        self.screen.blit(self.tileset, self.tileset_rect)
        self.screen.blit(self.farm, self.farm_rect)

        self.screen.blit(self.countdown_table, (self.countdown_table_rect.x + 350, self.countdown_table_rect.y + 30))
        self.countdown_table_text = self.font.render(f"{self.time_countdown}:00", False, WHITE)
        self.screen.blit(self.countdown_table_text, (self.countdown_table_rect.x + 384, self.countdown_table_rect.y + 59))

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
            if boss.boss_lives_count > 0:
                boss.draw(self.screen, self.player)


        pygame.display.flip()