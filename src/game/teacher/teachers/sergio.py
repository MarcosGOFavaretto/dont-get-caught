from ..teacher import Teacher, MovementAction, MovementDirection, MovementActionType, MovementActionWalk, MovementActionWait
import random
from ....utils import get_angle_between_points

class TeacherSergio(Teacher):
    def __init__(self, game: any):
        super().__init__(game=game, name="Sérgio")
        self.last_action = None

    def get_next_action(self) -> MovementAction:
        self.last_action = self.current_action

        if self.last_action is None:
            self.current_action = self.get_walk_action()
            return

        if self.last_action.action_type == MovementActionType.WALK:
            self.current_action = self.get_wait_action()
            return
            
        if self.last_action.action_type == MovementActionType.WAIT:
            self.current_action = self.get_walk_action()
            return

        raise ValueError("Invalid action type")

    def get_walk_action(self):
        movement_possibilities = self.get_movement_possibilities()
        next_action_final_point = random.choice(movement_possibilities)
        return MovementActionWalk(
            current_point=self.position, 
            final_point=next_action_final_point, 
            walk_speed=self.walk_speed,
            walk_path=self.classroom.find_path(self.position, next_action_final_point))

    def get_movement_possibilities(self) :
        movement_possibilities = []
        for row in self.classroom.grid_points:
            for point in row:
                if not point.is_student_desk and point != self.position and self.classroom.grid_point_is_close_to_wall(point):
                    movement_possibilities.append(point)
        return movement_possibilities

    def get_wait_action(self):  
        directions_to_look = list(MovementDirection)
        wall_direction = self.get_neighbor_wall_direction()
        if wall_direction is not None:
            directions_to_look = list(filter(lambda x: x.value != wall_direction.value, directions_to_look))
        direction_to_look = random.choice(directions_to_look)
        return MovementActionWait(point=self.position, direction_to_look=direction_to_look, wait_time=random.randint(self.wait_time_range[0], self.wait_time_range[1]))


    def get_neighbor_wall_direction(self) -> MovementDirection:
        neighbors = [
            dict(offset=(-1, 0), direction=MovementDirection.LEFT),
            dict(offset=(+1, 0), direction=MovementDirection.RIGHT),
            dict(offset=(0, -1), direction=MovementDirection.UP),
            dict(offset=(0, +1), direction=MovementDirection.DOWN) 
        ]

        for neighbor in neighbors:
            nx = self.position.column + neighbor.get('offset')[0]
            ny = self.position.row + neighbor.get('offset')[1]
            if nx < 0 or nx >= len(self.classroom.grid_points) or ny < 0 or ny >= len(self.classroom.grid_points[0]):
                return neighbor.get('direction')
