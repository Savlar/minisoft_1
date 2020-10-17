import tkinter
from graph import Graph
from serialize import save_data


class TaskEditor(Graph):

    def __init__(self, canvas: tkinter.Canvas):
        super(TaskEditor, self).__init__(canvas)
        self.saved = False
        self.canvas.create_image(50, 110, image=self.canvas.images['diskette'])
        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.end_drawing)
        self.canvas.bind('<Button-3>', self.cancel_drawing)
        self.canvas.bind('<Button-2>', self.delete_edge)
        self.canvas.bind('<Button-3>', self.mark_vertex)

    def start_drawing(self, e):
        if self.clicked_save(e.x, e.y):
            self.saved = True
            markers = list(self.vertex_markers.keys())
            save_data('data', self.edges, self.vertices, {'type': 1, 'path': [markers[0], markers[1]]})
            return
        for edge in self.edges:
            if edge.image.clicked(e.x, e.y):
                x, y = edge.image.image_coords
                t = edge.image.img_type + 1 if edge.image.img_type < 1 else 0
                self.delete_items(edge.image.image)
                edge.image.add_image_info(self.canvas.create_image(x, y, image=self.canvas.transport_types[t]), (x, y), t)
                break
        self.points = [e.x, e.y]

    def cancel_drawing(self, e):
        self.points = []
        self.canvas.delete(self.line)
        self.line = None

    def delete_edge(self, e):
        for edge in self.edges:
            if edge.clicked_edge(e.x, e.y):
                self.delete_items(*edge.delete_edge())
                return

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
        edge.image.add_image_info(self.canvas.create_image(x, y, image=self.canvas.transport_types[0]), (x, y), 0)

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