from settings import *
from menu import Menu

class SelectLevel(Menu):
    def __init__(self, game_engine):
        super().__init__(game_engine, ['Level-1', 'Level-2', 'Level-3'])

    def select_option(self):
        if self.options[self.selected_option] == 'Level-1':
            print('Loading Level-1')
        elif self.options[self.selected_option] == 'Level-2':
            print('Loading Level-2')
        elif self.options[self.selected_option] == 'Level-3':
            pygame.quit()
            sys.exit()