import random
import tkinter
from edge import Edge
from vertex import Vertex


class Graph:

    def __init__(self, canvas: tkinter.Canvas):
        self.canvas = canvas
        self.image_size = 50
        self.vertex_markers = {}
        self.points = []
        self.edges = []
        self.vertices = []
        self.line = None
        self.create_vertices()
        self.create_edges()
        self.draw_planets()
        self.canvas.bind('<Button-3>', self.mark_vertex)

    def draw_planets(self):
        for vertex in self.vertices:
            self.canvas.create_image(vertex.x, vertex.y, image=self.canvas.images[vertex.name])

    def create_vertices(self):
        coords = [(800, 150), (500, 300), (1100, 300), (200, 450), (1400, 450), (500, 600), (1100, 600), (800, 750)]
        planets = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
        for i in range(len(planets)):
            self.vertices.append(Vertex(*coords[i], planets[i]))

    def draw_edges(self):
        for edge in self.edges:
            if edge.points is not None and len(edge.points) > 0:
                edge.line = self.canvas.create_line(*edge.points, width=3, smooth=True, splinesteps=3,
                                                    arrow=tkinter.LAST, arrowshape=(16, 20, 6))
            if len(edge.image.image_coords) > 0:
                t = edge.image.img_type
                x, y = edge.image.image_coords
                edge.image.add_image_info(self.canvas.create_image(x, y, image=self.canvas.transport_types[t]), (x, y),
                                          t)

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

    def create_marker(self, vertex, order, mark=False):
        radius = self.image_size // 2
        text = self.canvas.create_text(vertex.x, vertex.y, text=order, fill='red', font=('Arial', 14, 'bold')) if mark else None
        self.vertex_markers[vertex] = [self.canvas.create_oval(vertex.x - radius, vertex.y - radius,
                                                               vertex.x + radius, vertex.y + radius, width=3,
                                                               outline='red'), text, order]

    def mark_vertex(self, e):
        marker_id = list(x[0] for x in self.vertex_markers.values())
        self.canvas.delete(marker_id)
        for vertex in self.vertices:
            if vertex.clicked(e.x, e.y):
                self.create_marker(vertex, 1)
                return

    def load(self, data):
        self.edges = data[0]
        self.vertices = data[1]
        self.draw_edges()

    def delete_items(self, *to_delete):
        for item in to_delete:
            self.canvas.delete(item)

    def delete_all(self):
        for marker in self.vertex_markers.values():
            self.delete_items(marker[0])
            self.delete_items(marker[1])
        for edge in self.edges:
            self.delete_items(*edge.delete_edge())
