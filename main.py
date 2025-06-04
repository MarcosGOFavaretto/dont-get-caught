import pygame
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GAME_NAME, ASSETS_FOLDER
from src.app import App

pygame.init()

pygame.init()
pygame.mixer.init()


logo = pygame.image.load(f'{ASSETS_FOLDER}/logo.png')
pygame.display.set_icon(logo)

main_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(GAME_NAME)
clock = pygame.time.Clock()
running = True

app = App(main_surface)

while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    app.render(event_list)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()