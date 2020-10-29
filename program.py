import random
import tkinter
from tkinter import filedialog

from editor import GraphEditor
from graph import Graph
from serialize import load_data
from task_description import TaskDescription


class Program:
    def __init__(self):
        win = tkinter.Tk()
        self.canvas = tkinter.Canvas(master=win, height=720, width=1280, bg='grey')
        self.canvas.pack()
        Main(self.canvas)
        win.mainloop()


class Main:
    def __init__(self, canvas: tkinter.Canvas, file_name=None):
        self.canvas = canvas
        self.random_type = random.randint(1, 4)
        self.max_transport_units = 8
        self.background = tkinter.PhotoImage(file="./textures/bg.png")
        self.canvas.create_image(640, 360, image=self.background, tag="background")
        self.msg = self.canvas.create_text(640, 680, text='', font=("Alfa Slab One", 18))
        self.game = None
        self.buttons_array_names = ["load", "reset", "close", "check", "save", "editor", "delete", "back",'1', '2', '3'
                                    , '4', '5']
        self.bad_solution = "Nesprávne riešenie"
        self.good_solution = "Správne riešenie"
        self.selected_task_types = ['1', '2', '3', '4']
        self.solved_tasks = {'1': 0, '2': 0, '3': 0, '4': 0}
        self.buttons_basic_images = self.create_dictionary_for_images("textures/buttons/basic/",
                                                                      self.buttons_array_names)
        self.buttons_filled_images = self.create_dictionary_for_images("textures/buttons/filled/",
                                                                       self.buttons_array_names)
        self.planets_images = self.create_dictionary_for_images("textures/planets/",
                                                                ["earth", "jupiter", "mars", "mercury", "neptune",
                                                                 "saturn", "uranus", "venus"])
        self.transport_images = self.create_dictionary_for_images("textures/transportunits/",
                                                                  ["rocket", "ufo", "rocket_small", "ufo_small",
                                                                   "rocket_ufo_tesla_small", 'tesla_small', 'rocket_ufo_small',
                                                                   'ufo_tesla_small', 'rocket_tesla_small', 'tesla'])

        self.title_images = self.create_dictionary_for_images("textures/titles/",
                                                              ["path", "task", "task_type", "difficulty"])

        self.buttons_id = {}

        self.create_buttons()
        self.buttons_bind = self.canvas.bind("<Motion>", self.filled_button)
        self.buttons_action_bind = self.canvas.tag_bind("button", "<Button-1>", self.buttons_action)
        self.buttons_task_type_bind = self.canvas.tag_bind('task_types', '<Button-1>', self.task_buttons_action)
        self.graph_editor = None
        self.task = None
        self.random_length = self.random_path = self.random_type = None
        self.graph = Graph(self.canvas, self.planets_images, self.transport_images, self.max_transport_units)

        self.file_name = file_name
        x = load_data(self.file_name)
        self.graph.load(x)
        self.graph.generate_paths()
        self.generate_task()

    def generate_task(self):
        self.graph.remove_all_markers()
        if self.game is not None:
            self.canvas.delete('movable')
            self.game.remove_selected_objects()
            self.game = None
        self.graph.free = False
        self.random_type = int(random.choice(self.selected_task_types))
        self.create_titles()
        type_solutions = self.solved_tasks[str(self.random_type)]
        if type_solutions == 0:
            self.random_length = random.randint(1, 3)
        elif type_solutions == 1:
            self.random_length = random.randint(4, 5)
        elif type_solutions == 2:
            self.random_length = random.randint(6, 7)
        else:
            self.random_length = random.randint(8, 10)
        while True:
            if len(self.graph.all_paths[self.random_length]) == 0:
                self.random_length -= 1
                continue
            self.random_path = random.randint(0, len(self.graph.all_paths[self.random_length]) - 1)
            break
        if self.random_type in [1, 2]:
            self.graph.disallow_marking()
            self.game = Game(self.canvas, self.transport_images, self.max_transport_units)
        else:
            self.graph.allow_marking()
        task_info = {'type': self.random_type, 'path': self.graph.all_paths[self.random_length][self.random_path][0],
                     'transport': self.graph.all_paths[self.random_length][self.random_path][1]}
        self.task = TaskDescription(self.canvas, task_info, self.planets_images, self.transport_images)

    def free_task(self):
        self.game = Game(self.canvas, self.transport_images, self.max_transport_units)
        self.canvas.delete('description')
        self.canvas.delete('title')
        self.graph.allow_marking()
        self.graph.free = True

    def create_titles(self):
        self.canvas.delete('title')
        self.canvas.create_image(1180, 50, image=self.title_images["task"], tag="title")
        if self.random_type < 3:
            self.canvas.create_image(640, 600, image=self.title_images["path"], tag="title")

    @staticmethod
    def create_dictionary_for_images(path, image_list):
        images = {}

        for item in image_list:
            images[item] = tkinter.PhotoImage(file=f"{path}{item}.png")
        return images

    def create_buttons(self):
        y = 50
        for buttonName in ["load", "editor", "reset", "close"]:
            self.buttons_id[buttonName] = self.canvas.create_image(110, y,
                                                                   image=self.buttons_basic_images[buttonName],
                                                                   tag="button")
            y += 40
        self.buttons_id["check"] = self.canvas.create_image(1170, 540, image=self.buttons_basic_images["check"],
                                                            tag="button")

        self.buttons_id["delete"] = self.canvas.create_image(1170, 580, image=self.buttons_basic_images["delete"],
                                                             tag="button")
        self.canvas.create_image(110, 350, image=self.title_images["task_type"], tag="task_types")
        for num,task_type_number in enumerate(["1","2","3","4","5"]):
            image = self.buttons_filled_images[task_type_number] \
                if task_type_number in self.selected_task_types else self.buttons_basic_images[task_type_number]
            self.buttons_id[task_type_number] = self.canvas.create_image(110, 380 + num*35, image=image,
                                                                         tag="task_types")

        self.canvas.update()

    def remove_objects_with_tag(self, tag):
        for item in self.canvas.find_withtag(tag):
            self.canvas.delete(item)

    def create_editor_buttons(self):
        self.buttons_id["save"] = self.canvas.create_image(110, 240, image=self.buttons_basic_images["save"],
                                                           tag="button")
        self.buttons_id["back"] = self.canvas.create_image(110, 280, image=self.buttons_basic_images["back"],
                                                           tag="button")

    def filled_button(self, event):
        for buttonsName in self.buttons_id.keys():
            if buttonsName in ['1', '2', '3', '4', '5']: return
            if self.buttons_id[buttonsName] is not None and self.canvas.coords(self.buttons_id[buttonsName]) == self.canvas.coords("current"):
                self.canvas.itemconfig("current", image=self.buttons_filled_images[buttonsName])
            else:
                self.canvas.itemconfig(self.buttons_id[buttonsName], image=self.buttons_basic_images[buttonsName])

    def browse_file(self):
        self.file_name = filedialog.askopenfilename(initialdir="./misc",
                                                    title="Select a File",
                                                    filetypes=(("Serialized python structure",
                                                                "*.pickle*"),
                                                               ))
        if self.file_name is not None and self.file_name != '' and not isinstance(self.file_name, tuple):
            if self.graph_editor is not None:
                self.graph_editor.load(load_data(self.file_name))
            else:
                self.reset()

    def delete_unused_editor_buttons(self):
        self.canvas.delete(self.buttons_id["check"])
        if self.buttons_id["delete"] is not None:
            self.canvas.delete(self.buttons_id["delete"])

        self.remove_objects_with_tag('title')
        self.remove_objects_with_tag('task_types')
        if self.game:
            self.game.clean_transport_units_objects()

    def task_buttons_action(self, e):
        if self.canvas.coords("current") == self.canvas.coords(self.buttons_id['5']):
            self.canvas.itemconfig(self.buttons_id['5'], image=self.buttons_filled_images['5'])
            self.deselect_task('1', '2', '3', '4')
            self.selected_task_types = ['5']
            self.free_task()
            return
        for task_id in ['1', '2', '3', '4']:
            if self.canvas.coords("current") == self.canvas.coords(self.buttons_id[task_id]):
                image = self.canvas.itemcget(self.buttons_id[task_id], option='image')
                if image == str(self.buttons_basic_images[task_id]):
                    self.selected_task_types.append(task_id)
                    new_image = self.buttons_filled_images[task_id]
                else:
                    if len(self.selected_task_types) == 1:
                        return
                    self.selected_task_types.remove(task_id)
                    if int(task_id) == self.random_type:
                        self.generate_task()
                    new_image = self.buttons_basic_images[task_id]
                self.canvas.itemconfig(self.buttons_id[task_id], image=new_image)
                if '5' in self.selected_task_types:
                    self.deselect_task('5')
                    self.generate_task()

    def deselect_task(self, *args):
        for task in args:
            if task in self.selected_task_types:
                self.selected_task_types.remove(task)
                self.canvas.itemconfig(self.buttons_id[task], image=self.buttons_basic_images[task])

    def buttons_action(self, event):
        if self.canvas.coords("current") == self.canvas.coords(self.buttons_id["editor"]):
            if self.graph_editor is not None:
                return
            self.change_text('')
            self.graph.delete_all()
            self.task.clear()
            self.delete_unused_editor_buttons()
            self.graph_editor = GraphEditor(self.canvas, self.planets_images, self.transport_images,
                                            self.max_transport_units)
            self.create_editor_buttons()

        if self.canvas.coords("current") == self.canvas.coords(self.buttons_id["load"]):
            self.browse_file()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["reset"]):
            if self.graph_editor is not None:
                self.graph_editor.close()
                self.graph_editor = None
            self.reset()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["close"]):
            quit()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["check"]):
            self.check_path()
        elif self.buttons_id["delete"] is not None and self.canvas.coords("current") == self.canvas.coords(self.buttons_id["delete"]):
            self.graph.remove_all_markers()
            if self.game is not None:
                self.game.remove_selected_objects()

        elif self.buttons_id["save"] is not None and self.canvas.coords("current") == self.canvas.coords(
                self.buttons_id["save"]):
            if self.graph_editor.correct_map():
                self.save_map()
            else:
                print('Wrong map')

        elif self.buttons_id["back"] is not None and self.canvas.coords("current") == self.canvas.coords(
                self.buttons_id["back"]):
            if self.graph_editor is not None:
                self.graph_editor.close()
            self.graph_editor = None
            self.reset()

    @staticmethod
    def equal_paths(user_path, generated_path):
        for i in range(len(user_path)):
            if user_path[i] not in generated_path[i]:
                return False
        return True

    def check_path(self):
        if self.random_type in [3, 4]:
            selected = list(self.graph.vertex_markers.keys())
            try:
                selected = selected[0].name
            except IndexError:
                self.change_text('Nebola vybraná planéta')
                return
            if self.random_type == 3:
                for path in self.graph.all_paths[self.random_length]:
                    if path[1] == self.graph.all_paths[self.random_length][self.random_path][1] and path[0][
                        -1] == selected \
                            and path[0][0] == self.graph.all_paths[self.random_length][self.random_path][0][0]:
                        self.change_text(self.good_solution)
                        return
                self.change_text(self.bad_solution)
            if self.random_type == 4:
                for path in self.graph.all_paths[self.random_length]:
                    if path[1] == self.graph.all_paths[self.random_length][self.random_path][1] and path[0][
                        0] == selected \
                            and path[0][-1] == self.graph.all_paths[self.random_length][self.random_path][0][-1]:
                        self.change_text(self.good_solution)
                        return
                self.change_text(self.bad_solution)
        elif self.random_type == 1:
            selected_transport = ['rocket' if x == 0 else 'ufo' if x == 1 else 'tesla'
                                  for x in self.get_results_transport_units()]
            source = self.graph.all_paths[self.random_length][self.random_path][0][0]
            destination = self.graph.all_paths[self.random_length][self.random_path][0][-1]
            for path in self.graph.all_paths[len(selected_transport)]:
                if path[0][0] == source and path[0][-1] == destination and path[1] == selected_transport:
                    self.change_text(self.good_solution)
                    return
            self.change_text(self.bad_solution)
        else:
            selected_transport = ['rocket' if x == 0 else 'ufo' for x in self.get_results_transport_units()]
            for path in self.graph.all_paths[len(selected_transport)]:
                if self.graph.all_paths[self.random_length][self.random_path][0] == path[0] and \
                        self.equal_paths(selected_transport, path[1]):
                    self.change_text(self.good_solution)
                    return
            self.change_text(self.bad_solution)

    def change_text(self, text):
        if text == self.good_solution:
            self.correct_answer()
        self.canvas.itemconfig(self.msg, text=text)

    def correct_answer(self):
        self.solved_tasks[str(self.random_type)] += 1
        self.generate_task()

    def get_results_transport_units(self):
        list_transport_units = []
        for transport_unit in self.game.results_transport_units:
            list_transport_units.append(transport_unit[0])

        return list_transport_units

    def save_map(self):
        self.graph_editor.save()

    def clean_main_menu(self):
        self.canvas.delete("all")
        self.canvas.unbind("<Motion>", self.buttons_bind)
        self.canvas.unbind("<Button-1>", self.buttons_action_bind)
        self.canvas.unbind('<Button-1>', self.buttons_task_type_bind)

    def reset(self):
        self.clean_main_menu()
        self.canvas.delete("all")
        Main(self.canvas, self.file_name)


