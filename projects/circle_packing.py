import tkinter as tk
import config as cfg
import random as rnd


class Circle:
    def __init__(self, master, x, y, r, num, *args, **kwargs):
        self.master = master
        self.x = x
        self.y = y
        self.r = r
        self.num = num
        self.object = self.master.canvas.create_oval(x - r, y - r, x + r, y + r, tags=num, *args, **kwargs)
        self.master.after(0, self.grow)

    def grow(self):
        if self.master.is_growable(self):
            self.r += 0.5
            self.master.canvas.coords(self.object, self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)
            self.master.after(self.master.growing_delay, self.grow)
        else:
            self.master.after(self.master.simultaneous_circles*2, self.master.add_circle)


class CircleMain(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        self.c_width = 0
        self.c_height = 0
        self.simultaneous_circles = 5
        self.max_attempts = 100
        self.starting_radius = 0
        self.drawing = True
        self.growing_delay = 1
        self.circle_list = []

        self.canvas = tk.Canvas(self, bg=cfg.bgc, highlightthickness=1, cursor='tcross', xscrollincrement='1')

        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.master.bind('<Escape>', quit)  # todo: remove later

        self.after(100, self.initialize)

    def initialize(self):
        self.c_width = self.canvas.winfo_width()
        self.c_height = self.canvas.winfo_height()
        for _ in range(self.simultaneous_circles):
            self.after(0, self.add_circle)

    def add_circle(self):
        """ adds a circle to the canvas and grows it until it hits an object or the edge of the canvas """
        attempts = 0
        # print('adding circle')
        while attempts < self.max_attempts:
            r = self.starting_radius
            x = rnd.randint(0, self.c_width)
            y = rnd.randint(0, self.c_height)
            if self.is_drawable(x, y):
                self.circle_list.append(Circle(self, x, y, r, len(self.circle_list)+1, outline=cfg.fgc, width=1))
                # print('circle added')
                break
            attempts += 1
        if attempts == self.max_attempts:
            print("Drawing failed")
            self.drawing = False

    def is_drawable(self, x, y):
        """ checks whether a certain point allows for drawing of a new circle """
        for circle in self.circle_list:
            if ((x-circle.x) ** 2 + (y-circle.y) ** 2) ** 0.5 < circle.r:
                return False
        return True

    def is_growable(self, current):
        """ checks whether the circle has space to grow to """
        if current.x-current.r < 0 or current.x+current.r > self.c_width-3 or current.y-current.r < 0\
                or current.y+current.r > self.c_height-3:                           # does circle grow out of bounds?
            # print("circle can't grow, because it hit the outer bounds")
            return False
        for circle in self.circle_list:
            if circle != current:
                if ((current.x-circle.x) ** 2 + (current.y-circle.y) ** 2) ** 0.5 <\
                        current.r+circle.r+0.5:                                     # does circle hit another circle?
                    # print("circle can't grow, because it hit another circle")
                    return False
        return True


root = tk.Tk()                                  # todo: remove later
root.attributes('-fullscreen', True)
CircleMain(root).pack(side="top", fill="both", expand=True)
root.mainloop()
