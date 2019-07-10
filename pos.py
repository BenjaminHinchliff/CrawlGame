# class to allow for constructing the player's position
class Pos:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    # operator overrides
    def __iter__(self):
        return iter((self.x, self.y))

    def __str__(self):
        return "(" + self.x + ", " + self.y + ")"

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)