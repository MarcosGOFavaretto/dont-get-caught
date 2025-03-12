from models import Coordinate
from classroom import Classroom
import random
from enum import Enum

class TeacherMovementPoint(Coordinate):
    def __init__(self, coordinate: Coordinate, row: int, column: int):
        super().__init__(x=coordinate.x, y=coordinate.y)
        self.column = column
        self.row = row

class MovementDirection(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN = 'DOWN'

class TeacherMovement:
    def __init__(self, point: TeacherMovementPoint, direction: MovementDirection):
        self.point = point
        self.direction = direction

class Teacher:
    def __init__(self, name: str, classroom: Classroom):
        self.name = name
        self.classroom = classroom
        self.classroom_movement_points = self.get_movement_points()
        self.current_position: TeacherMovementPoint = TeacherMovementPoint(Coordinate(0, 0), 2, 1)

    # Dentre as possibilidades de movimento possíveis, é escolhida uma aleatoriamente.
    #     
    def next_movement(self) -> TeacherMovement:
        movement_possibilities = self.get_movement_possibilities()
        next_movement_point = random.choice(movement_possibilities)
        movement_direction = self.get_movement_direction(self.current_position, next_movement_point)
        return TeacherMovement(
            point=next_movement_point,
            direction=movement_direction
        )
    
    # Retorna a direção do movimento a partir do ponto inicial e ponto final
    #
    def get_movement_direction(self, start_point: TeacherMovementPoint, finish_point: TeacherMovementPoint) -> MovementDirection:
        if start_point.row < finish_point.row:
            return MovementDirection.DOWN
        elif start_point.row > finish_point.row:
            return MovementDirection.UP
        elif start_point.column < finish_point.column:
            return MovementDirection.RIGHT
        elif start_point.column > finish_point.column:
            return MovementDirection.LEFT

    # Regras para movimentação:
    #   - O professor pode apenas se mover por todo o corredor da sala (mesmo movimento da torre no xadrez);
    #   - O professor não pode pular por cima de uma carteira;
    #
    def get_movement_possibilities(self) -> list[TeacherMovementPoint]:
        possible_movements = list[TeacherMovementPoint]()
        for point in self.classroom_movement_points:
            is_same_row_or_column = point.row == self.current_position.row or point.column == self.current_position.column
            is_not_jumping_desk = point.row >= self.current_position.row + 1 \
                or point.column >= self.current_position.column + 1 \
                or point.row <= self.current_position.row - 1 \
                or point.column <= self.current_position.column - 1
            is_valid = is_same_row_or_column and is_not_jumping_desk
            if is_valid:
                possible_movements.append(point)
        return possible_movements


    # Função para gerar os pontos de movimento do professor na sala
    #   Classroom 4 x 3 / Mapa de pontos 7 x 6
    #   . . . . . . .       
    #   @ . @ . @ . @       
    #   . . . . . . .       @ - Carteira de aluno 
    #   @ . @ . @ . @       . - Ponto de movimento
    #   . . . . . . . 
    #   @ . @ . @ . @ 
    #
    def get_movement_points(self) -> list[TeacherMovementPoint]:
        mv_points_columns = (self.classroom.columns * 2) - 1
        mv_points_rows = self.classroom.rows * 2
        x, y = self.classroom.dimension
        column_size = x / mv_points_columns
        row_size = y / mv_points_rows
        movement_points = list[TeacherMovementPoint]()
        for r in range(mv_points_rows):
            for c in range(mv_points_columns):
                point_is_desk = c % 2 == 0 and r % 2 != 0
                if point_is_desk:
                    continue
                movement_points.append(TeacherMovementPoint(
                    row=r,
                    column=c,
                    coordinate=Coordinate(column_size * c, row_size * r),
                ))
        return movement_points
t = Teacher(name='Oliver Taz', classroom=Classroom(dimension=(1000, 1000), x=0, y=0, rows=3, columns=4))

nx = t.next_movement()

print('( row:', nx.point.row + 1, 'col:', nx.point.column + 1, ')', ' => ', nx.direction)