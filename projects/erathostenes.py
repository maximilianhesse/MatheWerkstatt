import tkinter as tk
import config as cfg
from numba import jit
import time as ti


@jit
def prime_finder(num):
    """ returns a list of all prime numbers up to and including num and up to and including num*3 """
    prime_list = [True for _ in range(num+1)]
    prime_list[0] = False
    prime_list[1] = False
    for n in range(int(num**0.5)+1):
        if prime_list[n]:
            for k in range(2*n, num+1, n):
                prime_list[k] = False
    return_list_small = []
    for i in range(num+1):
        if prime_list[i]:
            return_list_small.append(i)
    num *= 3
    prime_list_2 = [True for _ in range(num + 1)]
    prime_list_2[0] = False
    prime_list_2[1] = False
    for n in range(int(num ** 0.5) + 1):
        if prime_list_2[n]:
            for k in range(2 * n, num + 1, n):
                prime_list_2[k] = False
    return_list_large = []
    for i in range(num + 1):
        if prime_list_2[i]:
            return_list_large.append(i)

    return return_list_small, return_list_large


class InfoFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.master = master

        self.prime_label = tk.Label(self, font=cfg.font_text, bg=cfg.bgc, fg=cfg.fgc,
                                    text=f'Primzahlen bis {self.master.canvas.max_num}:'
                                         f' {self.master.canvas.prime_list}')
        self.prime_label.pack(side=tk.TOP, fill=tk.X)


