import random
import tkinter


class TaskDescription:

    def __init__(self, canvas, task_info, planets_images, transport_images):
        self.canvas: tkinter.Canvas = canvas
        self.x = 933
        self.planets_images = planets_images
        self.transport_images = transport_images
        self.task_info = task_info
        self.task_type = self.task_info['type']
        self.from_image = tkinter.PhotoImage(file="./textures/texts/from.png")
        self.path = self.task_info['path'][:]
        if self.task_type == 1:
            self.path = [self.path[0], self.path[-1]]
        self.transport = self.task_info['transport']
        self.clear()
        x = {1: self.write_task_with_path, 2: self.write_task_with_path, 3: self.write_task_3, 4: self.write_task_4}
        x[self.task_type]()

    def write_task_with_path(self):
        strings = ['Chceš sa dostať z']
        if len(self.path) > 2:
            strings.append('cez')
        for i in range(len(self.path) - 3):
            strings.append('a')
        strings.append('do')
        order = 0
        for item in self.path:
            self.canvas.create_image(self.x, 75 + order * 45, image=self.planets_images[item][1], tag='img_description')
            self.canvas.create_text(self.x, 50 + order * 45, text=strings[order], font=("Alfa Slab One",12), tag='description')
            order += 1

    def write_task_3(self):
        strings = ['Začali sme na planéte', 'a išli sme']
        for i in range(len(self.transport) - 1):
            strings.append('a')
        strings.append('Kde sme skončili?')
        order = 0
        self.canvas.create_text(self.x, 55, text=strings[0], font=("Alfa Slab One",12), tag='description')
        self.canvas.create_image(self.x, 75, image=self.planets_images[self.path[0]][1], tag='img_description')
        for item in self.transport:
            transport_unit = random.choice(list(filter(None, item.split('_'))))
            self.canvas.create_image(self.x, 130 + order * 45, image=self.transport_images[transport_unit][1], tag='img_description')
            self.canvas.create_text(self.x, 100 + order * 45, text=strings[order + 1], font=("Alfa Slab One",12), tag='description')
            order += 1
        self.canvas.create_text(self.x, 55 + (1 + order) * 45, text=strings[-1], font=("Alfa Slab One",12), tag='description')

    def write_task_4(self):
        strings = ['Išli sme']
        for i in range(len(self.transport) - 1):
            strings.append('a')
        strings.append('a skončili sme na')
        strings.append('Kde sme začali?')
        order = 0
        for item in self.transport:
            transport_unit = random.choice(list(filter(None, item.split('_'))))
            self.canvas.create_text(self.x, 55 + order * 45, text=strings[order], font=("Alfa Slab One",12), tag='description')
            self.canvas.create_image(self.x, 75 + order * 45, image=self.transport_images[transport_unit][1], tag='img_description')
            order += 1
        self.canvas.create_text(self.x, 55 + order * 45, text=strings[-2], font=("Alfa Slab One",12), tag='description')
        self.canvas.create_image(self.x, 75 + order * 45, image=self.planets_images[self.path[-1]][1], tag='img_description')
        order += 1
        self.canvas.create_text(self.x, 55 + order * 45, text=strings[-1], font=("Alfa Slab One",12), tag='description')

    def clear(self):
        for item in self.canvas.find_withtag('description'):
            self.canvas.delete(item)
        for item in self.canvas.find_withtag('img_description'):
            self.canvas.delete(item)