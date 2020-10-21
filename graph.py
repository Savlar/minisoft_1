import tkinter
from edge import Edge
from vertex import Vertex


class Graph:

    def __init__(self, canvas: tkinter.Canvas, planets_images, transport_images, mark=False):
        self.canvas = canvas
        self.image_size = 60
        self.free = False
        self.vertex_markers = {}
        self.all_paths = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
        self.path = []
        self.points = []
        self.edges = []
        self.vertices = []
        self.planets_images = planets_images
        self.transport_images = transport_images
        self.create_vertices()
        self.create_edges()
        self.draw_planets()
        if mark:
            self.canvas.bind('<Button-3>', self.mark_vertex)
        self.offset_last_point = 5

    def draw_planets(self):
        for vertex in self.vertices:
            self.canvas.create_image(vertex.x, vertex.y, image=self.planets_images[vertex.name], tag="draw_ground")

    def create_vertices(self):
        coords = [(900, 100), (600, 250), (1200, 250), (300, 400), (1500, 400), (600, 550), (1200, 550), (900, 700)]
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
                edge.image.add_image_info(self.canvas.create_image(x, y, image=self.transport_images[
                    'ufo_small' if t == 1 else 'rocket_small']), (x, y), t)

    def create_edges(self):
        for vertex in self.vertices:
            for neighbour in self.vertices:
                if vertex is not neighbour:
                    self.edges.append(Edge(vertex, neighbour))

    def find_edge(self, start, end):
        area = 35
        for edge in self.edges:
            if edge.connected_nodes(start[0], start[1], end[0], end[1], area):
                return edge
        return None

    def create_marker(self, vertex, order, mark=False):
        radius = self.image_size // 2
        text = self.canvas.create_text(vertex.x, vertex.y, text=order, fill='red',
                                       font=('Arial', 14, 'bold')) if mark else None
        self.vertex_markers[vertex] = [self.canvas.create_oval(vertex.x - radius, vertex.y - radius,
                                                               vertex.x + radius, vertex.y + radius, width=3,
                                                               outline='red'), text, order]

    def mark_vertex(self, e):
        if not self.free:
            self.delete_items(list(x[0] for x in self.vertex_markers.values()))
            self.vertex_markers = {}
        for vertex in self.vertices:
            if vertex.clicked(e.x, e.y):
                try:
                    self.delete_items(self.vertex_markers[vertex][0])
                    self.delete_items(self.vertex_markers[vertex][1])
                    deleted_order = self.vertex_markers[vertex][2]
                    for marker in self.vertex_markers.values():
                        if marker[2] > deleted_order:
                            marker[2] = marker[2] - 1
                            self.canvas.itemconfig(marker[1], text=marker[2])
                    self.vertex_markers.pop(vertex)
                except KeyError:
                    order = len(self.vertex_markers.keys())
                    self.create_marker(vertex, order + 1, self.free)

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

    def generate_paths(self):
        self.all_paths = {k: [] for k in self.all_paths}
        self.all_paths[0] = [(['mercury'], []), (['venus'], []), (['earth'], []), (['mars'], []),
                              (['jupiter'], []), (['saturn'], []), (['uranus'], []), (['neptune'], [])]
        for source in self.vertices:
            for dest in self.vertices:
                self.path = []
                self.find_path(source, dest)

    def find_path(self, current, dest):
        if len(self.path) > 8:
            return
        if current == dest and len(self.path) > 0:
            vertices = [self.path[0].start.name]
            transport = []
            for edge in self.path:
                vertices.append(edge.end.name)
                transport.append('rocket' if edge.get_transport_type() == 0 else 'ufo')
            self.all_paths[len(transport)].append((vertices, transport))
            return
        else:
            for edge in self.edges:
                if edge.start == current and edge.is_edge():
                    self.path.append(edge)
                    self.find_path(edge.end, dest)
                    self.path.pop()
