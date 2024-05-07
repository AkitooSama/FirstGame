from settings import *
from pygame.math import Vector2

class AllSprites(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()

        self.display_surface: pygame.Surface = pygame.display.get_surface()
        self.offset: Vector2 = vector()

    def draw(self, target_position):
        self.offset.x = -(target_position[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_position[1] - WINDOW_HEIGHT / 2)

        for sprite in self.sprites():
            offset_position = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_position)