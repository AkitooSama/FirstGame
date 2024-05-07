from settings import *
from level import Level
from player import Player


class Debugger:
    def __init__(self, engine):
        self.engine = engine
        self.level: Level = self.engine.current_level
        self.player: Player = self.level.player

        self.font: pygame.Font = pygame.font.Font(None, 24)
        self.enabled: bool = False

    def toggle(self) -> None:
        self.enabled = not self.enabled

    def draw_text(self, text, position) -> None:
        if self.level.is_slowed: color = 'green'
        else: color = 'red'
        surface = self.font.render(text, True, color)
        self.engine.game_display.blit(surface, position)

    def draw(self) -> None:
        if self.enabled:
            self.draw_text(f"Player state: {self.player.player_state}", (0, 0))
            self.draw_text(f"On surface: {self.player.on_surface}", (0, 40))

            self.player.debug_player()