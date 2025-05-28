import pygame
from .config import ASSETS_FOLDER

pygame.font.init()

merriweather = pygame.font.Font(f"{ASSETS_FOLDER}/Merriweather.ttf", 24)
menu = pygame.font.Font(f"{ASSETS_FOLDER}/menu.ttf", 32)

game_final_screen_title = pygame.font.Font(f"{ASSETS_FOLDER}/Merriweather.ttf", 100)
game_final_subtext = pygame.font.Font(f"{ASSETS_FOLDER}/Merriweather.ttf", 18)
game_final_btn_label = pygame.font.Font(f"{ASSETS_FOLDER}/Merriweather.ttf", 18)

teacher_zzz = pygame.font.Font(f"{ASSETS_FOLDER}/Merriweather.ttf", 12)