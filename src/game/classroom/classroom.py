from .render import ClassroomRender
from .grid import ClassroomGridPoint
from .path_find_algorithm import a_star
from pygame import Surface
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..render import GameRender

class Classroom:
    def __init__(self, game: 'GameRender', dimension: tuple[int, int], x: int, y: int, rows: int, columns: int):
        self.game = game
        self.width, self.height = dimension
        self.grid_rows = rows
        self.grid_columns = columns
        self.column_width = self.width / self.grid_columns
        self.row_width = self.height / self.grid_rows
        self.x = x
        self.y = y
        self.grid_points = self._generate_grid_points()

    def get_render(self, surface: Surface):
        return ClassroomRender(self.game, classroom=self, surface=surface)
    
    def get_center_coordenate(self):
        center_x = int(self.x + self.width / 2)
        center_y = int(self.y + self.height / 2)
        return (center_x, center_y)

    # Função para criar um grid point a partir de uma posição do grid
    #
    def create_grid_point(self, column: int, row: int):
        x = int(self.column_width * column + self.x + self.column_width / 2)
        y = int(self.row_width * row + self.y + self.row_width / 2)
        return ClassroomGridPoint(column, row, x, y, classroom_desk=None)

    # Função que verifica se ponto do grid é carteira de aluno ou não
    #
    def is_student_desk(self, column: int, row: int) -> bool:
        return column % 2 == 0 and row % 2 != 0
    
    # Função para gerar uma matriz de pontos de posição da sala de aula
    #   Mapa de pontos 6 x 7
    #   . . . . . . .       
    #   @ . @ . @ . @       
    #   . . . . . . .       @ - Carteira de aluno 
    #   @ . @ . @ . @       . - Ponto de movimento
    #   . . . . . . . 
    #   @ . @ . @ . @ 
    #
    def _generate_grid_points(self):
        movement_points = list[list[ClassroomGridPoint]]()
        for c in range(self.grid_columns):
            grid_col = list[ClassroomGridPoint]()
            for r in range(self.grid_rows):
                grid_col.append(self.create_grid_point(c, r))
            movement_points.append(grid_col)
        return movement_points

    def find_path(self, initial_point: ClassroomGridPoint, final_point: ClassroomGridPoint):
        initial_point_coordenate = (initial_point.column, initial_point.row)
        final_point_coordenate = (final_point.column, final_point.row)
        path_coordenates = a_star(self.grid_points, initial_point_coordenate, final_point_coordenate)
        if path_coordenates is None:
            return []
        path = [self.grid_points[c][r] for c, r in path_coordenates]
        return path

    def get_grid_coordenates(self):
        coordenates = list[list[tuple[int, int]]]()
        for column in self.grid_points:
            column_coordenates = []
            for point in column:
                column_coordenates.append((point.column, point.row))
            coordenates.append(column_coordenates)
        return coordenates
    

    def grid_point_is_close_to_wall(self, grid_point: ClassroomGridPoint) -> bool:
        neighbors = [(-1, 0),(+1, 0),(0, +1),(0, -1)]
        for neighbor in neighbors:
            nx = grid_point.column + neighbor[0]
            ny = grid_point.row + neighbor[1]
            if nx < 0 or nx >= len(self.grid_points) or ny < 0 or ny >= len(self.grid_points[0]):
                return True
        return False

    def get_total_desks(self):
        total_desks = 0
        for column in self.grid_points:
            for point in column:
                if point.classroom_desk is not None:
                    total_desks += 1
        return total_desks
    
    def get_grid_points_list(self):
        grid_points: list[ClassroomGridPoint] = []
        for column in self.grid_points:
            for point in column:
                grid_points.append(point)
        return grid_points

