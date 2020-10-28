import random
import tkinter
from math import ceil
from tkinter import filedialog

from PIL import Image, ImageTk
from editor import GraphEditor
from graph import Graph
from serialize import load_data
from task_description import TaskDescription


class Program:
    def __init__(self):
        root = tkinter.Tk()
        self.base_width = 1024
        self.base_height = 576

        current_screen_width = root.winfo_screenwidth()
        current_screen_height = root.winfo_screenheight()

        self.width = current_screen_width if current_screen_width <= 1920 else 1920
        self.height = current_screen_height if current_screen_height <= 1080 else 1080
        self.canvas = tkinter.Canvas(master=root, width=self.width, height=self.height)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
        self.main = Main(self.canvas, self.width / self.base_width - 0.5, self.height / self.base_height - 0.5)
        self.canvas.bind('<Configure>', self.on_resize)
        root.mainloop()

    def on_resize(self, event):
        print("onresize")
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.canvas.scale('all', 0, 0, wscale, hscale)
        self.width = event.width
        self.height = event.height
        self.main.wscale = self.width / self.base_width - 0.5
        self.main.hscale = self.height / self.base_height - 0.5
        self.main.window_wscale = wscale
        self.main.window_hscale = hscale
        self.main.resize_images()


class Main:
    def __init__(self, canvas: tkinter.Canvas, wscale, hscale):
        self.canvas = canvas
        self.file_name = None
        self.window_wscale = 1
        self.window_hscale = 1
        self.wscale = wscale
        self.hscale = hscale
        self.max_transport_units = 8
        self.background = tkinter.PhotoImage(file="./textures/bg.png")
        self.msg = None
        self.game = None
        self.buttons_array_names = ["load", "reset", "close", "check", "save", "editor", "delete", "back"]
        # self.buttons_array_names = ["load", "reset", "close", "check", "save", "editor", "delete", "back", '1', '2', '3'
        #                             , '4', '5']
        self.bad_solution = "Nesprávne riešenie"
        self.good_solution = "Správne riešenie"

        self.buttons_basic_images = None
        self.buttons_filled_images = None
        self.planets_images = None
        self.transport_images = None
        self.title_images = None
        self.create_images()
        self.buttons_id = {}
        self.difficulty_id = {}
        self.random_type = random.randint(1, 4)

        self.buttons_bind = self.canvas.bind("<Motion>", self.filled_button)
        self.buttons_action_bind = self.canvas.tag_bind("button", "<Button-1>", self.buttons_action)

        self.random_type = self.random_length = self.random_path = self.graph_editor = self.graph = self.task = None
        self.start(True)

    def start(self, delete_all=False):
        self.canvas.delete('all')
        self.canvas.create_image(514, 288, image=self.background, tag="background")

        self.random_type = random.randint(1, 4)
        self.create_images()
        self.create_buttons()

        self.graph_editor = None

        self.graph = Graph(self.canvas, self.planets_images, self.transport_images, self.max_transport_units,
                           self.random_type > 2)

        x = load_data(self.file_name)
        self.graph.load(x)
        self.graph.generate_paths()
        while True:
            self.random_length = random.randint(2, 6)
            if len(self.graph.all_paths[self.random_length]) == 0:
                continue
            self.random_path = random.randint(0, len(self.graph.all_paths[self.random_length]) - 1)
            break
        if self.random_type in [1, 2]:
            self.game = Game(self.canvas, self.transport_images, self.max_transport_units)
        task_info = {'type': self.random_type, 'path': self.graph.all_paths[self.random_length][self.random_path][0],
                     'transport': self.graph.all_paths[self.random_length][self.random_path][1]}
        self.task = TaskDescription(self.canvas, task_info, self.planets_images, self.transport_images)
        self.msg = self.canvas.create_text(500, 500, text='', font=("Alfa Slab One", 18))
        self.resize_images(True)

    def create_images(self):
        self.buttons_basic_images = self.create_dictionary_for_images("textures/buttons/basic/",
                                                                      self.buttons_array_names)
        self.buttons_filled_images = self.create_dictionary_for_images("textures/buttons/filled/",
                                                                       self.buttons_array_names)
        self.planets_images = self.create_dictionary_for_images("textures/planets/",
                                                                ["earth", "jupiter", "mars", "mercury", "neptune",
                                                                 "saturn", "uranus", "venus", 'pluto', 'moon'])
        self.transport_images = self.create_dictionary_for_images("textures/transportunits/",
                                                                  ["rocket", "ufo", "rocket_small", "ufo_small",
                                                                   "rocket_ufo_tesla_small", 'tesla_small',
                                                                   'ufo_tesla_small',
                                                                   'rocket_tesla_small', 'tesla'])

        self.title_images = self.create_dictionary_for_images("textures/titles/",
                                                              ["path", "task", "task_type", "difficulty"])

    @staticmethod
    def create_dictionary_for_images(path, image_list):
        images = {}

        for item in image_list:
            pil_image = Image.open(f'{path}{item}.png')
            tk_image = ImageTk.PhotoImage(pil_image)
            images[item] = (pil_image, tk_image, pil_image)
        return images

    def resize_images(self, reset=False):
        if reset:
            wwscale = self.canvas.winfo_width() / 1024
            whscale = self.canvas.winfo_height() / 576
            self.canvas.scale('all', 0, 0, wwscale, whscale)
        self.resize(['draw_ground', 'img_description'], self.planets_images)
        self.resize(['button'], self.buttons_basic_images)
        self.resize([], self.buttons_filled_images)
        self.resize(['results_clickable', 'img_description', 'movable', 'graph'], self.transport_images)
        self.resize(['title'], self.title_images)

    def resize(self, tags, image_dict):
        image_id = {}
        for tag in tags:
            for object_id in self.canvas.find_withtag(tag):
                object_image_id = self.canvas.itemcget(object_id, option='image')
                image_id.setdefault(object_image_id, []).append(object_id)
        for key, value in image_dict.items():
            resized_image, tk_image, original_image = value
            width, height = original_image.size
            new_width = min(width, ceil(width * self.wscale))
            new_height = min(height, ceil(height * self.hscale))
            resized_image = original_image.resize((new_width, new_height))
            new_tk_image = ImageTk.PhotoImage(resized_image)
            try:
                for object in image_id[str(tk_image)]:
                    pass
                    self.canvas.itemconfig(object, image=new_tk_image)
            except KeyError:
                pass
            image_dict[key] = (resized_image, new_tk_image, original_image)

    def create_buttons(self):
        y = 27
        # for buttonName in ["load", "editor", "reset", "close", '1', '2', '3', '4', '5']:
        for buttonName in ["load", "editor", "reset", "close"]:
            self.buttons_id[buttonName] = self.canvas.create_image(90, y,
                                                                   image=self.buttons_basic_images[buttonName][1],
                                                                   tag="button")
            y += 35
        self.buttons_id["check"] = self.canvas.create_image(930, 453, image=self.buttons_basic_images["check"][1],
                                                            tag="button")

        self.buttons_id["delete"] = self.canvas.create_image(930, 500, image=self.buttons_basic_images["delete"][1],
                                                             tag="button")

        self.canvas.create_image(935, 27, image=self.title_images["task"][1], tag="title")
        if self.random_type < 3:
            self.canvas.create_image(250, 469, image=self.title_images["path"][1], tag="title")
        self.canvas.update()

    def remove_objects_with_tag(self, tag):
        for item in self.canvas.find_withtag(tag):
            self.canvas.delete(item)

    def create_editor_buttons(self):
        self.buttons_id["save"] = self.canvas.create_image(90, 266, image=self.buttons_basic_images["save"][1],
                                                           tag="button")
        self.buttons_id["back"] = self.canvas.create_image(90, 299, image=self.buttons_basic_images["back"][1],
                                                           tag="button")

    def filled_button(self, event):
        for buttonsName in self.buttons_id.keys():
            if self.canvas.coords(self.buttons_id[buttonsName]) == self.canvas.coords("current"):
                self.canvas.itemconfig("current", image=self.buttons_filled_images[buttonsName][1])
            else:
                self.canvas.itemconfig(self.buttons_id[buttonsName], image=self.buttons_basic_images[buttonsName][1])

    def browse_file(self):
        self.file_name = filedialog.askopenfilename(initialdir="./misc",
                                                    title="Select a File",
                                                    filetypes=(("Serialized python structure",
                                                                "*.pickle*"),
                                                               ))
        if self.file_name is not None and self.file_name != '' and not isinstance(self.file_name, tuple):
            self.reset()

    def delete_unused_editor_buttons(self):
        self.canvas.delete(self.buttons_id["check"])
        self.remove_objects_with_tag('title')
        if self.game:
            self.canvas.delete(self.game.place_for_results_transport_units)
            self.game.clean_transport_units_objects()

    def buttons_action(self, event):
        if self.canvas.coords("current") == self.canvas.coords(self.buttons_id["editor"]) and self.graph_editor is None:
            self.change_text('')
            self.graph.delete_all()
            self.task.clear()
            self.delete_unused_editor_buttons()
            self.graph_editor = GraphEditor(self.canvas, self.planets_images, self.transport_images,
                                            self.max_transport_units, self.graph)
            self.create_editor_buttons()

        if self.canvas.coords("current") == self.canvas.coords(self.buttons_id["load"]):
            if self.graph_editor is not None:
                self.graph_editor.close()
            self.browse_file()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["reset"]):
            if self.graph_editor is not None:
                self.graph_editor.close()
                self.graph_editor = None

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["close"]):
            quit()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["check"]):
            self.check_path()
        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["delete"]):
            if self.graph is not None:
                self.graph.remove_marker()
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
                if path[0][0] == source and path[0][-1] == destination and self.equal_paths(selected_transport,
                                                                                            path[1]):
                    self.change_text(self.good_solution)
                    return
            self.change_text(self.bad_solution)
        else:
            selected_transport = ['rocket' if x == 0 else 'ufo' if x == 1 else 'tesla'
                                  for x in self.get_results_transport_units()]
            for path in self.graph.all_paths[len(selected_transport)]:
                if self.graph.all_paths[self.random_length][self.random_path][0] == path[0] and \
                        self.equal_paths(selected_transport, path[1]):
                    self.change_text(self.good_solution)
                    return
            self.change_text(self.bad_solution)

    @staticmethod
    def equal_paths(user_path, generated_path):
        for i in range(len(user_path)):
            if user_path[i] not in generated_path[i]:
                return False
        return True

    def change_text(self, text):
        self.canvas.itemconfig(self.msg, text=text)

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


