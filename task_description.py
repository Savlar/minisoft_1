import random
import tkinter


class TaskDescription:
    def __init__(self, canvas, task_info, planets_images, transport_images, text_images):
        self.canvas: tkinter.Canvas = canvas
        self.text_images = text_images
        self.x = 1180
        self.planets_images = planets_images
        self.transport_images = transport_images
        self.task_info = task_info
        self.task_type = self.task_info['type']
        self.path = self.task_info['path'][:]
        if self.task_type == 1:
            self.path = [self.path[0], self.path[-1]]
        self.transport = self.task_info['transport']
        self.clear()
        x = {1: self.write_task_with_path, 2: self.write_task_with_path, 3: self.write_task_3, 4: self.write_task_4}
        x[self.task_type]()

    def write_task_with_path(self):
        strings = [self.text_images["want_caps"]]
        if len(self.path) > 2:
            strings.append(self.text_images["through_low"])
        for i in range(len(self.path) - 3):
            strings.append(self.text_images["and_low"])
        strings.append(self.text_images["to_low"])
        order = 0
        for item in self.path:
            self.canvas.create_image(self.x, 100 + order * 70, image=self.planets_images[item], tag='description')
            self.canvas.create_image(self.x, 70 + order * 70, image=strings[order], tag="description")
            order += 1

    def write_task_3(self):
        strings = [self.text_images["start_on_low"], self.text_images["go_caps"]]
        for i in range(len(self.transport) - 1):
            strings.append(self.text_images["and_low"])
        strings.append(self.text_images["where_end_caps"])
        order = 0
        self.canvas.create_image(self.x, 70, image=strings[0], tag="description")
        self.canvas.create_image(self.x, 100, image=self.planets_images[self.path[0]], tag='description')
        for item in self.transport:
            transport_unit = random.choice(list(filter(None, item.split('_'))))
            self.canvas.create_image(self.x, 154 + order * 65, image=self.transport_images[transport_unit],
                                     tag='description')
            self.canvas.create_image(self.x, 130 + order * 65, image=strings[order + 1], tag="description")
            order += 1
        self.canvas.create_image(self.x, 50 + (1 + order) * 65, image=strings[-1], tag="description")

    def write_task_4(self):
        strings = [self.text_images["go_caps"]]
        for i in range(len(self.transport) - 1):
            strings.append(self.text_images["and_low"])
        strings.append(self.text_images["end_low"])
        strings.append(self.text_images["where_caps"])
        order = 0
        for item in self.transport:
            transport_unit = random.choice(list(filter(None, item.split('_'))))
            self.canvas.create_image(self.x, 70 + order * 65, image=strings[order], tag="description")
            self.canvas.create_image(self.x, 100 + order * 65, image=self.transport_images[transport_unit],
                                     tag='description')
            order += 1
        self.canvas.create_image(self.x, 70 + order * 65, image=strings[-2], tag="description")
        self.canvas.create_image(self.x, 100 + order * 65, image=self.planets_images[self.path[-1]], tag='description')
        order += 1
        self.canvas.create_image(self.x, 70 + order * 65, image=strings[-1], tag="description")

    def clear(self):
        for item in self.canvas.find_withtag('description'):
            self.canvas.delete(item)
