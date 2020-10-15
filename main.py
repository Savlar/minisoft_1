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

        self.buttonsBasicImages = self.createDictionaryForImages("textures/buttons/basic/", ["settings", "load", "reset", "close"])
        self.buttonsFilledImages = self.createDictionaryForImages("textures/buttons/filled/", ["settings", "load", "reset", "close"])
        self.planetsImages = self.createDictionaryForImages("textures/planets/", ["earth", "jupiter", "mars", "mercury", "neptune", "saturn", "uranus", "venus"])
        self.transportUnitsImages = self.createDictionaryForImages("textures/transportunits/", ["rocket", "ufo"])
        self.buttonsId = {}

        self.createButtons()
        self.buttonsBind = self.canvas.tag_bind("button", "<Motion>", self.filledButton)
        self.buttonsActionBind = self.canvas.tag_bind("button", "<Button-1>", self.buttonsAction)

    def createDictionaryForImages(self, path, imagelist):
        images = {}

        for item in imagelist:
            images[item] = tkinter.PhotoImage(file=f"{path}{item}.png")

        return images

    def createButtons(self):
        x = 120
        for buttonName in self.buttonsBasicImages.keys():
            self.buttonsId[buttonName] = self.canvas.create_image(x, 30, image=self.buttonsBasicImages[buttonName], tag="button")
            x += 250
        self.canvas.update()

    def filledButton(self, event):
        for buttonsName in self.buttonsFilledImages.keys():
            if self.canvas.coords(self.buttonsId[buttonsName]) == self.canvas.coords("current"):
                self.canvas.itemconfig("current", image=self.buttonsFilledImages[buttonsName])
            else:
                self.canvas.itemconfig(self.buttonsId[buttonsName], image=self.buttonsBasicImages[buttonsName])

    def buttonsAction(self, event):
        if self.canvas.coords("current") == self.canvas.coords(self.buttonsId["load"]):
            self.clean_main_menu()
            Game(self.canvas)

        elif self.canvas.coords("current") == self.canvas.coords(self.buttonsId["settings"]):
            Settings(self.canvas)

        elif self.canvas.coords("current") == self.canvas.coords(self.buttonsId["reset"]):
            self.clean_main_menu()
            self.reset()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttonsId["close"]):
            quit()

    def clean_main_menu(self):
        self.canvas.delete("all")
        self.canvas.unbind("<Motion>", self.buttonsBind)
        self.canvas.unbind("<Button-1>", self.buttonsActionBind)

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
