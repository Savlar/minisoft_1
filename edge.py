class TransportImage:

    def __init__(self):
        self.image_coords = tuple()
        self.image = None
        self.img_type = 0

    def clicked(self, x, y):
        if len(self.image_coords) == 0:
            return False
        return self.image_coords[0] - 10 <= x <= self.image_coords[0] + 10 and self.image_coords[1] - 10 <= y <= \
               self.image_coords[1] + 10

    def add_image_info(self, img, coords, img_type):
        self.image_coords = coords
        self.image = img
        self.img_type = img_type


class Edge:

    def __init__(self, start, end, points=None, line=None):
        self.start = start
        self.end = end
        self.points = points
        self.line = line
        self.weight = []
        self.image = TransportImage()

    def get_transport_type(self):
        return self.image.img_type

    def connected_nodes(self, x1, y1, x2, y2, area):
        return self.start.x - area <= x1 <= self.start.x + area and self.start.y - area <= y1 <= self.start.y + area \
               and self.end.x - area <= x2 <= self.end.x + area and self.end.y - area <= y2 <= self.end.y + area

    def clicked_edge(self, x, y):
        if self.points is None or len(self.points) == 0:
            return False
        for i in range(len(self.points)):
            point_x, point_y = self.points[i][0], self.points[i][1]
            if point_x - 10 <= x <= point_x + 10 and point_y - 10 <= y <= point_y + 10:
                return True
        return False

    def delete_edge(self):
        img, line = self.image.image, self.line
        self.image = TransportImage()
        self.line = None
        self.points = []
        return img, line

    def is_edge(self):
        return self.line is not None

    def get_edge_stats(self):
        return self.start.name, self.end.name, self.get_transport_type()
