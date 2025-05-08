import pygame
from .config import ASSETS_FOLDER

pygame.font.init()

merriweather = pygame.font.Font(f"{ASSETS_FOLDER}/Merriweather.ttf", 24)
menu = pygame.font.Font(f"{ASSETS_FOLDER}/menu.ttf", 32)

game_over_title = pygame.font.Font(f"{ASSETS_FOLDER}/menu.ttf", 52)
game_over_btn_label = pygame.font.Font(f"{ASSETS_FOLDER}/menu.ttf", 18)