from .render import ClassroomRender
from .grid import ClassroomGridPoint
from .path_find_algorithm import a_star
class Classroom:
    def __init__(self, dimension: tuple[int, int], x: int, y: int, rows: int, columns: int):
        self.width, self.height = dimension
        self.grid_rows = rows
        self.grid_columns = columns
        self.column_width = self.width / self.grid_columns
        self.row_width = self.height / self.grid_rows
        self.x = x
        self.y = y
        self.grid_points = self.get_grid_points()

    def get_render(self):
        return ClassroomRender(self)

    # Função para criar um grid point a partir de uma posição do grid
    #
    def create_grid_point(self, column: int, row: int):
        x = int(self.column_width * column + self.x + self.column_width / 2)
        y = int(self.row_width * row + self.y + self.row_width / 2)
        is_student_desk = self.is_student_desk(column, row)
        return ClassroomGridPoint(column, row, x, y, is_student_desk)

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
    def get_grid_points(self):
        movement_points = list[list[ClassroomGridPoint]]()
        for c in range(self.grid_columns):
            grid_col = list[ClassroomGridPoint]()
            for r in range(self.grid_rows):
                grid_col.append(self.create_grid_point(c, r))
            movement_points.append(grid_col)
        return movement_points

    def get_grid_coordenates(self):
        coordenates = list[list[tuple[int, int]]]()
        for column in self.grid_points:
            column_coordenates = []
            for point in column:
                column_coordenates.append((point.column, point.row))
            coordenates.append(column_coordenates)
        return coordenates

    def find_path(self, initial_point: ClassroomGridPoint, final_point: ClassroomGridPoint):
        initial_point = (initial_point.column, initial_point.row)
        final_point = (final_point.column, final_point.row)
        path_coordenates = a_star(self.grid_points, initial_point, final_point)
        path = [self.grid_points[c][r] for c, r in path_coordenates]
        return path
