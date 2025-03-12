class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"Coordinate({self.x}, {self.y})"
    
