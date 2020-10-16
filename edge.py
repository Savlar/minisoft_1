class TransportImage:

    def __init__(self):
        self.image_coords = tuple()
        self.image = None
        self.img_type = 0

    def clicked(self, x, y):
        if len(self.image_coords) == 0: return False
        return self.image_coords[0] - 20 <= x <= self.image_coords[0] + 20 and self.image_coords[1] - 20 <= y <= \
               self.image_coords[1] + 20

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
        self.weigh = []
        self.image = TransportImage()

    def connected_nodes(self, x1, y1, x2, y2, area):
        return self.start.x - area <= x1 <= self.start.x + area and self.start.y - area <= y1 <= self.start.y + area \
               and self.end.x - area <= x2 <= self.end.x + area and self.end.y - area <= y2 <= self.end.y + area

    def clicked_edge(self, x, y):
        if self.points is None or len(self.points) == 0:
            return False
        for i in range(0, len(self.points), 2):
            point_x, point_y = self.points[i], self.points[i + 1]
            if point_x - 20 <= x <= point_x + 20 and point_y - 20 <= y <= point_y + 20:
                return True
        return False

    def delete_edge(self):
        img, line = self.image.image, self.line
        self.image = TransportImage()
        self.line = None
        self.points = []
        return img, line
