import itertools
import random
import tkinter
from graph import Graph
from serialize import save_data


class GraphEditor(Graph):

    def __init__(self, canvas, planets_images, transport_images, max_transport_units, wrong_map_image):
        super(GraphEditor, self).__init__(canvas, planets_images, transport_images, max_transport_units)
        self.saved = False
        self.wrong_map_image = wrong_map_image
        self.wrong_map_object = None
        self.canvas.tag_bind("draw_ground", '<Button-1>', self.start_drawing)
        self.canvas.tag_bind("draw_ground", '<B1-Motion>', self.mouse_drag)
        self.canvas.tag_bind("draw_ground", '<ButtonRelease-1>', self.end_drawing)
        self.canvas.bind('<Button-1>', self.change_transport_unit)
        self.canvas.bind('<Button-2>', self.delete_edge)
        self.canvas.unbind('<Button-3>')
        self.line = None

    def change_transport_unit(self, e):
        for edge in self.edges:
            if edge.image.clicked(e.x, e.y):
                x, y = edge.image.image_coords
                t = edge.image.img_type + 1 if edge.image.img_type < 6 else 0
                self.delete_items(edge.image.image)
                edge.image.add_image_info(
                    self.canvas.create_image(x, y, image=self.transport_images[self.image_names[t]],
                                             tag="change_transport_unit"), (x, y), t)
                break

    def save(self):
        return save_data(self.edges, self.vertices)

    def start_drawing(self, e):
        if self.wrong_map_object is not None:
            self.canvas.delete(self.wrong_map_object)
            self.wrong_map_object = None

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

    def create_wrong_map_title(self):
        if self.wrong_map_object is None:
            self.wrong_map_object = self.canvas.create_image(680, 640, image=self.wrong_map_image,
                                                             tag="wrong_map_title")

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
        index = len(coords) // 3
        if index % 2 == 1:
            index -= 1
        x, y = coords[index], coords[index + 1]
        edge.image.add_image_info(self.canvas.create_image(x, y, image=self.transport_images['rocket_small'],
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

    @staticmethod
    def clicked_save(x, y):
        return 25 <= x <= 75 and 85 <= y <= 135

    def close(self):
        self.canvas.tag_unbind('draw_ground', '<Button-1>')
        self.canvas.tag_unbind('draw_ground', '<B1-Motion>')
        self.canvas.tag_unbind('draw_ground', '<ButtonRelease-1>')
        self.canvas.unbind('<Button-3>')
        self.canvas.unbind('<Button-2>')
        self.canvas.unbind('<Button-3>')

    def correct_map(self):
        return self.check_correct_map()
