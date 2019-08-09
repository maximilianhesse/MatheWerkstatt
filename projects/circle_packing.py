import tkinter as tk
import config as cfg
import random as rnd
import time as ti
import PIL.Image
import PIL.ImageTk


class Circle:
    def __init__(self, master, x, y, r, num, *args, **kwargs):
        self.master = master
        self.x = x
        self.y = y
        self.r = r
        self.num = num
        if self.master.drawing_mode == 3:
            self.object_aa = None
            self.object = self.master.canvas.create_oval(x - r, y - r, x + r, y + r, tags=num,
                                                         width=1, *args, **kwargs)
        else:
            self.object_aa = self.master.canvas.create_oval(x - r, y - r, x + r, y + r, tags=num, outline=cfg.fgc_a,
                                                            width=1.5, *args, **kwargs)
            self.object = self.master.canvas.create_oval(x - r, y - r, x + r, y + r, tags=num, outline=cfg.fgc,
                                                         width=1, *args, **kwargs)
        self.master.after(1, self.grow)

    def grow(self):
        if self.master.is_growable(self):
            self.r += 0.5
            if self.master.drawing_mode != 3:
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
        self.max_attempts = 10000
        self.min_r = 1
        self.max_r = 150
        self.drawing = True
        self.growing_delay = 1
        self.circle_list = []
        self.drawing_mode = 1               # 1: rectangle fill, 2: b/w fill, 3: colored picture fill
        self.pil_im = None
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
            # todo: add more functionality, like canceling the initialization and asking for a new image...
            pixels_total = 0
            pixels_c = 0
            pixels_b = 0
            pixels_w = 0
            for x in range(self.image.width()):
                for y in range(self.image.height()):
                    pixels_total += 1
                    if self.image.get(x, y) == (0, 0, 0):
                        pixels_b += 1
                    elif self.image.get(x, y) == (255, 255, 255):
                        pixels_w += 1
                    else:
                        pixels_c += 1
            percent_c = round(100 * pixels_c / pixels_total, 2)
            percent_b = round(100 * pixels_b / pixels_total, 2)
            percent_w = round(100 * pixels_w / pixels_total, 2)
            self.master.master.status.set(f'Farbzusammensetzung: {percent_b}% schwarz, {percent_w}% weiß, '
                                          f'{percent_c}% "farbig"')

            self.current_image = self.canvas.create_image((self.c_width / 2, self.c_height / 2), image=self.image,
                                                          state="normal")
            self.img_min_x = self.c_width // 2 - self.image.width() // 2
            self.img_max_x = self.c_width // 2 + self.image.width() // 2
            self.img_min_y = self.c_height // 2 - self.image.height() // 2
            self.img_max_y = self.c_height // 2 + self.image.height() // 2
        if self.drawing_mode == 3:
            im = PIL.Image.open("logo3.jpg")
            self.pil_im = im.convert('RGB')
            self.image = PIL.ImageTk.PhotoImage(self.pil_im)
            self.current_image = self.canvas.create_image((self.c_width / 2, self.c_height / 2), image=self.image,
                                                          state="normal")
            self.img_min_x = self.c_width // 2 - self.image.width() // 2
            self.img_max_x = self.c_width // 2 + self.image.width() // 2
            self.img_min_y = self.c_height // 2 - self.image.height() // 2
            self.img_max_y = self.c_height // 2 + self.image.height() // 2

        for _ in range(self.simultaneous_circles):
            self.after(0, self.add_circle)

    def add_circle(self):
        """ adds a circle to the canvas and grows it until it hits an object or the edge of the canvas """
        attempts = 0
        # print('adding circle')
        while attempts < self.max_attempts:
            r = self.min_r
            if self.drawing_mode == 1:
                x = rnd.randint(self.min_r+1, self.c_width - self.min_r - 2)
                y = rnd.randint(self.min_r+1, self.c_height - self.min_r - 2)
                if self.is_drawable(x, y):
                    self.circle_list.append(Circle(self, x, y, r, len(self.circle_list) + 1))
                    # print('circle added')
                    break
            else:
                x = rnd.randint(self.img_min_x + self.min_r + 1, self.img_max_x - self.min_r - 2)
                y = rnd.randint(self.img_min_y + self.min_r + 1, self.img_max_y - self.min_r - 2)
                if self.drawing_mode == 2:
                    if self.is_drawable(x, y):
                        self.circle_list.append(Circle(self, x, y, r, len(self.circle_list) + 1))
                        # print('circle added')
                        break
                else:
                    if self.is_drawable(x, y):
                        color = "#%02x%02x%02x" % self.pil_im.getpixel((x-self.img_min_x, y-self.img_min_y))
                        self.circle_list.append(Circle(self, x, y, r, len(self.circle_list) + 1, outline=color,
                                                       fill=color))
                        # print('circle added')
                        break

            attempts += 1
        if attempts == self.max_attempts:
            if self.drawing_mode != 1:
                self.image = None
                self.current_image = None
            if self.drawing_mode == 3:
                self.pil_im = None
            self.master.master.status.set(f"Rechendauer: {round(ti.time()-self.starting_time, 2)}s")
            self.drawing = False

    def is_drawable(self, x, y):
        """ checks whether a certain point allows for drawing of a new circle """
        for circle in self.circle_list:
            if ((x-circle.x) ** 2 + (y-circle.y) ** 2) ** 0.5 < circle.r+self.min_r+1.5:
                return False
        if self.drawing_mode == 2:
            """ checks for all points in the possible circle if the color is black """
            for rect_x in range(x - self.img_min_x - self.min_r, x - self.img_min_x + self.min_r):
                for rect_y in range(y - self.img_min_y - self.min_r, y - self.img_min_y + self.min_r):
                    if ((x-self.img_min_x-rect_x)**2 + (y-self.img_min_y-rect_y)**2)**0.5 <= self.min_r:
                        if self.image.get(rect_x, rect_y) != (0, 0, 0):
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
            for rect_x in range(int(current.x-self.img_min_x-current.r-0.5),
                                int(current.x-self.img_min_x+current.r+0.5)):
                for rect_y in range(int(current.y-self.img_min_y-current.r-0.5),
                                    int(current.y-self.img_min_y+current.r+0.5)):
                    if ((current.x-self.img_min_x-rect_x)**2+(current.y-self.img_min_y-rect_y)**2)**0.5\
                            <= current.r+0.5:
                        if self.image.get(rect_x, rect_y) != (0, 0, 0):
                            return False
        else:
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
