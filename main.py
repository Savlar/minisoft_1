import tkinter


class Program:
    def __init__(self):
        win = tkinter.Tk()
        self.canvas = tkinter.Canvas(height=800, width=1360)
        self.canvas.configure(background="grey")
        self.canvas.pack()

        Main(self.canvas)
        win.mainloop()


class Main:
    def __init__(self, canvas):
        self.canvas = canvas

        self.buttons_basic_images = self.create_dictionary_for_images("textures/buttons/basic/", ["settings", "load", "reset", "close"])
        self.buttons_filled_images = self.create_dictionary_for_images("textures/buttons/filled/", ["settings", "load", "reset", "close"])
        self.planets_images = self.create_dictionary_for_images("textures/planets/", ["earth", "jupiter", "mars", "mercury", "neptune", "saturn", "uranus", "venus"])
        self.transport_units_images = self.create_dictionary_for_images("textures/transportunits/", ["rocket", "ufo"])
        self.buttons_id = {}

        self.create_buttons()
        self.buttons_bind = self.canvas.bind("<Motion>", self.filled_button)
        self.buttons_action_bind = self.canvas.tag_bind("button", "<Button-1>", self.buttonsAction)

    def create_dictionary_for_images(self, path, image_list):
        images = {}

        for item in image_list:
            images[item] = tkinter.PhotoImage(file=f"{path}{item}.png")

        return images

    def create_buttons(self):
        x = 120
        for buttonName in self.buttons_basic_images.keys():
            self.buttons_id[buttonName] = self.canvas.create_image(x, 30, image=self.buttons_basic_images[buttonName], tag="button")
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
    def __init__(self, canvas):
        self.canvas = canvas


class Settings:
    def __init__(self, canvas):
        self.canvas = canvas

    def return_to_menu(self, event):
        self.canvas.unbind_all("<Escape>")
        self.canvas.delete("all")
        Main(self.canvas)


Program()
