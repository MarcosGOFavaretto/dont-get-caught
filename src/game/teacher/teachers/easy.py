from ..teacher import Teacher, MovementAction, MovementDirection, MovementActionType, MovementActionWalk, MovementActionWait
import random
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..render import GameRender

class TeacherEasy(Teacher):
    def __init__(self, game: 'GameRender'):
        super().__init__(game=game, name="Easy", initial_position=(int(game.classroom.grid_columns / 2), 0))
        self.last_action = None
        self.walk_speed = 1.5

    def get_next_action(self) :
        self.last_action = self.current_action

        if self.last_action is None:
            self.current_action = self.get_wait_action(direction_to_look=MovementDirection.DOWN)
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
            walk_path=self.game.classroom.find_path(self.position, next_action_final_point))
    
    def get_wait_action(self, direction_to_look: MovementDirection | None = None) -> MovementAction:  
        if direction_to_look is None:
            directions_to_look = list(MovementDirection)
            wall_directions = self.get_neighbor_wall_direction()
            directions_to_look = list(filter(lambda x: x.value not in [d.value for d in wall_directions], directions_to_look))
            direction_to_look = random.choice(directions_to_look)
        return MovementActionWait(point=self.position, direction_to_look=direction_to_look, wait_time=random.randint(self.wait_time_range[0], self.wait_time_range[1]))


    def get_neighbor_wall_direction(self) :
        neighbors = [
            dict(offset=(-1, 0), direction=MovementDirection.LEFT),
            dict(offset=(+1, 0), direction=MovementDirection.RIGHT),
            dict(offset=(0, -1), direction=MovementDirection.UP),
            dict(offset=(0, +1), direction=MovementDirection.DOWN) 
        ]

        directions: list[MovementDirection] = []
        for neighbor in neighbors:
            nx = self.position.column + neighbor.get('offset')[0]
            ny = self.position.row + neighbor.get('offset')[1]
            if nx < 0 or nx >= len(self.game.classroom.grid_points) or ny < 0 or ny >= len(self.game.classroom.grid_points[0]):
                directions.append(neighbor.get('direction'))
        return directions
