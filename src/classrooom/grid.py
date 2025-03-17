class ClassroomGridPoint:
    def __init__(self, row: int, column: int, x: int, y: int, is_student_desk: bool):
        self.column = column
        self.row = row
        self.is_student_desk = is_student_desk
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"ClassroomGridPoint({self.row}, {self.column}, {self.is_student_desk}, {self.x}, {self.y})"