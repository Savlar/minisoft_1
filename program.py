import random
import tkinter

from editor import TaskEditor
from graph import Graph
from serialize import load_data
from task_description import TaskDescription


class Program:
    def __init__(self):
        win = tkinter.Tk()
        self.canvas = tkinter.Canvas(master=win, height=1080, width=1920, bg='grey')
        self.canvas.pack()
        Main(self.canvas)
        win.mainloop()


class Main:
    def __init__(self, canvas):
        self.canvas = canvas
        self.buttons_array_names = ["settings", "load", "reset", "close", "check", "save", "editor", "path", "task", "delete"]

        self.buttons_basic_images = self.create_dictionary_for_images("textures/buttons/basic/",
                                                                      self.buttons_array_names)
        self.buttons_filled_images = self.create_dictionary_for_images("textures/buttons/filled/",
                                                                       self.buttons_array_names)
        self.planets_images = self.create_dictionary_for_images("textures/planets/",
                                                                ["earth", "jupiter", "mars", "mercury", "neptune",
                                                                 "saturn", "uranus", "venus"])
        self.transport_images = self.create_dictionary_for_images("textures/transportunits/",
                                                                  ["rocket", "ufo", "rocket_small", "ufo_small"])

        self.buttons_id = {}

        self.create_buttons()
        self.buttons_bind = self.canvas.bind("<Motion>", self.filled_button)
        self.buttons_action_bind = self.canvas.tag_bind("button", "<Button-1>", self.buttons_action)

        self.create_rectangles()

        self.te = None
        self.random_type = random.randint(1, 4)

        self.g = Graph(self.canvas, self.planets_images, self.transport_images, self.random_type > 2)
        x = load_data()
        self.g.load(x)
        self.g.generate_paths()
        while True:
            self.random_length = random.randint(2, 6)
            if len(self.g.all_paths[self.random_length]) == 0:
                continue
            self.random_path = random.randint(0, len(self.g.all_paths[self.random_length]) - 1)
            break
        if self.random_type in [1, 2]:
            self.game = Game(self.canvas, self.transport_images)
        task_info = {'type': self.random_type, 'path': self.g.all_paths[self.random_length][self.random_path][0],
                     'transport': self.g.all_paths[self.random_length][self.random_path][1]}
        self.task = TaskDescription(self.canvas, task_info, self.planets_images, self.transport_images)

    def create_dictionary_for_images(self, path, image_list):
        images = {}

        for item in image_list:
            images[item] = tkinter.PhotoImage(file=f"{path}{item}.png")
        return images

    def create_rectangles(self):
        self.canvas.create_rectangle(10, 80, 1650, 850)
        self.canvas.create_rectangle(1660, 80, 1870, 1050)

    def create_buttons(self):
        x = 120
        for buttonName in self.buttons_basic_images.keys():
            if buttonName != "check" and buttonName != "save":
                self.buttons_id[buttonName] = self.canvas.create_image(x, 30,
                                                                       image=self.buttons_basic_images[buttonName],
                                                                       tag="button")
                x += 250
        self.buttons_id["check"] = self.canvas.create_image(1500, 960, image=self.buttons_basic_images["check"],
                                                            tag="button")
        self.canvas.update()

    def create_save_button(self):
        self.buttons_id["save"] = self.canvas.create_image(1250, 30, image=self.buttons_basic_images["save"],
                                                           tag="button")

    def filled_button(self, event):
        for buttonsName in self.buttons_id.keys():
            if self.canvas.coords(self.buttons_id[buttonsName]) == self.canvas.coords("current"):
                self.canvas.itemconfig("current", image=self.buttons_filled_images[buttonsName])
            else:
                self.canvas.itemconfig(self.buttons_id[buttonsName], image=self.buttons_basic_images[buttonsName])

    def buttons_action(self, event):
        if self.canvas.coords("current") == self.canvas.coords(self.buttons_id["load"]):
            if self.te is not None:
                self.te.close()
            self.g.delete_all()
            self.task.clear()
            self.te = TaskEditor(self.canvas, self.planets_images, self.transport_images)
            self.create_save_button()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["settings"]):
            if self.te is not None:
                self.te.close()
            Settings(self.canvas)

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["reset"]):
            if self.te is not None:
                self.te.close()
                self.te = None
            self.reset()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["close"]):
            quit()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["check"]):
            self.check_path()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["save"]):
            if self.te.correct_map():
                self.save_map()
            else:
                print('Wrong map')

    def check_path(self):
        if self.random_type in [3, 4]:
            selected = list(self.g.vertex_markers.keys())[0]
            if self.random_type == 3:
                for path in self.g.all_paths[self.random_length]:
                    if path[0][-1] == selected.name and path[1] == self.g.all_paths[self.random_length][self.random_path][1]:
                        print('Correct solution')
                        return
                print('Incorrect solution')
            if self.random_type == 4:
                for path in self.g.all_paths[self.random_length]:
                    if path[0][0] == selected.name and path[1] == self.g.all_paths[self.random_length][self.random_path][1]:
                        print('Correct solution')
                        return
                print('Incorrect solution')
        elif self.random_type == 1:
            selected_transport = ['rocket' if x == 0 else 'ufo' for x in self.get_results_transport_units()]
            source = self.g.all_paths[self.random_length][self.random_path][0][0]
            destination = self.g.all_paths[self.random_length][self.random_path][0][-1]
            for path in self.g.all_paths[len(selected_transport)]:
                if path[0][0] == source and path[0][-1] == destination:
                    print('Correct solution')
                    return
            print('Incorrect solution')
        else:
            selected_transport = ['rocket' if x == 0 else 'ufo' for x in self.get_results_transport_units()]
            for path in self.g.all_paths[len(selected_transport)]:
                if path[1] == selected_transport and self.g.all_paths[self.random_length][self.random_path][0] == path[0]:
                    print('Correct solution')
                    return
            print('Incorrect solution')

    def get_results_transport_units(self):
        list_transport_units = []
        for transport_unit in self.game.results_transport_units:
            list_transport_units.append(transport_unit[0])

        return list_transport_units

    def save_map(self):
        self.te.save()

    def clean_main_menu(self):
        self.canvas.delete("all")
        self.canvas.unbind("<Motion>", self.buttons_bind)
        self.canvas.unbind("<Button-1>", self.buttons_action_bind)

    def reset(self):
        # self.game.remove_selected_objects()
        self.clean_main_menu()
        self.canvas.unbind_all("<Escape>")
        self.canvas.delete("all")
        Main(self.canvas)


