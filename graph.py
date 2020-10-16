import random
import tkinter
from PIL import ImageTk, Image

from edge import Edge
from serialize import load_data
from vertex import Vertex


class Graph:

    def __init__(self, canvas):
        self.canvas = canvas
        self.image_size = 50
        self.points = []
        self.edges = []
        self.vertices = []
        self.line = None
        self.create_vertices()
        self.create_edges()
        self.draw_edges()
        self.draw_planets()

    def draw_planets(self):
        self.canvas.images = []
        for vertex in self.vertices:
            image = ImageTk.PhotoImage(Image.open(f'textures/planets/{vertex.name}.png').
                                       resize((self.image_size, self.image_size)))
            self.canvas.images.append(image)
            self.canvas.create_image(vertex.x, vertex.y, image=self.canvas.images[-1])

    def create_vertices(self):
        coords = [(800, 150), (500, 300), (1100, 300), (200, 450), (1400, 450), (500, 600), (1100, 600), (800, 750)]
        planets = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
        for i in range(len(planets)):
            self.vertices.append(Vertex(*coords[i], planets[i]))

    def draw_edges(self):
        for edge in self.edges:
            if edge.points is not None:
                self.canvas.create_line(*edge.points, width=3, smooth=True, splinesteps=3, arrow=tkinter.LAST)
            if len(edge.image.image_coords) > 0:
                t = edge.image.img_type
                x, y = edge.image.image_coords
                edge.image.add_image_info(self.canvas.create_image(x, y, image=self.canvas.transport_types[t]), (x, y), t)

    def create_edges(self):
        for vertex in self.vertices:
            for neighbour in self.vertices:
                if vertex is not neighbour:
                    self.edges.append(Edge(vertex, neighbour))

    def find_edge(self, x1, y1, x2, y2):
        area = self.image_size + 50
        for edge in self.edges:
            if edge.connected_nodes(x1, y1, x2, y2, area):
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

    def load(self):
        x = load_data()
        self.edges = x[0]
        self.vertices = x[1]
        self.draw_planets()
        self.draw_edges()
