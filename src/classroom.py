class Classroom:
    def __init__(self, dimension: tuple[int, int], x: int, y: int, rows: int, columns: int):
        self.dimension = dimension
        self.rows = rows
        self.columns = columns
        self.x = x
        self.y = y