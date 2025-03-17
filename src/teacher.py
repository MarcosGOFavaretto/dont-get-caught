from .classroom import Classroom, ClassroomGridPoint
import random
from enum import Enum
import pygame

class MovementDirection(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN = 'DOWN'

class TeacherMovement:
    def __init__(self, point: ClassroomGridPoint, direction: MovementDirection):
        self.point = point
        self.direction = direction
        self.speed = 10

    def __str__(self):
        return f"TeacherMovement({self.point}, {self.direction})"

class Teacher:
    def __init__(self, name: str, classroom: Classroom, initial_position: ClassroomGridPoint):
        self.name = name
        self.classroom = classroom
        self.current_grid_point_position: ClassroomGridPoint = initial_position if initial_position is not None \
            else classroom.create_grid_point(0, 0)
        self.next_mv: TeacherMovement = None

    def render(self, surface: pygame.Surface):
        if self.next_mv is None:
            self.next_mv = self.next_movement()

        is_end_point = False
        if self.next_mv.direction == MovementDirection.LEFT:
            is_end_point = self.current_grid_point_position.x <= self.next_mv.point.x and self.current_grid_point_position.y == self.next_mv.point.y
        if self.next_mv.direction == MovementDirection.RIGHT:
            is_end_point = self.current_grid_point_position.x >= self.next_mv.point.x and self.current_grid_point_position.y == self.next_mv.point.y
        if self.next_mv.direction == MovementDirection.UP:
            is_end_point = self.current_grid_point_position.x == self.next_mv.point.x and self.current_grid_point_position.y <= self.next_mv.point.y
        if self.next_mv.direction == MovementDirection.DOWN:
            is_end_point = self.current_grid_point_position.x == self.next_mv.point.x and self.current_grid_point_position.y >= self.next_mv.point.y

        if not is_end_point:
            if self.next_mv.direction == MovementDirection.LEFT:
                self.current_grid_point_position.x -= self.next_mv.speed
            if self.next_mv.direction == MovementDirection.RIGHT:
                self.current_grid_point_position.x += self.next_mv.speed
            if self.next_mv.direction == MovementDirection.UP:
                self.current_grid_point_position.y -= self.next_mv.speed
            if self.next_mv.direction == MovementDirection.DOWN:
                self.current_grid_point_position.y += self.next_mv.speed
        else:
            self.current_grid_point_position = self.classroom.create_grid_point(self.next_mv.point.row, self.next_mv.point.column)
            self.next_mv = self.next_movement()
        pygame.draw.circle(surface, 'green', (self.current_grid_point_position.x, self.current_grid_point_position.y), 20)

    # Dentre as possibilidades de movimento possíveis, é escolhida uma aleatoriamente.
    #     
    def next_movement(self) -> TeacherMovement:
        movement_possibilities = self.get_movement_possibilities()
        next_movement_point = random.choice(movement_possibilities)
        movement_direction = self.get_movement_direction(self.current_grid_point_position, next_movement_point)
        # self.current_grid_point_position = next_movement_point
        return TeacherMovement(
            point=next_movement_point,
            direction=movement_direction,
        )
    
    # Retorna a direção do movimento a partir do ponto inicial e ponto final
    #
    def get_movement_direction(self, start_point: ClassroomGridPoint, finish_point: ClassroomGridPoint) -> MovementDirection:
        if start_point.row < finish_point.row:
            return MovementDirection.DOWN
        elif start_point.row > finish_point.row:
            return MovementDirection.UP
        elif start_point.column < finish_point.column:
            return MovementDirection.RIGHT
        elif start_point.column > finish_point.column:
            return MovementDirection.LEFT

    # Função para calcular o próximo movimento possível do professor:
    #   Regras de movimento:
    #   - O professor pode se mover por todo o corredor da sala (mesmo movimento da torre no xadrez);
    #   - Uma carteira não pode ser um ponto de movimento;
    #   - O professor não pode pular por cima de uma carteira;
    #
    def get_movement_possibilities(self) -> list[ClassroomGridPoint]:
        column_grid_points = [mp for mp in self.classroom.grid_points if mp.column == self.current_grid_point_position.column]
        row_grid_points = [mp for mp in self.classroom.grid_points if mp.row == self.current_grid_point_position.row]
        possible_movements = list[ClassroomGridPoint]()

        # up
        for row_index in range(self.current_grid_point_position.row, 0, -1):
            point = column_grid_points[row_index - 1]
            if point.is_student_desk:
                break
            possible_movements.append(point)

        # down
        for row_index in range(self.current_grid_point_position.row + 1, self.classroom.grid_rows, 1):
            point = column_grid_points[row_index]
            if point.is_student_desk:
                break
            possible_movements.append(point)

        # left
        for column_index in range(self.current_grid_point_position.column, 0, -1):
            point = row_grid_points[column_index - 1]
            if point.is_student_desk:
                break
            possible_movements.append(point)

        # right
        for column_index in range(self.current_grid_point_position.column + 1, self.classroom.grid_columns, 1):
            point = row_grid_points[column_index]
            if point.is_student_desk:
                break
            possible_movements.append(point)

        return possible_movements