class ECanvas(tk.Canvas):
    def __init__(self, master, max_num=100, aa=True, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)

        self.master = master
        self.max_num = max_num
        self.scale_factor = 1.0
        self.number_state = tk.HIDDEN
        self.anti_aliasing = aa
        self.prime_list, self.expanded_prime_list = prime_finder(self.max_num)
        self.circle_list = []
        self.circle_list_aa = []
        self.dot_list = []
        self.number_list = []
        self.coordinate_radius = 0.1
        self.y_center = 1
        self.height = 1
        self.width = 1

        self.bind('<Button-3>', self.m3_drag_start)
        self.bind('<B3-Motion>', self.m3_dragging)
        self.bind('<ButtonRelease-3>', self.m3_drag_stop)
        self.bind('<MouseWheel>', self.zoom)
        self.bind('<Button-1>', self.m1)

    def initialize(self):
        start = ti.time()
        self.circle_list = []
        self.circle_list_aa = []
        self.delete(tk.ALL)
        self.prime_list, self.expanded_prime_list = prime_finder(self.max_num)
        self.height = self.winfo_height()
        self.width = self.winfo_width()
        self.y_center = self.height*0.5
        self.draw_all_circles()
        self.draw_number_line()
        self.draw_numbers()

        """ adjust canvas to show everything """
        self.xview_scroll(-(int((self.width-(3*self.prime_list[-1])-1)*0.5)), "units")
        factor = 0.98*self.width/(3*self.prime_list[-1])
        self.scale_factor *= factor
        self.scale(tk.ALL, self.canvasx(int(self.width*0.5)), self.canvasy(int(self.height*0.5)), factor, factor)

        self.master.master.master.status.set(f"Rechendauer: {round(ti.time()-start, 2)}s")

    def m1(self, _event):
        """ left click on canvas event - includes click events on objects """
        current_tags = self.gettags(tk.CURRENT)
        if self.find_withtag(tk.CURRENT):
            if 'dot' in current_tags or 'num' in current_tags:                  # events bound to the number line
                factor_set = self.prime_factorization(int(current_tags[1]))
                if self.anti_aliasing:
                    for circle in self.circle_list_aa:
                        if int(self.gettags(circle)[1]) in factor_set:
                            self.itemconfigure(circle, state=tk.NORMAL)
                        else:
                            self.itemconfigure(circle, state=tk.HIDDEN)
                for circle in self.circle_list:
                    if int(self.gettags(circle)[1]) in factor_set:
                        self.itemconfigure(circle, state=tk.NORMAL)
                    else:
                        self.itemconfigure(circle, state=tk.HIDDEN)
            elif 'circle' in current_tags or 'circle_aa' in current_tags:       # events bound to prime circles
                if self.anti_aliasing:
                    for circle in self.circle_list_aa:
                        if self.gettags(circle)[1] == current_tags[1]:
                            self.itemconfigure(circle, state=tk.NORMAL)
                        else:
                            self.itemconfigure(circle, state=tk.HIDDEN)
                for circle in self.circle_list:
                    if self.gettags(circle)[1] == current_tags[1]:
                        self.itemconfigure(circle, state=tk.NORMAL)
                    else:
                        self.itemconfigure(circle, state=tk.HIDDEN)
        else:                                                                   # events bound to the canvas background
            if self.anti_aliasing:
                for circle in self.circle_list_aa:
                    self.itemconfigure(circle, state=tk.NORMAL)
            for circle in self.circle_list:
                self.itemconfigure(circle, state=tk.NORMAL)

    def prime_factorization(self, num):
        """ returns a set of all primes that num is divisible by """
        factor_set = set()
        for prime in self.expanded_prime_list:
            if num % prime == 0:
                factor_set.add(prime)
        return factor_set

    def draw_circle(self, x, y, r, *args, **kwargs):
        """ Creates a circle with center x,y and radius r """
        return self.create_oval(x-r, y-r, x+r, y+r, *args, **kwargs)

    def draw_all_circles(self):
        if self.anti_aliasing:
            i = 0
            for prime in self.prime_list:
                color = cfg.c_map_2[i % len(cfg.c_map_2)]
                for current in range(0, int((3*self.prime_list[-1])/prime)-2):
                    self.circle_list_aa.append(self.draw_circle(prime*(2.5+current), self.y_center, prime/2,
                                                                outline=color, width=1.5, tags=("circle_aa", prime)))
                i += 1
        i = 0
        for prime in self.prime_list:
            color = cfg.c_map_1[i % len(cfg.c_map_1)]
            for current in range(0, int((3*self.prime_list[-1])/prime)-2):
                self.circle_list.append(self.draw_circle(prime*(2.5+current), self.y_center, prime/2,
                                                         outline=color, width=1, tags=("circle", prime)))
            i += 1

    def draw_number_line(self):
        self.dot_list = []
        for n in range(2, 3*self.prime_list[-1]+1):
            if n in self.expanded_prime_list:
                color = cfg.fgc_w
            else:
                color = cfg.fgc
            self.dot_list.append(self.create_oval(n - self.coordinate_radius, self.y_center - self.coordinate_radius,
                                                  n + self.coordinate_radius, self.y_center + self.coordinate_radius,
                                                  fill=color, width=0, tags=("dot", n)))

    def draw_numbers(self):
        self.number_list = []

        for n in range(1, 3*self.prime_list[-1]+1):
            if n in self.expanded_prime_list:
                color = cfg.bgc_w
            else:
                color = cfg.bgc
            self.number_list.append(self.create_text(n, self.y_center, text=n, fill=color, font=(cfg.font_only, 10),
                                                     state=self.number_state, tags=("num", n)))

    def m3_drag_start(self, event):
        """ sets starting point for moving the image if right mouse button is held down and dragged + cursor change """
        self.configure(cursor='fleur')
        self.scan_mark(event.x, event.y)

    def m3_dragging(self, event):
        """ moves the circles on the canvas according to the current cursor position """

        self.scan_dragto(event.x, event.y, gain=1)

    def m3_drag_stop(self, _event):
        self.configure(cursor='tcross')

    def zoom(self, event):
        if event.delta > 0:
            factor = 2
        else:
            factor = 0.5
        self.scale(tk.ALL, self.canvasx(event.x), self.canvasy(event.y), factor, factor)
        self.scale_factor *= factor
        tipping_point = 100
        if self.scale_factor > tipping_point:
            if self.number_state == tk.HIDDEN:
                self.number_state = tk.NORMAL
                for number in self.number_list:
                    self.itemconfig(number, state=self.number_state)
        if self.scale_factor <= tipping_point:
            if self.number_state == tk.NORMAL:
                self.number_state = tk.HIDDEN
                for number in self.number_list:
                    self.itemconfig(number, state=self.number_state)


class ErathostenesMain(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.master = master

        self.canvas = ECanvas(self, bg=cfg.bgc, highlightthickness=1, cursor='tcross', xscrollincrement='1')
        self.info = InfoFrame(self, bg=cfg.bgc, highlightthickness=1)

        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.info.pack(side=tk.TOP, fill=tk.X)

        self.canvas.after(100, self.canvas.initialize)
