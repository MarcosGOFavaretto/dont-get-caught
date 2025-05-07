import pygame
from .config import ASSETS_FOLDER

pygame.font.init()

merriweather = pygame.font.Font(f"{ASSETS_FOLDER}/Merriweather.ttf", 24)
merriweather_large = pygame.font.Font(f"{ASSETS_FOLDER}/Merriweather.ttf", 32)
menu = pygame.font.Font(f"{ASSETS_FOLDER}/menu.ttf", 32)