class Game:
    def __init__(self, canvas, transport_units, max_transport_units):
        self.canvas = canvas
        self.max_results_transport_units = max_transport_units
        self.transport_units = transport_units
        self.transport_units_objects = []
        self.results_transport_units = []
        self.results_rectangle_coords = (250, 580, 1050, 680)
        self.movable_units = self.canvas.tag_bind("movable", "<B3-Motion>", self.move_transport_unit)
        self.release_units = self.canvas.tag_bind("movable", "<ButtonRelease-3>", self.release_transport_unit)
        self.click_units = self.canvas.tag_bind("movable", "<Button-1>", self.add_transport_unit_on_click)
        self.click_units = self.canvas.tag_bind("results_clickable", "<Button-1>", self.remove_transport_unit_on_click)
        self.click_units = self.canvas.tag_bind("results_clickable", "<Button-3>", self.change_transport_unit_on_click)
        self.create_transport_units()
        self.canvas.update()

    def change_transport_unit_on_click(self, event):
        current = self.canvas.find_withtag("current")[0]
        for transport_unit in self.results_transport_units:
            if current == transport_unit[1]:
                kind = 1

                if transport_unit[0] == 1:
                    kind = 2
                if transport_unit[0] == 2:
                    kind = 0

                self.canvas.delete(transport_unit[1])
                index = self.results_transport_units.index(transport_unit)
                self.results_transport_units[index] = (kind, None)

        self.remake_results_transport_units_objects()

    def remove_transport_unit_on_click(self, event):
        current = self.canvas.find_withtag("current")[0]
        for transport_unit in self.results_transport_units:
            if current == transport_unit[1]:
                self.canvas.delete(transport_unit[1])
                self.results_transport_units.remove(transport_unit)

        self.remake_results_transport_units_objects()

    def remake_results_transport_units_objects(self):
        old_transport_units = self.results_transport_units
        self.results_transport_units = []
        for old_transport_unit in old_transport_units:
            self.append_to_results_transport_unit(old_transport_unit[0])
            self.canvas.delete(old_transport_unit[1])

    def add_transport_unit_on_click(self, event):
        if len(self.results_transport_units) == self.max_results_transport_units:
            return

        # ufo
        kind = 1

        if self.canvas.find_withtag("current")[0] == self.transport_units_objects[0]:
            # rocket
            kind = 0

        self.append_to_results_transport_unit(kind)

    def release_transport_unit(self, event):
        if len(self.results_transport_units) != self.max_results_transport_units:
            current_coords = [event.x, event.y]
            kind = 1

            if self.canvas.find_withtag("current")[0] == self.transport_units_objects[0]:
                kind = 0

            if self.canvas.find_withtag("current")[0] == self.transport_units_objects[2]:
                # tesla
                kind = 2

            if self.results_rectangle_coords == current_coords or self.results_rectangle_coords[0] + 800 >= \
                    current_coords[
                        0] and self.results_rectangle_coords[0] - 5 <= current_coords[
                0] and self.results_rectangle_coords[1] + 100 >= current_coords[1] >= self.results_rectangle_coords[
                1] - 30:
                self.append_to_results_transport_unit(kind)
        self.remake_transport_units_objects()

    def append_to_results_transport_unit(self, kind):
        self.results_transport_units.append(
            (kind, self.canvas.create_image(380 + len(self.results_transport_units) * 75, 640,
                                            image=(self.transport_units[
                                                       "rocket"] if kind == 0 else self.transport_units[
                                                "ufo"] if kind == 1 else
                                            self.transport_units["tesla"]),
                                            tag="results_clickable")))

    def remove_selected_objects(self):
        self.results_transport_units = []
        for item in self.canvas.find_withtag('results_clickable'):
            self.canvas.delete(item)

    def clean_transport_units_objects(self):
        for objc in self.transport_units_objects:
            self.canvas.delete(objc)
        self.transport_units_objects = []

    def create_transport_units(self):
        self.transport_units_objects.append(
            self.canvas.create_image(1165, 620, image=self.transport_units["rocket"], tag="movable"))
        self.transport_units_objects.append(
            self.canvas.create_image(1170, 655, image=self.transport_units["ufo"], tag="movable"))
        self.transport_units_objects.append(
            self.canvas.create_image(1170, 690, image=self.transport_units["tesla"], tag="movable"))

    def remake_transport_units_objects(self):
        self.clean_transport_units_objects()
        self.create_transport_units()

    def move_transport_unit(self, event):
        self.canvas.coords("current", event.x, event.y)
