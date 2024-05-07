from settings import *
from sprites import Sprite, MovingSprites
from player import Player
from pytmx import TiledMap
from groups import AllSprites

class Level:
    def __init__(self, map_data: TiledMap) -> None:
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        self.all_sprites: AllSprites = AllSprites()
        self.collidable_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.slowed = False
        self.is_slowed = False
        self.setup(map_data=map_data)

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_t]:
            self.slowed = True
        else:
            self.slowed = False
            self.is_slowed = False
            self.player.player_state['slowed'] = False

    def setup(self, map_data: TiledMap) -> None:
        for x, y, surface in map_data.get_layer_by_name('Terrain').tiles():
            if surface:
                self.sprite = Sprite(position=(x*TILE_SIZE, y*TILE_SIZE), surface=surface,
                        sprite_groups=(self.all_sprites, self.collidable_sprites))

        for game_object in map_data.get_layer_by_name('Objects'):
            if game_object.name == 'player':
                self.player = Player(position=(game_object.x, game_object.y), sprite_groups=self.all_sprites,
                       collidable_sprites=self.collidable_sprites)
        for game_object in map_data.get_layer_by_name('Object'):
                if game_object.image:
                    Sprite(position=(game_object.x, game_object.y), surface=game_object.image, sprite_groups=(self.all_sprites, self.collidable_sprites))

        # for game_object in map_data.get_layer_by_name('Moving Objects'):
        #     if game_object.name == 'helicopter':
        #         if game_object.width > game_object.height:
        #             moving_direction = 'x'
        #             start_position = (game_object.x, game_object.y + game_object.height / 2)
        #             end_position = (game_object.x + game_object.width, game_object.y + game_object.height / 2)
        #         # else:
        #         #     moving_direction = 'y'
        #         #     start_position = (game_object.x + game_object.width / 2, game_object.y)
        #         #     end_position = (game_object.x + game_object.width / 2, game_object.y + game_object.height)
        #             speed = game_object.properties['speed']
        #             self.moving_sprites = MovingSprites(start_position=start_position, end_position=end_position,
        #                         moving_direction=moving_direction, speed=speed, sprite_groups=(self.all_sprites, self.collidable_sprites))

    def check_slowed(self, delta_time: float) -> float:
        if self.slowed and self.player.player_state['falling'] and self.player.direction.y > 0:
            self.player.player_state['slowed'] = True
            self.is_slowed = True
            self.player.jumps = 0
            self.display_surface.fill('firebrick2')
            return delta_time * 0.1
        else:
            self.is_slowed = False
            self.display_surface.fill('gray5')
            return delta_time

    def run(self, delta_time: float) -> None:
        self.handle_input()
        adjusted_delta_time: float = self.check_slowed(delta_time)
        self.all_sprites.draw(target_position = self.player.hitbox.center)
        self.all_sprites.update(adjusted_delta_time, self.is_slowed)