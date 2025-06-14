import pygame
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GAME_NAME, ASSETS_FOLDER, FULLSCREEN
from src.app import App
import ctypes
import sys

# --- Windows-specific DPI awareness fix ---
try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    # This might fail on older Windows versions or non-Windows OS
    pass

pygame.init()
pygame.mixer.init()

logo = pygame.image.load(f'{ASSETS_FOLDER}/images/logo.png')
pygame.display.set_icon(logo)

if len(sys.argv) > 1 and sys.argv[1] == '--no-fullscreen':
    FULLSCREEN = False 

info = pygame.display.Info()
WINDOW_WIDTH = info.current_w
WINDOW_WIDTH = info.current_h
main_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN | pygame.SCALED if FULLSCREEN else 0)

pygame.display.set_caption(GAME_NAME)
clock = pygame.time.Clock()
running = True

app = App(main_surface)

while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    quit = app.render(event_list)
    if quit:
        running = False
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()