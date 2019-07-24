import tkinter as tk
import config as cfg
import random as rnd
import time as ti


class Circle:
    def __init__(self, master, x, y, r, num, *args, **kwargs):
        self.master = master
        self.x = x
        self.y = y
        self.r = r
        self.num = num
        self.object_aa = self.master.canvas.create_oval(x - r, y - r, x + r, y + r, tags=num, outline=cfg.fgc_a,
                                                        width=1.5, *args, **kwargs)
        self.object = self.master.canvas.create_oval(x - r, y - r, x + r, y + r, tags=num, outline=cfg.fgc,
                                                     width=1, *args, **kwargs)
        self.master.after(1, self.grow)

    def grow(self):
        if self.master.is_growable(self):
            self.r += 0.5
            self.master.canvas.coords(self.object_aa, self.x - self.r, self.y - self.r,
                                      self.x + self.r, self.y + self.r)
            self.master.canvas.coords(self.object, self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r)
            self.master.after(self.master.growing_delay, self.grow)
        elif self.master.drawing:
            self.master.after(self.master.simultaneous_circles*2-2, self.master.add_circle)


class CircleMain(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        self.starting_time = ti.time()
        self.c_width = 0
        self.c_height = 0
        self.simultaneous_circles = 1
        self.max_attempts = 1000
        self.min_r = 3
        self.max_r = 50
        self.drawing = True
        self.growing_delay = 2
        self.circle_list = []
        self.drawing_mode = 2               # 1: rectangle fill, 2: b/w fill, 3: colored picture fill
        self.image = None
        self.current_image = None
        self.img_min_x = None
        self.img_max_x = None
        self.img_min_y = None
        self.img_max_y = None

        self.canvas = tk.Canvas(self, bg=cfg.bgc, highlightthickness=1, cursor='tcross', xscrollincrement='1')

        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.after(100, self.initialize)

    def initialize(self):
        self.starting_time = ti.time()
        self.c_width = self.canvas.winfo_width()
        self.c_height = self.canvas.winfo_height()
        if self.drawing_mode == 2:
            self.image = tk.PhotoImage(file="logo2.gif")
            self.current_image = self.canvas.create_image((self.c_width / 2, self.c_height / 2), image=self.image,
                                                          state="normal")
            self.img_min_x = self.c_width // 2 - self.image.width() // 2
            self.img_max_x = self.c_width // 2 + self.image.width() // 2
            self.img_min_y = self.c_height // 2 - self.image.height() // 2
            self.img_max_y = self.c_height // 2 + self.image.height() // 2
        for _ in range(self.simultaneous_circles):
            self.after(1, self.add_circle)

    def add_circle(self):
        """ adds a circle to the canvas and grows it until it hits an object or the edge of the canvas """
        attempts = 0
        # print('adding circle')
        while attempts < self.max_attempts:
            r = self.min_r
            if self.drawing_mode == 1:
                x = rnd.randint(self.min_r+1, self.c_width - self.min_r - 2)
                y = rnd.randint(self.min_r+1, self.c_height - self.min_r - 2)
            elif self.drawing_mode == 2:
                x = rnd.randint(self.img_min_x + self.min_r + 1, self.img_max_x - self.min_r - 2)
                y = rnd.randint(self.img_min_y + self.min_r + 1, self.img_max_y - self.min_r - 2)
            if self.is_drawable(x, y):
                self.circle_list.append(Circle(self, x, y, r, len(self.circle_list)+1))
                # print('circle added')
                break
            attempts += 1
        if attempts == self.max_attempts:
            if self.drawing_mode == 2:
                self.image = None
                self.current_image = None
            self.master.master.status.set(f"Rechendauer: {round(ti.time()-self.starting_time, 2)}s")
            self.drawing = False

    def is_drawable(self, x, y):
        """ checks whether a certain point allows for drawing of a new circle """
        if self.drawing_mode == 1:
            for circle in self.circle_list:
                if ((x-circle.x) ** 2 + (y-circle.y) ** 2) ** 0.5 < circle.r+self.min_r+1.5:
                    return False
        elif self.drawing_mode == 2:
            for circle in self.circle_list:
                if ((x-circle.x) ** 2 + (y-circle.y) ** 2) ** 0.5 < circle.r+self.min_r+1.5:
                    return False

        return True

    def is_growable(self, current):
        """ checks whether the circle has space to grow to """
        if current.r > self.max_r:
            return False
        if self.drawing_mode == 1:
            if current.x-current.r < 1 or current.x+current.r > self.c_width-3 or current.y-current.r < 1\
                    or current.y+current.r > self.c_height-3:                       # does circle grow out of bounds?
                # print("circle can't grow, because it hit the outer bounds")
                return False
        elif self.drawing_mode == 2:
            # does circle grow out of bounds?
            if current.x-current.r < self.img_min_x+1 or current.x+current.r > self.img_max_x-2\
                    or current.y-current.r < self.img_min_y+1 or current.y+current.r > self.img_max_y-2:
                # print("circle can't grow, because it hit the outer bounds")
                return False
        for circle in self.circle_list:
            if circle != current:
                if ((current.x-circle.x) ** 2 + (current.y-circle.y) ** 2) ** 0.5 <\
                        current.r+circle.r+0.5:                                     # does circle hit another circle?
                    # print("circle can't grow, because it hit another circle")
                    return False
        return True