class Game:
    def __init__(self, canvas, transport_units):
        self.canvas = canvas
        self.max_results_transport_units = 10
        self.transport_units = transport_units
        self.transport_units_objects = []
        self.results_transport_units = []
        self.place_for_results_transport_units = self.canvas.create_rectangle(10, 870, 1120, 1060, tag="units_place")
        self.results_rectangle_coords = self.canvas.coords(self.place_for_results_transport_units)
        self.movable_units = self.canvas.tag_bind("movable", "<B3-Motion>", self.move_transport_unit)
        self.release_units = self.canvas.tag_bind("movable", "<ButtonRelease-3>", self.release_transport_unit)
        self.click_units = self.canvas.tag_bind("movable", "<Button-1>", self.add_transport_unit_on_click)
        self.click_units = self.canvas.tag_bind("results_clickable", "<Button-1>", self.remove_transport_unit_on_click)
        self.create_transport_units()
        self.canvas.update()

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

    def append_to_results_transport_unit(self, kind):
        self.results_transport_units.append(
            (kind, self.canvas.create_image(80 + len(self.results_transport_units) * 100, 960,
                                            image=(self.transport_units[
                                                       "rocket"] if kind == 0 else
                                                   self.transport_units["ufo"]),
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
            self.canvas.create_image(1240, 930, image=self.transport_units["rocket"], tag="movable"))
        self.transport_units_objects.append(
            self.canvas.create_image(1250, 1000, image=self.transport_units["ufo"], tag="movable"))

    def remake_transport_units_objects(self):
        self.clean_transport_units_objects()
        self.create_transport_units()

    def move_transport_unit(self, event):
        self.canvas.coords("current", event.x, event.y)

    def release_transport_unit(self, event):
        if len(self.results_transport_units) != self.max_results_transport_units:
            current_coords = [event.x, event.y]
            kind = 1

            if self.canvas.find_withtag("current")[0] == self.transport_units_objects[0]:
                kind = 0

            if self.results_rectangle_coords == current_coords or self.results_rectangle_coords[0] + 1110 >= \
                    current_coords[
                        0] and self.results_rectangle_coords[0] - 1110 <= current_coords[
                0] and self.results_rectangle_coords[1] + 150 >= current_coords[1] >= self.results_rectangle_coords[
                1] - 150:
                self.results_transport_units.append((kind,
                                                     self.canvas.create_image(
                                                         80 + len(self.results_transport_units) * 100, 960, image=(
                                                             self.transport_units["rocket"] if kind == 0 else
                                                             self.transport_units["ufo"]),
                                                         tag="results_clickable")))
        self.remake_transport_units_objects()


class Settings:
    def __init__(self, canvas):
        self.canvas = canvas

    def return_to_menu(self, event):
        self.canvas.unbind_all("<Escape>")
        self.canvas.delete("all")
        Main(self.canvas)
