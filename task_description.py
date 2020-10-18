import tkinter


class TaskDescription:

    def __init__(self, canvas, task_info, planets_images):
        self.canvas: tkinter.Canvas = canvas
        self.task_info = task_info
        self.planets_images = planets_images

        try:
            self.path = task_info['path']
        except KeyError:
            self.transport = task_info['transport']
        write_task = {1: self.write_task_1, 2: self.write_task_2, 3: self.write_task_3, 4: self.write_task_4}
        write_task[self.task_info['type']]()

    def write_task_1(self):
        self.canvas.create_text(1765, 100, text='Chces sa dostat z ')
        self.canvas.create_image(1765, 150, image=self.planets_images[self.task_info['path'][0].name])
        self.canvas.create_text(1765, 200, text='do')
        self.canvas.create_image(1765, 250, image=self.planets_images[self.task_info['path'][1].name])

    def write_task_2(self):
        pass

    def write_task_3(self):
        pass

    def write_task_4(self):
        pass