class Game:
    def __init__(self, canvas, transport_units, max_transport_units):
        self.canvas = canvas
        self.max_results_transport_units = max_transport_units
        self.transport_units = transport_units
        self.transport_units_objects = []
        self.results_transport_units = []
        self.place_for_results_transport_units = self.canvas.create_rectangle(213, 453, 823, 533, tag="units_place")
        self.results_rectangle_coords = self.canvas.coords(self.place_for_results_transport_units)
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

        if self.canvas.find_withtag("current")[0] == self.transport_units_objects[2]:
            # tesla
            kind = 2

        self.append_to_results_transport_unit(kind)

    def release_transport_unit(self, event):
        if len(self.results_transport_units) != self.max_results_transport_units:
            current_coords = [event.x, event.y]
            kind = 1

            if self.canvas.find_withtag("current")[0] == self.transport_units_objects[0]:
                kind = 0

            if self.canvas.find_withtag("current")[0] == self.transport_units_objects[2]:
                kind = 2

            if self.results_rectangle_coords == current_coords or self.results_rectangle_coords[0] + 592 >= \
                    current_coords[
                        0] and self.results_rectangle_coords[0] - 592 <= current_coords[
                0] and self.results_rectangle_coords[1] + 80 >= current_coords[1] >= self.results_rectangle_coords[
                1] - 80:
                self.append_to_results_transport_unit(kind)
        self.remake_transport_units_objects()

    def append_to_results_transport_unit(self, kind):
        self.results_transport_units.append(
            (kind, self.canvas.create_image(253 + len(self.results_transport_units) * 70, 495,
                                            image=(self.transport_units["rocket"][1] if kind == 0 else
                                                   self.transport_units["ufo"][1] if kind == 1 else
                                                   self.transport_units["tesla"][1]),
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
            self.canvas.create_image(586, 469, image=self.transport_units["rocket"][1], tag="movable"))
        self.transport_units_objects.append(
            self.canvas.create_image(639, 469, image=self.transport_units["ufo"][1], tag="movable"))
        self.transport_units_objects.append(
            self.canvas.create_image(693, 469, image=self.transport_units["tesla"][1], tag="movable"))

    def remake_transport_units_objects(self):
        self.clean_transport_units_objects()
        self.create_transport_units()

    def move_transport_unit(self, event):
        self.canvas.coords("current", event.x, event.y)
