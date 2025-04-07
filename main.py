import pygame
from src.classrooom.classroom import Classroom
from src.teacher.teacher import Teacher
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

classroom = Classroom(dimension=(1000, 600), x=0, y=0, rows=8, columns=11)
teacher = Teacher(name='Oliver Taz', classroom=classroom, initial_position=classroom.grid_points[0][0])

classroom = classroom.get_render()
teacher = teacher.get_render()

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Don't get caught")
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    classroom.render(screen)
    teacher.render(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()