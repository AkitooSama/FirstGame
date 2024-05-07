from settings import *

class Menu:
    def __init__(self, game_engine, options):
        self.game_engine = game_engine
        self.options = options
        self.selected_option = 0
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.bg_color = BLACK
        self.key_released = {pygame.K_UP: True, pygame.K_DOWN: True, pygame.K_RETURN: True}

    def draw(self):
        self.game_engine.game_display.fill(self.bg_color)
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, WHITE)
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 40))
            self.game_engine.game_display.blit(text, rect)
            if i == self.selected_option:
                pygame.draw.rect(self.game_engine.game_display, WHITE, rect, 2)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.key_released[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
            self.key_released[pygame.K_UP] = False
        elif keys[pygame.K_DOWN] and self.key_released[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
            self.key_released[pygame.K_DOWN] = False
        elif keys[pygame.K_RETURN] and self.key_released[pygame.K_RETURN]:
            self.select_option()
            self.key_released[pygame.K_RETURN] = False

        for key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN]:
            if not keys[key]:
                self.key_released[key] = True

    def select_option(self):
        pass

    def run(self, delta_time):
        self.handle_input()
        self.draw()