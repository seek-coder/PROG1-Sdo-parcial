import pygame
from .spritesheet_control import *
from .surface_and_rect_control import *
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, width: float, height: float, x_speed = 1, y_speed = 1):
        self.rect = pygame.Rect(x, y, width, height)
        self.sprite = pygame.Surface((width, height))
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.right = False
        self.left = False
        self.jumping = False
        self.running = False
        self.on_tile = False
        self.hit = False
        self.melee_attack = False
        self.range_attack = False

        self.gravity = 0.65

        self.direction = "right"

        self.animation_delay = 10

        self.animation_count = 0

        # ───── CARGA DE SPRITES SHEETS FUERA DEL BUCLE PARA EVITAR FPS BAJOS ───── #
        self.sprites_idle = load_sprite_sheets("img", "player", 63, 72, False)
        self.sprites_walk = load_sprite_sheets("img", "player", 72, 72, False)
        self.sprites_jump = load_sprite_sheets("img", "player", 82, 96, False)
        self.sprites_melee_attack = load_sprite_sheets("img", "player", 117, 72, False)
        self.sprites_range_attack = load_sprite_sheets("img", "player", 95, 72, False)
        self.sprites_hit = load_sprite_sheets("img", "player", 63, 72, False)

        # ───── CONTROL DE LOS DISPAROS ───── #
        self.shoot_to_the_right_list = []
        self.shoot_to_the_left_list = []
        self.last_shot_time = 0
        self.shoot_cooldown = 300

        # ───── CONTROL DEL MELEE ───── #
        self.last_melee_time = 0
        self.melee_cooldown = 300

        # ───── CONTROL DE HIT ───── #
        self.hit_timer = 0
        self.hit_duration = 30

        # ───── VIDAS ───── #
        self.lives_count = 3
        self.live, self.live_rect = get_surface_and_rect("assets/img/live.png")
        self.time_since_hit = 0
        self.hit_cooldown = 1000

        # ───── PUNTOS ───── #
        self.points_count = 0
        self.points_table, self.points_table_rect = get_surface_and_rect("assets/img/points.png")

        # ───── FUENTES ───── #
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

        # ───── SONIDOS ───── #
        pygame.mixer.init()
        self.hit_wav = pygame.mixer.Sound("assets/sound/hit.wav")

    def movement(self) -> list:
        # ───── MOVIMIENDO LATERAL Y SALTO ───── #
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction = "right"
            self.right = True
        else:
            self.right = False
            
        if keys[pygame.K_LEFT]:
            self.direction = "left"
            self.left = True
        else:
            self.left = False

        if keys[pygame.K_c]:
            current_time = pygame.time.get_ticks()
            if not self.range_attack and current_time - self.last_shot_time >= self.shoot_cooldown:
                self.range_attack = True

                self.last_shot_time = current_time

                # ───── CARGA DE BALAS ───── #
                self.shoot, self.shoot_rect = get_surface_and_rect("assets/img/shoot.png", (self.rect.x + 24, self.rect.y + 34))
                if self.direction == "right":
                    self.shoot_to_the_right_list.append((self.shoot, self.shoot_rect))
                else:
                    self.shoot_to_the_left_list.append((self.shoot, self.shoot_rect))
        else:
            self.range_attack = False

        if keys[pygame.K_z]:
            current_time = pygame.time.get_ticks()
            if not self.melee_attack and current_time - self.last_melee_time >= self.melee_cooldown:
                self.melee_attack = True
                self.last_melee_time = current_time
        else:
            self.melee_attack = False

        if self.right:
            self.running = True
            self.rect.x += self.x_speed
        elif self.left:
            self.running = True
            self.rect.x -= self.x_speed
        else:
            self.running = False

        if self.animation_count > 200: # evitar ad infinitum del contador
            self.animation_count = 0

        # ───── GRAVEDAD ───── #
        if keys[pygame.K_SPACE] and not self.jumping:
            self.y_speed = 14 # alto de salto
            self.jumping = True

        if self.jumping:
            self.y_speed -= self.gravity # permite que el movimiento sea más curvo y BAJE al personaje, porque hay un valor constante que se va restando en cada frame
            self.rect.y -= self.y_speed # cuando el valor de speed pasa de positivo a negativo, el personaje empieza a caer
            
            if self.rect.y >= floor_inicial_y: # cuando el jugador vuelve a Y inicial
                self.y_speed = 0
                self.rect.y = floor_inicial_y
                self.jumping = False 
        
        # ───── LÍMITES DE PANTALLA ───── #
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH - 36:
            self.rect.right = WIDTH - 36
            
        return self.shoot_to_the_right_list, self.shoot_to_the_left_list

    def collision(self, collider_list, trap_list, enemy_list, boss_list, sound_mode = True):
        self.gravity = 0.65

        # ───── HIT ───── #
        if self.hit:
            if self.hit_timer < self.hit_duration:
                self.hit_timer += 1
            else:
                self.hit_timer = 0
                self.hit = False

        if pygame.time.get_ticks() - self.time_since_hit > self.hit_cooldown:

            for boss in boss_list:
                if self.rect.colliderect(boss.rect):
                        self.hit = True
                        self.hit_timer = 0
                        self.time_since_hit = pygame.time.get_ticks()
                        if sound_mode:
                            self.hit_wav.play()
                        self.lives_count -= 1
            
            for trap in trap_list:
                if self.rect.colliderect(trap):
                    self.hit = True
                    self.hit_timer = 0
                    self.time_since_hit = pygame.time.get_ticks()
                    if sound_mode:
                        self.hit_wav.play()
                    self.lives_count -= 1

            for enemy in enemy_list:
                if self.rect.colliderect(enemy):
                    self.hit = True
                    self.hit_timer = 0
                    self.time_since_hit = pygame.time.get_ticks()
                    if sound_mode:
                        self.hit_wav.play()
                    self.lives_count -= 1

        for collider in collider_list:
            if self.rect.bottomleft == collider.topright:
                self.jumping = True
                self.gravity = 0.3
            elif self.rect.bottomright == collider.topleft:
                self.jumping = True
                self.gravity = 0.3

            if self.rect.colliderect(collider):
                if self.jumping:
                    if self.rect.y <= collider.y:
                        self.rect.bottom = collider.top
                        self.gravity = 0
                        self.jumping = False
                    elif self.rect.y >= collider.y:
                        self.rect.top = collider.bottom
                        self.gravity = 1

                else:
                    if self.rect.x <= collider.x:
                        self.rect.right = collider.left
                    if self.rect.x >= collider.x:
                        self.rect.left = collider.right

    def update_sprite(self):
        sprite_sheet = "player_idle"
        self.sprites = self.sprites_idle

        if self.running:
            sprite_sheet = "player_walk"
            self.sprites = self.sprites_walk
        
        if self.jumping:
            sprite_sheet = "player_jump"
            self.sprites = self.sprites_jump
        
        if self.melee_attack:
            sprite_sheet = "player_melee_attack"
            self.sprites = self.sprites_melee_attack
        
        if self.range_attack:
            sprite_sheet = "player_range_attack"
            self.sprites = self.sprites_range_attack
        
        if self.hit:
            sprite_sheet = "player_hit"
            self.sprites = self.sprites_hit

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites_animate = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // self.animation_delay) % len(sprites_animate) # actualización del spritesheet

        self.sprite = sprites_animate[sprite_index]
        self.animation_count += 1

    def draw(self, window):
        # pygame.draw.rect(window, GREEN, self.rect)
        window.blit(self.sprite, (self.rect.x, self.rect.y))
        window.blit(self.points_table, (self.points_table_rect.x + 50, self.points_table_rect.y + 30))
        # window.blit(self.countdown_table, (self.countdown_table_rect.x + 350, self.countdown_table_rect.y + 30))
        for surface, rect in self.shoot_to_the_left_list:
                window.blit(surface, rect)
                rect.x -= 7
        for surface, rect in self.shoot_to_the_right_list:
                window.blit(surface, rect)
                rect.x += 7
        
        if self.lives_count == 1:
            window.blit(self.live, (self.live_rect.x + 1100, self.live_rect.y + 50))
        if self.lives_count == 2:
            window.blit(self.live, (self.live_rect.x + 1100, self.live_rect.y + 50))
            window.blit(self.live, (self.live_rect.x + 1020, self.live_rect.y + 50))
        if self.lives_count == 3:
            window.blit(self.live, (self.live_rect.x + 1100, self.live_rect.y + 50))
            window.blit(self.live, (self.live_rect.x + 1020, self.live_rect.y + 50))
            window.blit(self.live, (self.live_rect.x + 940, self.live_rect.y + 50))
        
        self.points_count_text = self.font.render(f"{self.points_count:04d}", False, WHITE)
        window.blit(self.points_count_text, (self.points_table_rect.x + 134, self.points_table_rect.y + 66))

