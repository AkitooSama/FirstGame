import pygame
from typing import Dict
from pygame import Surface, Clock
from time import sleep
from settings import *
from level import Level
from debug import Debugger
from pytmx.util_pygame import load_pygame

class SelectLevel:
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.options = ['Level-1', 'Level-2', 'Level-3']
        self.selected_option = 0
        self.font = pygame.font.Font(None, 36)
        self.bg_color = (0, 0, 0)
        self.key_released = {pygame.K_UP: True, pygame.K_DOWN: True, pygame.K_RETURN: True}

    def draw(self):
        self.game_engine.game_display.fill(self.bg_color)
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, (255, 255, 255))
            rect = text.get_rect()
            rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 40)
            self.game_engine.game_display.blit(text, rect)

            if i == self.selected_option:
                pygame.draw.rect(self.game_engine.game_display, (255, 255, 255), rect, 2)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.key_released[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
            self.key_released[pygame.K_UP] = False
        elif keys[pygame.K_DOWN] and self.key_released[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
            self.key_released[pygame.K_DOWN] = False
        elif keys[pygame.K_RETURN] and self.key_released[pygame.K_RETURN]:
            if self.options[self.selected_option] == 'Level-1':
                print('yup-2')
                self.game_engine.current_level = Level(map_data=self.game_engine.map_files[0])
                self.game_engine.debugger = Debugger(engine=self.game_engine)
            elif self.options[self.selected_option] == 'Level-2':
                print('options lol')
            elif self.options[self.selected_option] == 'Level-3':
                pygame.quit()
                sys.exit()
            self.key_released[pygame.K_RETURN] = False

        if not keys[pygame.K_UP]:
            self.key_released[pygame.K_UP] = True
        if not keys[pygame.K_DOWN]:
            self.key_released[pygame.K_DOWN] = True
        if not keys[pygame.K_RETURN]:
            self.key_released[pygame.K_RETURN] = True

    def run(self, delta_time):
        self.handle_input()
        self.draw()

class Menu:
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.options = ['Start', 'Options', 'Exit']
        self.selected_option = 0
        self.font = pygame.font.Font(None, 36)
        self.bg_color = (0, 0, 0)
        self.key_released = {pygame.K_UP: True, pygame.K_DOWN: True, pygame.K_RETURN: True}

    def draw(self):
        self.game_engine.game_display.fill(self.bg_color)
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, (255, 255, 255))
            rect = text.get_rect()
            rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 40)
            self.game_engine.game_display.blit(text, rect)

            if i == self.selected_option:
                pygame.draw.rect(self.game_engine.game_display, (255, 255, 255), rect, 2)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.key_released[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
            self.key_released[pygame.K_UP] = False
        elif keys[pygame.K_DOWN] and self.key_released[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
            self.key_released[pygame.K_DOWN] = False
        elif keys[pygame.K_RETURN] and self.key_released[pygame.K_RETURN]:
            if self.options[self.selected_option] == 'Start':
                print('yup')
                sleep(1)
                self.game_engine.current_level = SelectLevel(self.game_engine)
                
            elif self.options[self.selected_option] == 'Options':
                print('options lol')
            elif self.options[self.selected_option] == 'Exit':
                pygame.quit()
                sys.exit()
            self.key_released[pygame.K_RETURN] = False

        if not keys[pygame.K_UP]:
            self.key_released[pygame.K_UP] = True
        if not keys[pygame.K_DOWN]:
            self.key_released[pygame.K_DOWN] = True
        if not keys[pygame.K_RETURN]:
            self.key_released[pygame.K_RETURN] = True

    def run(self, delta_time):
        self.handle_input()
        self.draw()

class GameEngine:
    def __init__(self, debug: bool = False) -> None:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(r"BTS - Dionysus.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)
        self.debug: bool = debug
        pygame.display.set_caption(GAME_TITLE)
        self.game_display: Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.frame_rate: int = FPS

        self.game_clock: Clock = pygame.time.Clock()
        
        self.map_files: Dict[int, str] = {0: load_pygame(r"data/levels/test2.tmx")}
        self.current_level: Menu = Menu(self)
        self.debugger: Debugger = None

    def run_game(self) -> None:
        while True:
            time_delta: float = self.game_clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYUP and self.debug:
                    if self.debugger:
                        if event.key == pygame.K_UP:
                            self.debugger.toggle()
            
            self.current_level.run(delta_time=time_delta)
            if self.debug and self.debugger: self.debugger.draw()
            pygame.display.update()

if __name__=='__main__':
    game_engine: GameEngine = GameEngine(debug=True)
    game_engine.run_game()