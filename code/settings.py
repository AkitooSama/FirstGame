import pygame
import sys
import random
from pygame.math import Vector2 as vector
from setup import config_contents, settings_contents

WINDOW_WIDTH: int = settings_contents['window_width']
WINDOW_HEIGHT: int = settings_contents['window_height']
TILE_SIZE: int = 48
ANIMATION_SPEED: int = 6
GAME_TITLE: str = settings_contents['game_title']
ICON_PATH: str = settings_contents['icon_path']
FPS: int = settings_contents['fps']
