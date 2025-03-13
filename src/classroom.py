from .models import Coordinate

class ClassroomMapPoint:
    def __init__(self, row: int, column: int, x: int, y: int):
        self.column = column
        self.row = row
        self.is_student_desk = self.is_student_desk_condition()
        self.x = x
        self.y = y

    def is_student_desk_condition(self) -> bool:
        return self.column % 2 == 0 and self.row % 2 != 0
    
    def __str__(self):
        return f"ClassroomMapPoint({self.row}, {self.column}, {self.is_student_desk}, {self.x}, {self.y})"

class Classroom:
    def __init__(self, dimension: tuple[int, int], x: int, y: int, desk_rows: int, desk_columns: int):
        self.width, self.height = dimension
        self.desk_rows = desk_rows
        self.desk_columns = desk_columns
        self.map_rows = self.desk_rows * 2
        self.map_columns = (self.desk_columns * 2) - 1
        self.column_width = self.width / self.map_columns
        self.row_width = self.height / self.map_rows
        self.x = x
        self.y = y
        self.map_points = self.get_map_points()

    # Função para criar um map point a partir de uma posição do mapa de sala
    #
    def map_point(self, row: int, column: int):
        x = self.column_width * column + self.x
        y = self.row_width * row + self.y
        return ClassroomMapPoint(row, column, x, y)
    
    # Função para gerar os pontos de posição da sala de aula
    #   Classroom 3 x 4 / Mapa de pontos 6 x 7
    #   . . . . . . .       
    #   @ . @ . @ . @       
    #   . . . . . . .       @ - Carteira de aluno 
    #   @ . @ . @ . @       . - Ponto de movimento
    #   . . . . . . . 
    #   @ . @ . @ . @ 
    #
    def get_map_points(self):
        movement_points = list[ClassroomMapPoint]()
        for r in range(self.map_rows):
            for c in range(self.map_columns):
                movement_points.append(self.map_point(r, c))
        return movement_points