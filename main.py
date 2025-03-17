import pygame
from src.classrooom.classroom import Classroom
from src.teacher.teacher import Teacher

classroom = Classroom(dimension=(1000, 600), x=0, y=0, rows=8, columns=11)
teacher = Teacher(name='Oliver Taz', classroom=classroom, initial_position=classroom.create_grid_point(0, 0))

classroom = classroom.get_render()
teacher = teacher.get_render()

pygame.init()
screen = pygame.display.set_mode((1000, 600))
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
    clock.tick(60)

pygame.quit()