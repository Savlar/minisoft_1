import tkinter


class TaskDescription:

    def __init__(self, canvas, task_info):
        self.canvas: tkinter.Canvas = canvas
        self.task_info = task_info
        task_type = task_info['type']
        write_task = {1: self.write_task_1, 2: self.write_task_2, 3: self.write_task_3, 4: self.write_task_4}
        write_task[task_type]()

    def write_task_1(self):
        path = self.task_info['path']
        self.canvas.create_text(1725, 100, text='Chces sa dostat z ')
        self.canvas.create_image(1725, 150, image=self.canvas.images[path[0].name])
        self.canvas.create_text(1725, 200, text='do')
        self.canvas.create_image(1725, 250, image=self.canvas.images[path[1].name])

    def write_task_2(self):
        pass

    def write_task_3(self):
        pass

    def write_task_4(self):
        pass
