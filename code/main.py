from typing import Dict
from pygame import Surface, Clock
from settings import *
from level import Level
from debug import Debugger
from pytmx.util_pygame import load_pygame

class GameEngine:
    def __init__(self, debug: bool = False) -> None:
        pygame.init()
        self.debug: bool = debug
        pygame.display.set_caption(GAME_TITLE)
        self.game_display: Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.frame_rate: int = FPS

        self.game_clock: Clock = pygame.time.Clock()
        
        self.map_files: Dict[int, str] = {0: load_pygame(r"data/levels/test2.tmx")}
        self.current_level: Level = Level(map_data=self.map_files[0])

        self.debugger: Debugger = Debugger(engine=self)

    def run_game(self) -> None:
        while True:
            time_delta: float = self.game_clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYUP and self.debug:
                    if event.key == pygame.K_UP:
                        self.debugger.toggle()
            
            self.current_level.run(delta_time=time_delta)
            if self.debug: self.debugger.draw()
            pygame.display.update()

if __name__=='__main__':
    game_engine: GameEngine = GameEngine(debug=True)
    game_engine.run_game()