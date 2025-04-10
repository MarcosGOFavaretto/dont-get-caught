import pygame
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_NAME
from src.game import Game

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)
clock = pygame.time.Clock()
running = True

game = Game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    game.render(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()