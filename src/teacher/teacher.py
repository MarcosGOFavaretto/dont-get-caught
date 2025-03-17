from ..classrooom.classroom import Classroom, ClassroomGridPoint
import random
from .render import TeacherRender
from .movement import MovementAction, MovementDirection, MovementActionType, MovementActionWalk, MovementActionStand

class Teacher:
    def __init__(self, name: str, classroom: Classroom, initial_position: ClassroomGridPoint):
        self.name = name
        self.classroom = classroom
        self.current_grid_point_position: ClassroomGridPoint = initial_position if initial_position is not None \
            else classroom.create_grid_point(0, 0)
        self.next_action: MovementAction = None

    def get_render(self):
        return TeacherRender(teacher=self)

    # Dentre as possibilidades de movimento possíveis, é escolhida uma aleatoriamente.
    #     
    def get_next_action(self) -> MovementAction:
        random_action = random.choice(list(MovementActionType))

        if random_action == MovementActionType.WALK:
            movement_possibilities = self.get_movement_possibilities()
            next_action_point = random.choice(movement_possibilities)
            movement_direction = self.get_movement_direction(self.current_grid_point_position, next_action_point)
            return MovementActionWalk(point=next_action_point, direction=movement_direction, speed=6)
        
        if random_action == MovementActionType.STAND:
            random_direction = random.choice(list(MovementDirection))
            return MovementActionStand(point=self.current_grid_point_position, direction=random_direction, wait=1000)
    
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
