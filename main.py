import pygame
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GAME_NAME
from src.app import App

pygame.init()

pygame.init()
pygame.mixer.init()

main_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(GAME_NAME)
clock = pygame.time.Clock()
running = True

app = App(main_surface)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    app.render()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()