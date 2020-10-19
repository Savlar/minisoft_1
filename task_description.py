import tkinter


class TaskDescription:

    def __init__(self, canvas, task_info, planets_images, transport_images):
        self.canvas: tkinter.Canvas = canvas
        self.planets_images = planets_images
        self.transport_images = transport_images
        self.task_info = task_info
        self.task_type = self.task_info['type']
        self.path = self.task_info['path']
        self.transport = self.task_info['transport']
        self.clear()
        x = {1: self.write_task_with_path, 2: self.write_task_with_path, 3: self.write_task_3, 4: self.write_task_4}
        x[self.task_type]()

    def write_task_with_path(self):
        strings = ['Chces sa dostat z']
        if len(self.path) > 2:
            strings.append('cez')
        for i in range(len(self.path) - 3):
            strings.append('a')
        strings.append('do')
        order = 0
        for item in self.path:
            self.canvas.create_image(1765, 150 + order * 100, image=self.planets_images[item], tag='description')
            self.canvas.create_text(1765, 100 + order * 100, text=strings[order], tag='description')
            order += 1

    def write_task_3(self):
        strings = ['Zacali sme na planete', 'a isli sme']
        for i in range(len(self.transport) - 1):
            strings.append('a')
        strings.append('Kde sme skoncili?')
        order = 0
        self.canvas.create_text(1765, 100, text=strings[0], tag='description')
        self.canvas.create_image(1765, 150, image=self.planets_images[self.path[0]], tag='description')
        for item in self.transport:
            self.canvas.create_image(1765, 250 + order * 100, image=self.transport_images[item], tag='description')
            self.canvas.create_text(1765, 200 + order * 100, text=strings[order + 1], tag='description')
            order += 1
        self.canvas.create_text(1765, 100 + (1 + order) * 100, text=strings[-1], tag='description')

    def write_task_4(self):
        strings = ['Isli sme']
        for i in range(len(self.transport) - 1):
            strings.append('a')
        strings.append('a skoncili sme na')
        strings.append('Kde sme zacali?')
        order = 0
        for item in self.transport:
            self.canvas.create_text(1765, 100 + order * 100, text=strings[order], tag='description')
            self.canvas.create_image(1765, 150 + order * 100, image=self.transport_images[item], tag='description')
            order += 1
        self.canvas.create_text(1765, 100 + order * 100, text=strings[-2], tag='description')
        self.canvas.create_image(1765, 150 + order * 100, image=self.planets_images[self.path[0]], tag='description')
        order += 1
        self.canvas.create_text(1765, 100 + order * 100, text=strings[-1], tag='description')

    def clear(self):
        for item in self.canvas.find_withtag('description'):
            self.canvas.delete(item)
