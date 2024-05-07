from typing import Tuple
from pygame import Vector2
from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[float, float], surface: pygame.Surface = pygame.Surface((TILE_SIZE, TILE_SIZE)),
                 sprite_groups: pygame.sprite.Group=None) -> None:
        super().__init__(sprite_groups)

        self.default_image = surface.convert_alpha()
        self.image: pygame.Surface = self.default_image

        self.slowed_image = pygame.Surface(self.default_image.get_size())
        self.slowed_image.fill((0, 0, 0))

        self.rect: pygame.Rect = self.image.get_frect(topleft = position)
        self.previous_rect: pygame.Rect = self.rect.copy()

    def update(self, _: float, is_slowed: bool):
        if is_slowed:
            self.image = self.slowed_image.copy()
        else:
            self.image = self.default_image.copy()

class MovingSprites(Sprite):
    def __init__(self, start_position: tuple, end_position: tuple, moving_direction: str, speed: int, sprite_groups: pygame.sprite.Group) -> None:
        surface: pygame.Surface = pygame.Surface((200,40))
        super().__init__(start_position, surface, sprite_groups)

        if moving_direction == 'x': self.rect.midleft = start_position
        else: self.rect.midtop = start_position
        
        self.rect.center = start_position
        self.start_position: tuple = start_position
        self.end_position: tuple = end_position

        self.moving = True
        self.speed = speed
        self.direction: Vector2 = vector(1,0) if moving_direction == 'x' else vector(0,1)
        self.moving_direction: str = moving_direction


    def check_border(self):
        if self.moving_direction == 'x':
            if self.rect.right >= self.end_position[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.end_position[0]
            if self.rect.left <= self.start_position[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.start_position[0]

        # if self.moving_direction == 'y':
        #     if self.rect.bottom >= self.end_position[1] and self.direction.y == 1:
        #         self.direction.y = -1
        #         self.rect.bottom = self.end_position[1]
        #     if self.rect.top <= self.start_position[1] and self.direction.y == -1:
        #         self.direction.y = 1
        #         self.rect.top = self.start_position[1]

    def update(self, delta_time: float, is_slowed: bool):
        self.old_rect = self.rect.copy()
        self.check_border()

        if is_slowed: self.image.fill('black')
        else: self.image.fill('chocolate4')

        self.rect.topleft += self.direction * self.speed * delta_time
