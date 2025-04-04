from ..classrooom.classroom import Classroom, ClassroomGridPoint
import random
from .render import TeacherRender
from .movement import MovementAction, MovementDirection, MovementActionType, MovementActionWalk, MovementActionWait
class Teacher:
    def __init__(self, name: str, classroom: Classroom, initial_position: ClassroomGridPoint):
        self.name = name
        self.classroom = classroom
        self.current_grid_point_position: ClassroomGridPoint = initial_position if initial_position is not None \
            else self.classroom[0][0]
        self.current_action: MovementAction = None
        self.sleep_time_threshold = 2800
        self.time_to_wake_up = 4000
        self.wait_time_range = (1000, 3000)
        self.walk_speed = 3
        self.is_walking = False
        self.is_waiting = False
        self.is_sleeping = False
        self.direction = None

    def get_render(self):
        return TeacherRender(teacher=self)

    # Dentre as possibilidades de ações possíveis, é escolhida uma aleatoriamente.
    #     
    def get_next_action(self) -> MovementAction:
        random_action = random.choice(list(MovementActionType))
        if random_action == MovementActionType.WALK:
            movement_possibilities = self.get_movement_possibilities()
            next_action_final_point = random.choice(movement_possibilities)
            return MovementActionWalk(
                current_point=self.current_grid_point_position, 
                final_point=next_action_final_point, 
                walk_speed=self.walk_speed,
                walk_path=self.classroom.find_path(self.current_grid_point_position, next_action_final_point))
        
        if random_action == MovementActionType.WAIT:
            random_direction = random.choice(list(MovementDirection))
            return MovementActionWait(point=self.current_grid_point_position, direction=random_direction, wait_time=random.randint(self.wait_time_range[0], self.wait_time_range[1]))

    # Função para retornar os possíveis pontos de movimento do professor:
    #
    def get_movement_possibilities(self) -> list[ClassroomGridPoint]:
        movement_possibilities = []
        for row in self.classroom.grid_points:
            for point in row:
                if not point.is_student_desk and point != self.current_grid_point_position:
                    movement_possibilities.append(point)
        return movement_possibilities