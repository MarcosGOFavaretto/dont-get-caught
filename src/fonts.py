import pygame
from .config import ASSETS_FOLDER

pygame.font.init()

merriweather = pygame.font.Font(f"{ASSETS_FOLDER}/fonts/Merriweather.ttf", 24)
menu_lg = pygame.font.Font(f"{ASSETS_FOLDER}/fonts/menu.ttf", 32)
menu_sm = pygame.font.Font(f"{ASSETS_FOLDER}/fonts/menu.ttf", 18)
menu_how_to_play_description = pygame.font.Font(f"{ASSETS_FOLDER}/fonts/Merriweather.ttf", 26)

game_final_screen_title = pygame.font.Font(f"{ASSETS_FOLDER}/fonts/Merriweather.ttf", 100)
game_final_subtext = pygame.font.Font(f"{ASSETS_FOLDER}/fonts/Merriweather.ttf", 18)
game_final_btn_label = pygame.font.Font(f"{ASSETS_FOLDER}/fonts/Merriweather.ttf", 18)

teacher_zzz = pygame.font.Font(f"{ASSETS_FOLDER}/fonts/Merriweather.ttf", 12)

clock = pygame.font.Font(f"{ASSETS_FOLDER}/fonts/digital-7-mono.ttf", 32)