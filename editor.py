import itertools
import random
import tkinter
from graph import Graph
from serialize import save_data


class TaskEditor(Graph):

    def __init__(self, canvas, planets_images, transport_images):
        super(TaskEditor, self).__init__(canvas, planets_images, transport_images)
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
                t = edge.image.img_type + 1 if edge.image.img_type < 1 else 0
                self.delete_items(edge.image.image)
                edge.image.add_image_info(self.canvas.create_image(x, y, image=self.transport_images['ufo_small' if t == 1 else 'rocket_small'], tag="change_transport_unit"), (x, y),
                                          t)
                break

    def save(self):
        save_data('data', self.edges, self.vertices)

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
                self.line = self.canvas.create_line(list(itertools.chain(*copy_points)), width=3, smooth=True, splinesteps=3,
                                                    arrow=tkinter.LAST)
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
        edge.image.add_image_info(self.canvas.create_image(x, y, image=self.transport_images['rocket_small'], tag="change_transport_unit"), (x, y), 0)

    def simplify_line(self, e):
        try:
            copy_points = [self.points[0]]
        except IndexError:
            return []
        for i in range(1, len(self.points)):
            # if (e.x > self.points[i][0] + self.offset_last_point or e.x < self.points[i][0] - self.offset_last_point) and \
            #         (e.y > self.points[i][1] + self.offset_last_point or e.y < self.points[i][1] - self.offset_last_point):
            #     continue
            if random.random() < 0.20:
                copy_points.append(self.points[i])
        copy_points.append((e.x, e.y))
        return copy_points

    @staticmethod
    def clicked_save(x, y):
        return 25 <= x <= 75 and 85 <= y <= 135

    def close(self):
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')
        self.canvas.unbind('<Button-3>')
        self.canvas.unbind('<Button-2>')
        self.canvas.unbind('<Button-3>')
