from ..classroom.classroom import Classroom, ClassroomGridPoint
import random
from .render import TeacherRender
from .movement import MovementAction, MovementDirection, MovementActionType, MovementActionWalk, MovementActionWait
import math
import pygame
import copy
from ...config import ASSETS_FOLDER
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..render import GameRender

class Teacher:
    def __init__(self, game: 'GameRender', name: str = 'Default', initial_position: tuple = (0, 0)):
        self.game = game
        self.name = name
        self.initial_position = initial_position
        self.position: ClassroomGridPoint = copy.deepcopy(self.game.classroom.grid_points[initial_position[0]][initial_position[1]])
        self.current_action: MovementAction | None = None
        self.sleep_time_threshold = 2800
        self.time_to_wake_up = 8000
        self.wait_time_range = (1000, 3000)
        self.walk_speed = 2
        self.is_walking = False
        self.is_waiting = False
        self.is_sleeping = False
        self.direction: MovementDirection = MovementDirection.DOWN
        self.vision_radius = 200
        self.vision_angle = math.pi * 0.5
        self.vision_direction: MovementDirection | None = None
        self.footstep_sound = pygame.mixer.Sound(f'{ASSETS_FOLDER}/sounds/footstep.mp3')
        self.foot_dist = 10
        self.foot_size = 6
        self.step_amplitude = 10


    def set_default_position(self):
        self.position = copy.deepcopy(self.game.classroom.grid_points[self.initial_position[0]][self.initial_position[1]])

    def get_render(self):
        return TeacherRender(game=self.game, teacher=self)

    # Dentre as possibilidades de ações possíveis, é escolhida uma aleatoriamente.
    #     
    def get_next_action(self) -> MovementAction | None:
        random_action = random.choice(list(MovementActionType))
        if random_action == MovementActionType.WALK:
            movement_possibilities = self.get_movement_possibilities()
            next_action_final_point = random.choice(movement_possibilities)
            next_action = MovementActionWalk(
                current_point=self.position, 
                final_point=next_action_final_point, 
                walk_speed=self.walk_speed,
                walk_path=self.game.classroom.find_path(self.position, next_action_final_point))
            self.current_action = next_action
            return
        if random_action == MovementActionType.WAIT:
            random_direction = random.choice(list(MovementDirection))
            next_action = MovementActionWait(point=self.position, direction_to_look=random_direction, wait_time=random.randint(self.wait_time_range[0], self.wait_time_range[1]))
            self.current_action = next_action
            return
        raise ValueError("Invalid action type")

    # Função para retornar os possíveis pontos de movimento do professor:
    #
    def get_movement_possibilities(self) :
        movement_possibilities = list[ClassroomGridPoint]()
        for row in self.game.classroom.grid_points:
            for point in row:
                if point.classroom_desk is None and point != self.position:
                    movement_possibilities.append(point)
        student_neighbors = self.game.student.get_neighbor_grid_points()
        return movement_possibilities + student_neighbors
    
    # Função para retornar o intervalo de ângulo de visão do professor.
    #   - O intervalo de ângulo de visão é definido em relação à direção do professor.
    def get_vision_angle_range(self )-> tuple[float, float]:
        if self.vision_direction == MovementDirection.LEFT:
            return (-self.vision_angle / 2 + math.pi, self.vision_angle / 2 + math.pi)
        elif self.vision_direction == MovementDirection.RIGHT:
            return (-self.vision_angle / 2, self.vision_angle / 2)
        elif self.vision_direction == MovementDirection.UP:
            return (-self.vision_angle / 2 - math.pi / 2, self.vision_angle / 2 - math.pi / 2)
        elif self.vision_direction == MovementDirection.DOWN:
            return (-self.vision_angle / 2 + math.pi / 2, self.vision_angle / 2 + math.pi / 2)
        else:
            raise ValueError("Invalid vision direction")

    # Função para retornar os pontos que estão dentro do raio de visão do professor.
    #
    def get_vision_points(self):
        if self.is_sleeping:
            return list[ClassroomGridPoint]()
        points_in_vision = list[ClassroomGridPoint]()
        for column in self.game.classroom.grid_points:
            for point in column:
                if self.point_is_in_vision(point):
                    points_in_vision.append(point)
        return points_in_vision
    
    def is_looking_for_player(self) -> bool:
        if self.is_sleeping:
            return False
        for point in self.get_vision_points():
            if self.game.student.position.to_grid_point() == point.to_grid_point():
                return True
        return False
    
    # Verifica se o ponto está dentro do raio de visão e dentro do ângulo de visão.
    #
    def point_is_in_vision(self, point: ClassroomGridPoint) -> bool:
        angle_range = self.get_vision_angle_range()
        px, py = point.x, point.y
        cx, cy = self.position.x, self.position.y
        center_distance = math.sqrt(math.pow(px - cx, 2) + math.pow(py - cy, 2))
        if center_distance > self.vision_radius:
            return False
        angle = math.atan2(py - cy, px - cx)
        if angle < 0 and angle_range[0] > 0:
            angle += 2 * math.pi
        return angle_range[0] <= angle <= angle_range[1]