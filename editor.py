import random
import tkinter
from PIL import ImageTk, Image


class Vertex:

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name


class Edge:

    def __init__(self, start, end, points=None, line=None):
        self.start = start
        self.end = end
        self.points = points
        self.line = line


class TaskEditor:

    def __init__(self):
        self.frame = tkinter.Frame(root)
        self.frame.pack()
        self.canvas = tkinter.Canvas(self.frame, bg='white', width=1920, height=1080)
        self.canvas.pack()
        self.canvas.create_rectangle(10, 80, 1650, 850)
        self.image_size = 50
        self.points = []
        self.images = []
        self.edges = []
        self.vertices = []
        self.line = None
        self.create_vertices()
        self.create_edges()
        # self.draw_edges()
        self.draw_planets()
        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.end_drawing)
        self.canvas.bind('<Button-3>', self.cancel_drawing)
        self.canvas.bind('<Button-2>', self.delete_edge)

    def draw_planets(self):
        for vertex in self.vertices:
            image = ImageTk.PhotoImage(Image.open(f'textures/planets/{vertex.name}.png').
                                       resize((self.image_size, self.image_size)))
            self.images.append(image)
            self.canvas.create_image(vertex.x, vertex.y, image=self.images[-1])

    def create_vertices(self):
        coords = [(800, 150), (500, 300), (1100, 300), (200, 450), (1400, 450), (500, 600), (1100, 600), (800, 750)]
        planets = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
        for i in range(len(planets)):
            self.vertices.append(Vertex(*coords[i], planets[i]))

    def draw_edges(self):
        for edge in self.edges:
            self.canvas.create_line(*edge.points, arrow=tkinter.LAST)

    def create_edges(self):
        for vertex in self.vertices:
            for neighbour in self.vertices:
                if vertex is not neighbour:
                    self.edges.append(Edge(vertex, neighbour))

    def start_drawing(self, e):
        self.points = [e.x, e.y]

    def mouse_drag(self, e):
        self.points.append(e.x)
        self.points.append(e.y)
        if self.line is None:
            self.line = self.canvas.create_line(*self.points, width=3)
        else:
            self.canvas.coords(self.line, *self.points)

    def end_drawing(self, e):
        copy_points = self.simplify_line(e)
        self.canvas.delete(self.line)
        if len(copy_points) > 4:
            edge = self.find_edge(copy_points[0], copy_points[1], copy_points[-2], copy_points[-1])
            print(edge)
            if edge is not None:
                self.line = self.canvas.create_line(*copy_points, width=3, smooth=True, splinesteps=3,
                                                    arrow=tkinter.LAST)
                if edge.line is not None:
                    self.canvas.delete(edge.line)
                edge.line = self.line
                edge.points = self.points[:]
        self.line = None

    def find_edge(self, x1, y1, x2, y2):
        area = self.image_size + 50
        for edge in self.edges:
            if edge.start.x - area <= x1 <= edge.start.x + area and edge.start.y - area <= y1 <= edge.start.y + area \
                    and edge.end.x - area <= x2 <= edge.end.x + area and edge.end.y - area <= y2 <= edge.end.y + area:
                return edge
        return None

    def simplify_line(self, e):
        try:
            copy_points = [self.points[0], self.points[1]]
        except IndexError:
            return []
        for i in range(2, len(self.points), 2):
            if random.random() < 0.02:
                copy_points.append(self.points[i])
                copy_points.append(self.points[i + 1])
        copy_points.append(e.x)
        copy_points.append(e.y)
        return copy_points

    def cancel_drawing(self, e):
        self.points = []
        self.canvas.delete(self.line)
        self.line = None

    def delete_edge(self, e):
        for edge in self.edges:
            if edge.points is None: continue
            for i in range(0, len(edge.points), 2):
                x, y = edge.points[i], edge.points[i + 1]
                if e.x - 20 <= x <= e.x + 20 and e.y - 20 <= y <= e.y + 20:
                    edge.points = []
                    self.canvas.delete(edge.line)
                    edge.line = None
                    return


if __name__ == '__main__':
    root = tkinter.Tk()
    TaskEditor()
    root.mainloop()
