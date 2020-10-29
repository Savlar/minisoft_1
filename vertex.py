class Vertex:

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def clicked(self, x, y):
        return self.x - 14 <= x <= self.x + 14 and self.y - 14 <= y <= self.y + 14
