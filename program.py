import random
import tkinter
from tkinter import filedialog

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
    def __init__(self, canvas, file_name=None):
        self.canvas = canvas
        self.random_type = random.randint(1, 4)
        self.msg = self.canvas.create_text(1730, 800, text='', font=('Arial', 18))
        self.game = None
        self.buttons_array_names = ["settings", "load", "reset", "close", "check", "save", "editor", "delete"]

        self.buttons_basic_images = self.create_dictionary_for_images("textures/buttons/basic/",
                                                                      self.buttons_array_names)
        self.buttons_filled_images = self.create_dictionary_for_images("textures/buttons/filled/",
                                                                       self.buttons_array_names)
        self.planets_images = self.create_dictionary_for_images("textures/planets/",
                                                                ["earth", "jupiter", "mars", "mercury", "neptune",
                                                                 "saturn", "uranus", "venus"])
        self.transport_images = self.create_dictionary_for_images("textures/transportunits/",
                                                                  ["rocket", "ufo", "rocket_small", "ufo_small"])

        self.title_images = self.create_dictionary_for_images("textures/titles/", ["path", "task"])

        self.buttons_id = {}

        self.create_buttons()
        self.buttons_bind = self.canvas.bind("<Motion>", self.filled_button)
        self.buttons_action_bind = self.canvas.tag_bind("button", "<Button-1>", self.buttons_action)

        self.te = None

        self.g = Graph(self.canvas, self.planets_images, self.transport_images, self.random_type > 2)

        self.file_name = file_name
        x = load_data(self.file_name)
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

    def create_buttons(self):
        y = 50
        for buttonName in ["load", "editor", "reset", "close"]:
            self.buttons_id[buttonName] = self.canvas.create_image(150, y,
                                                                   image=self.buttons_basic_images[buttonName],
                                                                   tag="button")
            y += 65
        self.buttons_id["check"] = self.canvas.create_image(1745, 850, image=self.buttons_basic_images["check"],
                                                            tag="button")

        self.canvas.create_image(1755, 50, image=self.title_images["task"], tag="title")
        if self.random_type < 3:
            self.canvas.create_image(960, 880, image=self.title_images["path"], tag="title")
        self.canvas.update()

    def remove_objects_with_tag(self,tag):
        for item in self.canvas.find_withtag(tag):
            self.canvas.delete(item)

    def create_editor_buttons(self):
        self.buttons_id["save"] = self.canvas.create_image(150, 500, image=self.buttons_basic_images["save"],
                                                           tag="button")
        #self.buttons_id["delete"] = self.canvas.create_image(150, 560, image=self.buttons_basic_images["delete"],
                                                           #tag="button")

    def filled_button(self, event):
        for buttonsName in self.buttons_id.keys():
            if self.canvas.coords(self.buttons_id[buttonsName]) == self.canvas.coords("current"):
                self.canvas.itemconfig("current", image=self.buttons_filled_images[buttonsName])
            else:
                self.canvas.itemconfig(self.buttons_id[buttonsName], image=self.buttons_basic_images[buttonsName])

    def browse_file(self):
        self.file_name = filedialog.askopenfilename(initialdir="/",
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
        if self.canvas.coords("current") == self.canvas.coords(self.buttons_id["editor"]):
            if self.te is not None:
                return
            self.change_text('')
            self.g.delete_all()
            self.task.clear()
            self.delete_unused_editor_buttons()
            self.te = TaskEditor(self.canvas, self.planets_images, self.transport_images)
            self.create_editor_buttons()

        if self.canvas.coords("current") == self.canvas.coords(self.buttons_id["load"]):
            if self.te is not None:
                self.te.close()
            self.browse_file()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["reset"]):
            if self.te is not None:
                self.te.close()
                self.te = None
            self.reset()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["close"]):
            quit()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["check"]):
            self.check_path()

        elif self.buttons_id["save"] is not None and self.canvas.coords("current") == self.canvas.coords(
                self.buttons_id["save"]):
            if self.te.correct_map():
                self.save_map()
            else:
                print('Wrong map')

    def check_path(self):
        if self.random_type in [3, 4]:
            selected = list(self.g.vertex_markers.keys())
            try:
                selected = selected[0].name
            except IndexError:
                self.change_text('Nebola vybrana planeta')
                return
            if self.random_type == 3:
                for path in self.g.all_paths[self.random_length]:
                    if path[1] == self.g.all_paths[self.random_length][self.random_path][1] and path[0][-1] == selected\
                            and path[0][0] == self.g.all_paths[self.random_length][self.random_path][0][0]:
                        self.change_text('Spravne riesenie')
                        return
                self.change_text('Nespravne riesnie')
            if self.random_type == 4:
                for path in self.g.all_paths[self.random_length]:
                    if path[1] == self.g.all_paths[self.random_length][self.random_path][1] and path[0][0] == selected\
                            and path[0][-1] == self.g.all_paths[self.random_length][self.random_path][0][-1]:
                        self.change_text('Spravne riesenie')
                        return
                self.change_text('Nespravne riesnie')
        elif self.random_type == 1:
            selected_transport = ['rocket' if x == 0 else 'ufo' for x in self.get_results_transport_units()]
            source = self.g.all_paths[self.random_length][self.random_path][0][0]
            destination = self.g.all_paths[self.random_length][self.random_path][0][-1]
            for path in self.g.all_paths[len(selected_transport)]:
                if path[0][0] == source and path[0][-1] == destination and path[1] == selected_transport:
                    self.change_text('Spravne riesenie')
                    return
            self.change_text('Nespravne riesnie')
        else:
            selected_transport = ['rocket' if x == 0 else 'ufo' for x in self.get_results_transport_units()]
            for path in self.g.all_paths[len(selected_transport)]:
                if path[1] == selected_transport and self.g.all_paths[self.random_length][self.random_path][0] == path[
                    0]:
                    self.change_text('Spravne riesenie')
                    return
            self.change_text('Nespravne riesnie')

    def change_text(self, text):
        self.canvas.itemconfig(self.msg, text=text)

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
        Main(self.canvas, self.file_name)


class Game:
    def __init__(self, canvas, transport_units):
        self.canvas = canvas
        self.max_results_transport_units = 10
        self.transport_units = transport_units
        self.transport_units_objects = []
        self.results_transport_units = []
        self.place_for_results_transport_units = self.canvas.create_rectangle(400, 850, 1545, 1000, tag="units_place")
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
                self.append_to_results_transport_unit(kind)
        self.remake_transport_units_objects()

    def append_to_results_transport_unit(self, kind):
        self.results_transport_units.append(
            (kind, self.canvas.create_image(475 + len(self.results_transport_units) * 110, 930,
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
            self.canvas.create_image(1745, 910, image=self.transport_units["rocket"], tag="movable"))
        self.transport_units_objects.append(
            self.canvas.create_image(1755, 970, image=self.transport_units["ufo"], tag="movable"))

    def remake_transport_units_objects(self):
        self.clean_transport_units_objects()
        self.create_transport_units()

    def move_transport_unit(self, event):
        self.canvas.coords("current", event.x, event.y)