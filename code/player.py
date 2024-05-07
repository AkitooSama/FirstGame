from typing import Tuple, Dict
from pygame import Vector2
from tools.timer import Timer
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[float, float], sprite_groups: pygame.sprite.Group,
                 collidable_sprites: pygame.sprite.Group) -> None:
        super().__init__(sprite_groups)

        self.image: pygame.Surface = pygame.image.load(r"C:\Users\DigiTronic\Downloads\sprites\Archive\character.png")
        self.sprites: pygame.sprite.Group = sprite_groups

        self.rect: pygame.Rect = self.image.get_frect(topleft=position)
        self.hitbox: pygame.Rect = self.rect.inflate(-30, 0)
        self.previous_rect: pygame.Rect = self.hitbox.copy()

        self.speed: int = 400
        self.gravity: int = 1300
        self.jump_height: int = 900
        self.jumps: int = 2
        self.direction: Vector2 = vector()

        self.space_key_released = True
        self.jumping = False
        self.player_state: Dict[str, bool] = {'jumping': False, 'falling': False, 'slowed': False}
        self.on_surface: Dict[str, bool] = {'floor': False, 'left': False, 'right': False}

        self.timers: Dict[str,Timer] = {'wall jump': Timer(400), 'wall slide block': Timer(250)}

        self.collidable_sprites: pygame.sprite.Group = collidable_sprites
        self.platform = None

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()
        input_vector: Vector2 = vector()

        if not self.timers['wall jump'].active:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                input_vector.x += 1

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                input_vector.x -= 1

            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        if keys[pygame.K_SPACE] and self.space_key_released:
            self.jumping = True
            self.space_key_released = False
        elif not keys[pygame.K_SPACE]:
            self.space_key_released = True

    def move(self, delta_time: float) -> None:
        self.hitbox.x += self.direction.x * self.speed * delta_time
        self.check_collision('horizontal')

        if self.on_surface['floor'] and not self.jumping:
            self.player_state['jumping'] = False
            self.player_state['falling'] = False
        elif not self.on_surface['floor'] and self.direction.y > 0:
            self.player_state['falling'] = True
        else: self.player_state['jumping'] = True

        if self.jumping:
            if self.on_surface['floor'] and self.jumps==2:
                self.image: pygame.Surface = pygame.image.load(r"C:\Users\DigiTronic\Downloads\shittysprite-removebg-preview.png")
                self.jump()
                self.jump_audio()
                self.timers['wall slide block'].activate()
                
            elif not any((self.on_surface['right'], self.on_surface['left'])) and self.jumps==1:
                self.image: pygame.Surface = pygame.image.load(r"C:\Users\DigiTronic\Downloads\sprites\Archive\character.png")
                self.jump()
                self.jump_audio()
                # self.timers['wall slide block'].activate() 
            elif any((self.on_surface['right'], self.on_surface['left'])) and not self.timers['wall slide block'].active:
                self.timers['wall jump'].activate()
                self.jump()
                self.jump_audio()
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jumping = False

        if not self.on_surface['floor'] and any((self.on_surface['right'], self.on_surface['left'])) and not self.timers['wall slide block'].active:
            self.hitbox.y += self.gravity / 10 * delta_time
        else:
            self.direction.y += self.gravity / 2 * delta_time
            self.hitbox.y += self.direction.y * delta_time
            self.direction.y += self.gravity / 2 * delta_time

        self.check_collision('vertical')
        self.rect.center = self.hitbox.center

    def jump(self):
        self.direction.y = 0
        self.direction.y = -self.jump_height
        self.player_state['jumping'] = True
        self.jumps -= 1

    def jump_audio(self):
        path_list: list = [
                    r"C:\Users\DigiTronic\Downloads\metallica.ogg",
                    r"C:\Users\DigiTronic\Downloads\amoung us.ogg",
                    r"C:\Users\DigiTronic\Downloads\Berserk Clang Sound Effect.mp3",
                    r"C:\Users\DigiTronic\Downloads\zaza.ogg",
                    r"C:\Users\DigiTronic\Downloads\1178025199573147788.ogg"
                ]
        path: str = random.choice(path_list)
        pygame.mixer.Sound(r"C:\Users\DigiTronic\Downloads\Berserk Clang Sound Effect.mp3").play()

    def platform_move(self, delta_time: float):
        if self.platform:
            self.hitbox.topleft += self.platform.direction * self.platform.speed * delta_time

    def check_surface_contact(self) -> None:
        self.floor_rect: pygame.Rect = pygame.Rect(self.hitbox.bottomleft, (self.hitbox.width, 2))
        self.right_rect: pygame.Rect = pygame.Rect(self.hitbox.topright + vector(0, self.hitbox.height / 4), (2, self.hitbox.height / 2))
        self.left_rect: pygame.Rect = pygame.Rect(self.hitbox.topleft + vector(-2, self.hitbox.height / 4), (2, self.hitbox.height / 2))

        collide_rects: list = [sprite.rect for sprite in self.collidable_sprites]

        if self.floor_rect.collidelist(collide_rects) >= 0:
            self.on_surface['floor'] = True
            self.jumps = 2
        else: self.on_surface['floor'] = False 
        self.on_surface['right'] = True if self.right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if self.left_rect.collidelist(collide_rects) >= 0 else False

        self.platform = None
        sprites = self.collidable_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(self.floor_rect):
                self.platform = sprite

    def check_collision(self, axis: str) -> None:
        for sprite in self.collidable_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if axis == 'horizontal':
                    if self.hitbox.left <= sprite.rect.right and int(self.previous_rect.left) >= int(sprite.previous_rect.right):
                        self.hitbox.left = sprite.rect.right

                    if self.hitbox.right >= sprite.rect.left and int(self.previous_rect.right) <= int(sprite.previous_rect.left):
                        self.hitbox.right = sprite.rect.left
                else:
                    if self.hitbox.top <= sprite.rect.bottom and int(self.previous_rect.top) >= int(sprite.previous_rect.bottom):
                        self.hitbox.top = sprite.rect.bottom
                        if hasattr(sprite, 'moving'):
                            self.hitbox.top += 8

                    if self.hitbox.bottom >= sprite.rect.top and int(self.previous_rect.bottom) <= int(sprite.previous_rect.top):
                        self.hitbox.bottom = sprite.rect.top
                    self.direction.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def debug_player(self):
        screen = self.sprites.display_surface
        offset = self.sprites.offset

        hitbox_rect = self.hitbox.move(offset)
        self.floor_rect = self.floor_rect.move(offset)
        self.right_rect = self.right_rect.move(offset)
        self.left_rect = self.left_rect.move(offset)

        pygame.draw.rect(screen, 'green', hitbox_rect)
        pygame.draw.rect(screen, 'red', self.floor_rect)
        pygame.draw.rect(screen, 'red', self.right_rect)
        pygame.draw.rect(screen, 'red', self.left_rect)

    def update(self, delta_time: float, _) -> None:
        self.previous_rect = self.hitbox.copy()
        self.update_timers()
        self.handle_input()
        self.check_surface_contact()
        self.platform_move(delta_time=delta_time)
        self.move(delta_time=delta_time)
