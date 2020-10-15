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
        self.buttons_bind = None
        self.buttons_action_bind = None
        self.buttons_basic = [tkinter.PhotoImage(file=f"textures/buttons/basic/{i}.png") for i in range(0, 4)]  # [LOAD/SETTINGS/RESET/QUIT 0/1/2/3]
        self.buttons_filled = [tkinter.PhotoImage(file=f"textures/buttons/filled/{i}.png") for i in range(0, 4)]

        self.canvas = canvas
        self.buttons_ID = []

        self.buttons()
        self.buttons_bind = self.canvas.tag_bind("button", "<Motion>", self.filled_button)
        self.buttons_action_bind = self.canvas.tag_bind("button", "<Button-1>", self.buttons_action)

    def buttons(self):
        x = 90
        for number in range(4):
            self.buttons_ID.append(
                self.canvas.create_image(x, 40, image=self.buttons_basic[number], tag="button"))
            x += 250
        self.canvas.update()

    def filled_button(self, event):
        for number in range(4):
            if self.canvas.coords(self.buttons_ID[number]) == self.canvas.coords("current"):
                self.canvas.itemconfig("current", image=self.buttons_filled[number])
            else:
                self.canvas.itemconfig(self.buttons_ID[number], image=self.buttons_basic[number])

    def buttons_action(self, event):
        if self.canvas.coords("current") == self.canvas.coords(self.buttons_ID[0]):
            self.clean_main_menu()
            Game(self.canvas)

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_ID[1]):
            Settings(self.canvas)

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_ID[2]):
            self.clean_main_menu()
            self.reset()

        elif self.canvas.coords("current") == self.canvas.coords(self.buttons_ID[3]):
            quit()

    def clean_main_menu(self):
        self.canvas.delete("all")
        self.canvas.unbind("<Motion>", self.buttons_bind)
        self.canvas.unbind("<Button-1>", self.buttons_action_bind)

    def reset(self):
        self.canvas.unbind_all("<Escape>")
        self.canvas.delete("all")
        Main(self.canvas)


class Settings:
    def __init__(self, canvas):
        self.canvas = canvas

    def return_to_menu(self, event):
        self.canvas.unbind_all("<Escape>")
        self.canvas.delete("all")
        Main(self.canvas)




Program()
