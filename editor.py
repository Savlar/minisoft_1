import itertools
import random
import tkinter
from graph import Graph
from serialize import save_data


class GraphEditor(Graph):

    def __init__(self, canvas, planets_images, transport_images, max_transport_units, parent=None):
        if parent is not None:
            self.canvas = parent.canvas
            self.edges = parent.edges
            self.transport_images = parent.transport_images
            self.max_transport_units = parent.max_transport_units
            self.image_names = parent.image_names
        else:
            super(GraphEditor, self).__init__(canvas, planets_images, transport_images, max_transport_units)
        self.saved = False
        self.canvas.tag_bind("draw_ground", '<Button-1>', self.start_drawing)
        self.canvas.tag_bind("draw_ground", '<B1-Motion>', self.mouse_drag)
        self.canvas.tag_bind("draw_ground", '<ButtonRelease-1>', self.end_drawing)
        self.canvas.tag_bind("change_transport_unit", '<Button-1>', self.change_transport_unit)
        self.canvas.bind('<Button-2>', self.delete_edge)
        self.canvas.unbind('<Button-3>')
        self.line = None

    def change_transport_unit(self, e):
        for edge in self.edges:
            if edge.image.clicked(e.x, e.y):
                x, y = edge.image.image_coords
                t = edge.image.img_type + 1 if edge.image.img_type < len(self.image_names.keys()) - 1 else 0
                self.delete_items(edge.image.image)
                edge.image.add_image_info(
                    self.canvas.create_image(x, y, image=self.transport_images[self.image_names[t]][1],
                                             tag="change_transport_unit"), (x, y), t)
                break

    def save(self):
        save_data(self.edges, self.vertices)

    def start_drawing(self, e):
        self.points = [(e.x, e.y)]

    def delete_edge(self, e):
        for edge in self.edges:
            if edge.clicked_edge(e.x, e.y):
                self.delete_items(*edge.delete_edge())
                return

    def mouse_drag(self, e):
        self.points.append((e.x, e.y))
        points = list(itertools.chain(*self.points))
        if self.line is None:
            self.line = self.canvas.create_line(points, width=3)
        else:
            self.canvas.coords(self.line, points)

    def end_drawing(self, e):
        copy_points = self.simplify_line(e)
        self.canvas.delete(self.line)
        if len(copy_points) > 4:
            edge = self.find_edge(copy_points[0], copy_points[-1])
            if edge is not None:
                self.line = self.canvas.create_line(list(itertools.chain(*copy_points)), width=3, smooth=True,
                                                    splinesteps=3, arrow=tkinter.LAST, arrowshape=(16, 20, 6))
                if edge.line is not None:
                    self.delete_items(*edge.delete_edge())
                edge.line = self.line
                edge.points = copy_points[:]
                self.transport_selection(edge)
        self.line = None

    def transport_selection(self, edge):
        coords = self.canvas.coords(edge.line)
        middle = len(coords) // 2
        if middle % 2 == 1:
            middle -= 1
        x, y = coords[middle], coords[middle + 1]
        edge.image.add_image_info(self.canvas.create_image(x, y, image=self.transport_images['rocket_small'][1],
                                                           tag="change_transport_unit"), (x, y), 0)

    def simplify_line(self, e):
        try:
            copy_points = [self.points[0]]
        except IndexError:
            return []
        for i in range(1, len(self.points) - 3):
            if random.random() < 0.2 or len(self.points) < 30:
                copy_points.append(self.points[i])
        copy_points.append((e.x, e.y))
        return copy_points

    def close(self):
        self.canvas.tag_unbind('draw_ground', '<Button-1>')
        self.canvas.tag_unbind('draw_ground', '<B1-Motion>')
        self.canvas.tag_unbind('draw_ground', '<ButtonRelease-1>')
        self.canvas.unbind('<Button-3>')
        self.canvas.unbind('<Button-2>')
        self.canvas.unbind('<Button-3>')

    def correct_map(self):
        self.generate_paths()
        for i in range(2, 9):
            if len(self.all_paths[i]) > 0:
                return True
        return False
