import pygame

class ClassroomGridPoint:
    def __init__(self, row: int, column: int, x: int, y: int, is_student_desk: bool):
        self.column = column
        self.row = row
        self.is_student_desk = is_student_desk
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"ClassroomGridPoint({self.row}, {self.column}, {self.is_student_desk}, {self.x}, {self.y})"

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

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, 'black', (self.x, self.y, self.width, self.height), 2)
        for point in self.grid_points:
            if point.is_student_desk:
                pygame.draw.circle(surface, 'brown', (point.x , point.y), 16)
                continue
            pygame.draw.circle(surface, 'red', (point.x, point.y), 10)

    # Função para criar um grid point a partir de uma posição do grid
    #
    def create_grid_point(self, row: int, column: int):
        x = int(self.column_width * column + self.x + self.column_width / 2)
        y = int(self.row_width * row + self.y + self.row_width / 2)
        is_student_desk = self.is_student_desk(row, column)
        return ClassroomGridPoint(row, column, x, y, is_student_desk)

    # Função que verifica se ponto do grid é carteira de aluno ou não
    #
    def is_student_desk(self, row: int, column: int) -> bool:
        return column % 2 == 0 and row % 2 != 0
    
    # Função para gerar os pontos de posição da sala de aula
    #   Classroom 3 x 4 / Mapa de pontos 6 x 7
    #   . . . . . . .       
    #   @ . @ . @ . @       
    #   . . . . . . .       @ - Carteira de aluno 
    #   @ . @ . @ . @       . - Ponto de movimento
    #   . . . . . . . 
    #   @ . @ . @ . @ 
    #
    def get_grid_points(self):
        movement_points = list[ClassroomGridPoint]()
        for r in range(self.grid_rows):
            for c in range(self.grid_columns):
                movement_points.append(self.create_grid_point(r, c))
        return movement_points