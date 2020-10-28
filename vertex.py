class Vertex:

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def clicked(self, x, y):
        return self.x - 25 <= x <= self.x + 25 and self.y - 25 <= y <= self.y + 25
