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
        self.canvas.tag_bind("draw_ground", '<Button-3>', self.mark_vertex)

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

    def start_drawing(self, e):
        if self.clicked_save(e.x, e.y):
            self.saved = True
            markers = list(self.vertex_markers.keys())
            save_data('data', self.edges, self.vertices, {'type': 1, 'path': [markers[0], markers[1]]})
            return
        self.points = [e.x, e.y]

    def delete_edge(self, e):
        for edge in self.edges:
            if edge.clicked_edge(e.x, e.y):
                self.delete_items(*edge.delete_edge())
                return

    def mouse_drag(self, e):
        print(e)
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
            if edge is not None:
                self.line = self.canvas.create_line(*copy_points, width=3, smooth=True, splinesteps=3,
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
        edge.image.add_image_info(self.canvas.create_image(x, y, image=self.transport_images['rocket_small'], tag="change_transport_unit"), (x, y), 0, )

    def mark_vertex(self, e):
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
                    self.create_marker(vertex, order + 1, True)

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