import tkinter

from PIL import ImageTk, Image

from graph import Graph


class Program:
    def __init__(self):
        win = tkinter.Tk()
        self.canvas = tkinter.Canvas(height=1080, width=1920, bg='grey')
        self.canvas.pack()

        Main(self.canvas)
        win.mainloop()


class Main:
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas.transport_types = []
        self.canvas.transport_types.append(ImageTk.PhotoImage(Image.open('textures/transportunits/rocket.png').resize((40, 40))))
        self.canvas.transport_types.append(ImageTk.PhotoImage(Image.open('textures/transportunits/ufo.png').resize((40, 40))))

        self.buttons_basic_images = self.create_dictionary_for_images("textures/buttons/basic/",
                                                                      ["settings", "load", "reset", "close"])
        self.buttons_filled_images = self.create_dictionary_for_images("textures/buttons/filled/",
                                                                       ["settings", "load", "reset", "close"])
        self.planets_images = self.create_dictionary_for_images("textures/planets/",
                                                                ["earth", "jupiter", "mars", "mercury", "neptune",
                                                                 "saturn", "uranus", "venus"])
        self.transport_units_images = self.create_dictionary_for_images("textures/transportunits/", ["rocket", "ufo"])
        self.buttons_id = {}

        self.create_buttons()
        self.buttons_bind = self.canvas.bind("<Motion>", self.filled_button)
        self.buttons_action_bind = self.canvas.tag_bind("button", "<Button-1>", self.buttonsAction)

        self.create_rectangles()
        Game(self.canvas, self.transport_units_images)
        self.graph = Graph(self.canvas)

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
            self.buttons_id[buttonName] = self.canvas.create_image(x, 30, image=self.buttons_basic_images[buttonName],
                                                                   tag="button")
            x += 250
        self.canvas.update()

    def filled_button(self, event):
        for buttonsName in self.buttons_filled_images.keys():
            if self.canvas.coords(self.buttons_id[buttonsName]) == self.canvas.coords("current"):
                self.canvas.itemconfig("current", image=self.buttons_filled_images[buttonsName])
            else:
                self.canvas.itemconfig(self.buttons_id[buttonsName], image=self.buttons_basic_images[buttonsName])

    def buttonsAction(self, event):
        if self.canvas.coords("current") == self.canvas.coords(self.buttons_id["load"]):
            self.clean_main_menu()
            Game(self.canvas)

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["settings"]):
            Settings(self.canvas)

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["reset"]):
            self.clean_main_menu()
            self.reset()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_id["close"]):
            quit()

    def clean_main_menu(self):
        self.canvas.delete("all")
        self.canvas.unbind("<Motion>", self.buttons_bind)
        self.canvas.unbind("<Button-1>", self.buttons_action_bind)

    def reset(self):
        self.canvas.unbind_all("<Escape>")
        self.canvas.delete("all")
        Main(self.canvas)


class Game:
    def __init__(self, canvas, transport_units):
        self.canvas = canvas
        self.transport_units = transport_units
        self.transport_units_objects = []
        self.results_transport_units = []
        self.place_for_results_transport_units = self.canvas.create_rectangle(10, 870, 1120, 1060, tag="units_place")
        self.results_rectangle_coords = self.canvas.coords(self.place_for_results_transport_units)
        self.movable_units = self.canvas.tag_bind("movable", "<B3-Motion>", self.move_transport_unit)
        self.release_units = self.canvas.tag_bind("movable", "<ButtonRelease-3>", self.release_transport_unit)
        self.click_units = self.canvas.tag_bind("movable", "<Button-1>", self.add_transport_unit_on_click)
        self.create_transport_units()
        self.canvas.update()

    def add_transport_unit_on_click(self, event):
        kind = "ufo"
        if self.canvas.find_withtag("current")[0] == self.transport_units_objects[0]:
            kind = "rocket"

        self.results_transport_units.append(self.canvas.create_image(80 + len(self.results_transport_units) * 100, 940,
                                                                     image=(self.transport_units[
                                                                                "rocket"] if kind == "rocket" else
                                                                            self.transport_units["ufo"]),
                                                                     tag="results_clickable"))

    def clean_transport_units_objects(self):
        for objc in self.transport_units_objects:
            self.canvas.delete(objc)
        self.transport_units_objects = []

    def create_transport_units(self):
        self.transport_units_objects.append(
            self.canvas.create_image(1240, 900, image=self.transport_units["rocket"], tag="movable"))
        self.transport_units_objects.append(
            self.canvas.create_image(1250, 970, image=self.transport_units["ufo"], tag="movable"))

    def remake_transport_units_objects(self):
        self.clean_transport_units_objects()
        self.create_transport_units()

    def move_transport_unit(self, event):
        self.canvas.coords("current", event.x, event.y)

    def release_transport_unit(self, event):
        current_coords = [event.x, event.y]
        kind = "ufo"

        if self.canvas.find_withtag("current")[0] == self.transport_units_objects[0]:
            kind = "rocket"

        if self.results_rectangle_coords == current_coords or self.results_rectangle_coords[0] + 1110 >= current_coords[
            0] and self.results_rectangle_coords[0] - 1110 <= current_coords[
            0] and self.results_rectangle_coords[1] + 150 >= current_coords[1] >= self.results_rectangle_coords[
            1] - 150:
            self.results_transport_units.append(
                self.canvas.create_image(80 + len(self.results_transport_units) * 100, 1200, image=(
                    self.transport_units["rocket"] if kind == "rocket" else self.transport_units["ufo"]),
                                         tag="results_clickable"))
        self.remake_transport_units_objects()


class Settings:
    def __init__(self, canvas):
        self.canvas = canvas

    def return_to_menu(self, event):
        self.canvas.unbind_all("<Escape>")
        self.canvas.delete("all")
        Main(self.canvas)
