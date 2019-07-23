import tkinter as tk
import numpy as np
import time as ti
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageTk
from numba import jit
import config as cfg
import os as os

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""                                                                                                                  """
"""                                           global color scheme                                                    """
"""                                                                                                                  """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

bgc = cfg.bgc      # background color
fgc = cfg.fgc      # foreground color
hbgc = cfg.hbgc    # highlight background color
hfgc = cfg.hfgc    # highlight foreground color


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""                                                                                                                  """
"""                                            global font style                                                     """
"""                                                                                                                  """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

font_heading = cfg.font_heading     # font for standard headings
font_text = cfg.font_text           # font for standard text


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""                                                                                                                  """
"""                                            initial settings                                                      """
"""                                                                                                                  """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

max_iterations = 256                            # standard maximum iterations
gamma = 0.3                                     # standard gamma setting
color_map = plt.get_cmap('gnuplot2')            # standard matplotlib color map


@jit
def check1(c, maxiter, horizon, log_horizon):
    z = c
    for n in range(maxiter):
        absz = abs(z)
        if absz > horizon:
            return n - np.log(np.log(absz)) / np.log(2) + log_horizon
        z = z * z + c
    return 0


@jit
def check2(c, maxiter):
    z = c
    for n in range(maxiter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return 0


@jit
def create(min_x, max_x, min_y, max_y, c_width, c_height, maxiter, antialiasing):
    horizon = 2.0 ** 40
    log_horizon = np.log(np.log(horizon)) / np.log(2)
    x_spaced = np.linspace(min_x, max_x, c_width)
    y_spaced = np.linspace(min_y, max_y, c_height)
    array = np.empty((c_height, c_width))
    if antialiasing:
        for x in range(c_width):
            for y in range(c_height):
                array[y, x] = check1(x_spaced[x] + y_spaced[y] * 1j, maxiter, horizon, log_horizon) / maxiter
        return array
    else:
        for x in range(c_width):
            for y in range(c_height):
                array[y, x] = check2(x_spaced[x] + y_spaced[y] * 1j, maxiter) / maxiter
        return array


def callback_int(p):
    if str.isdigit(p) or p == "":
        return True
    else:
        return False


def callback_float(p):
    if str.isdigit(p.replace(".", "", 1)) or p == "":
        return True
    else:
        return False


def callback_neg_float(p):
    if str.isdigit(p.replace(".", "", 1).replace("-", "", 1)) or p == "":
        return True
    else:
        return False


class InfoFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        vcmd_int = (self.register(callback_int))
        vcmd_float = (self.register(callback_float))
        # vcmd_neg_float = (self.register(callback_neg_float))

        self.text_settings = tk.Label(self, bg=bgc, fg=fgc, text='Einstellungen', font=font_heading)
        self.text_maxiter = tk.Label(self, bg=bgc, fg=fgc, text=f'Iterationstiefe:', font=font_text, justify=tk.LEFT)
        self.entry_maxiter = tk.Entry(self, font=font_text, bg=bgc, fg=fgc, width=10, selectbackground=hbgc,
                                      selectforeground=hfgc, validate='all', validatecommand=(vcmd_int, '%P'))
        self.entry_maxiter.insert(0, str(self.master.maxiter))
        self.entry_maxiter.bind("<KeyRelease>", self.update_maxiter)
        self.entry_maxiter.bind("<Return>", self.update_image)
        self.text_gamma = tk.Label(self, bg=bgc, fg=fgc, text=f'Gamma:',
                                   font=font_text, justify=tk.LEFT)
        self.entry_gamma = tk.Entry(self, font=font_text, bg=bgc, fg=fgc, width=10, selectbackground=hbgc,
                                    selectforeground=hfgc, validate='all', validatecommand=(vcmd_float, '%P'))
        self.entry_gamma.insert(0, str(self.master.gamma))
        self.entry_gamma.bind("<KeyRelease>", self.update_gamma)
        self.entry_gamma.bind("<Return>", self.update_image)
        self.button_settings_reset = tk.Button(self, text='Zurücksetzen', font=('Ebrima', 10), bg=bgc, fg=fgc,
                                               activebackground=hbgc, activeforeground=hfgc,
                                               command=self.master.reset_settings)

        self.text_colors = tk.Label(self, bg=bgc, fg=fgc, text='Farbschema', font=font_heading)
        self.new_cmap = tk.StringVar()
        self.new_cmap.set('gnuplot2')
        self.cmap_1 = tk.Radiobutton(self, bg=bgc, fg=fgc, selectcolor=bgc, activebackground=hbgc,
                                     activeforeground=hfgc, text='gnuplot2', font=font_text,
                                     variable=self.new_cmap, value='gnuplot2', command=self.update_cmap)
        self.cmap_2 = tk.Radiobutton(self, bg=bgc, fg=fgc, selectcolor=bgc, activebackground=hbgc,
                                     activeforeground=hfgc, text='hot', font=font_text,
                                     variable=self.new_cmap, value='hot', command=self.update_cmap)
        self.cmap_3 = tk.Radiobutton(self, bg=bgc, fg=fgc, selectcolor=bgc, activebackground=hbgc,
                                     activeforeground=hfgc, text='gist_earth', font=font_text,
                                     variable=self.new_cmap, value='gist_earth', command=self.update_cmap)
        self.cmap_4 = tk.Radiobutton(self, bg=bgc, fg=fgc, selectcolor=bgc, activebackground=hbgc,
                                     activeforeground=hfgc, text='gist_gray', font=font_text,
                                     variable=self.new_cmap, value='gist_gray', command=self.update_cmap)
        self.cmap_5 = tk.Radiobutton(self, bg=bgc, fg=fgc, selectcolor=bgc, activebackground=hbgc,
                                     activeforeground=hfgc, text='bone', font=font_text,
                                     variable=self.new_cmap, value='bone', command=self.update_cmap)
        self.cmap_6 = tk.Radiobutton(self, bg=bgc, fg=fgc, selectcolor=bgc, activebackground=hbgc,
                                     activeforeground=hfgc, text='seismic', font=font_text,
                                     variable=self.new_cmap, value='seismic', command=self.update_cmap)
        self.cmap_7 = tk.Radiobutton(self, bg=bgc, fg=fgc, selectcolor=bgc, activebackground=hbgc,
                                     activeforeground=hfgc, text='spring', font=font_text,
                                     variable=self.new_cmap, value='spring', command=self.update_cmap)
        self.antialiasing = tk.BooleanVar()
        self.antialiasing.set(True)
        self.checkbox_antialiasing = tk.Checkbutton(self, bg=bgc, fg=fgc, selectcolor=bgc, activebackground=hbgc,
                                                    activeforeground=hfgc, text='Kantenglättung', font=font_text,
                                                    variable=self.antialiasing, onvalue=True, offvalue=False,
                                                    command=self.update_antialiasing)

        self.text_coords = tk.Label(self, bg=bgc, fg=fgc, text='Koordinaten', font=font_heading)
        self.text_coords1 = tk.Label(self, bg=bgc, fg=fgc,
                                     text='c = 0.00 + 0.00i', font=font_text, anchor=tk.W)
        self.text_coords2 = tk.Label(self, bg=bgc, fg=fgc,
                                     text='Min real:\n'
                                          'Max real:\n'
                                          'Min im:\n'
                                          'Max im:', font=font_text, justify=tk.LEFT, anchor=tk.W)
        self.text_coords3 = tk.Label(self, bg=bgc, fg=fgc,
                                     text='\n\n\n', font=font_text, justify=tk.LEFT, anchor=tk.W)
        """ self.text_min_x = tk.Label(self, bg=bgc, fg=fgc,
                                   text='min. real:', font=font_text, anchor=tk.W)
        self.entry_min_x = tk.Entry(self, font=font_text, bg=bgc, fg=fgc, width=4,
                                    validate='all', validatecommand=(vcmd_neg_float, '%P'))
        self.entry_min_x.bind("<KeyRelease>", self.update_gamma)
        self.text_max_x = tk.Label(self, bg=bgc, fg=fgc,
                                   text='max. real:', font=font_text, anchor=tk.W)
        self.entry_max_x = tk.Entry(self, font=font_text, bg=bgc, fg=fgc, width=4,
                                    validate='all', validatecommand=(vcmd_neg_float, '%P'))
        self.entry_max_x.bind("<KeyRelease>", self.update_gamma)
        self.text_min_y = tk.Label(self, bg=bgc, fg=fgc,
                                   text='min. imag:', font=font_text, anchor=tk.W)
        self.entry_min_y = tk.Entry(self, font=font_text, bg=bgc, fg=fgc, width=4,
                                    validate='all', validatecommand=(vcmd_neg_float, '%P'))
        self.entry_min_y.bind("<KeyRelease>", self.update_gamma)
        self.text_max_y = tk.Label(self, bg=bgc, fg=fgc,
                                   text='max. imag:', font=font_text, anchor=tk.W)
        self.entry_max_y = tk.Entry(self, font=font_text, bg=bgc, fg=fgc, width=4,
                                    validate='all', validatecommand=(vcmd_neg_float, '%P'))
        self.entry_max_y.bind("<KeyRelease>", self.update_gamma)"""

        # button for updating the image
        """self.button_update = tk.Button(self, text='Aktualisieren',  font=('Ebrima', 10),
                                       bg=bgc, fg=fgc, command=self.master.create_image)"""
        self.button_reset = tk.Button(self, text='Zurücksetzen', font=('Ebrima', 10), bg=bgc, fg=fgc,
                                      activebackground=hbgc, activeforeground=hfgc, command=self.master.reset_image)

        self.button_export = tk.Button(self, text='Speichern', font=('Ebrima', 10), bg=bgc, fg=fgc,
                                       activebackground=hbgc, activeforeground=hfgc, command=self.master.save_image)

        self.text_background = tk.Label(self, bg=bgc, fg=fgc, text='Hintergrundbild', font=font_heading)
        self.text_width = tk.Label(self, bg=bgc, fg=fgc, text=f'Breite:', font=font_text, justify=tk.LEFT)
        self.entry_width = tk.Entry(self, font=font_text, bg=bgc, fg=fgc, width=4, selectbackground=hbgc,
                                    selectforeground=hfgc, validate='all', validatecommand=(vcmd_int, '%P'))
        self.entry_width.insert(0, str(1920))
        self.text_height = tk.Label(self, bg=bgc, fg=fgc, text=f'Höhe:', font=font_text, justify=tk.LEFT)
        self.entry_height = tk.Entry(self, font=font_text, bg=bgc, fg=fgc, width=4, selectbackground=hbgc,
                                     selectforeground=hfgc, validate='all', validatecommand=(vcmd_int, '%P'))
        self.entry_height.insert(0, str(1080))
        self.button_screenshot = tk.Button(self, text='Als Wallpaper speichern', font=('Ebrima', 10), bg=bgc, fg=fgc,
                                           activebackground=hbgc, activeforeground=hfgc,
                                           command=self.master.save_screenshot)

        self.rowconfigure(0, weight=3)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(7, weight=3)
        self.rowconfigure(17, weight=1)
        self.rowconfigure(19, weight=3)
        self.rowconfigure(21, weight=1)
        self.rowconfigure(23, weight=1)
        self.rowconfigure(25, weight=1)
        self.rowconfigure(27, weight=3)
        self.rowconfigure(29, weight=1)
        self.rowconfigure(31, weight=1)
        self.rowconfigure(50, weight=3)

        self.text_settings.grid(row=1, columnspan=4)
        self.text_maxiter.grid(row=3, columnspan=2, sticky=tk.W)
        self.entry_maxiter.grid(row=3, column=2, columnspan=2)
        self.text_gamma.grid(row=4, columnspan=2, sticky=tk.W)
        self.entry_gamma.grid(row=4, column=2, columnspan=2)
        self.button_settings_reset.grid(row=6, column=0, columnspan=2)

        self.text_colors.grid(row=8, columnspan=4)
        self.cmap_1.grid(row=10, columnspan=4, sticky=tk.W)
        self.cmap_2.grid(row=11, columnspan=4, sticky=tk.W)
        self.cmap_3.grid(row=12, columnspan=4, sticky=tk.W)
        self.cmap_4.grid(row=13, columnspan=4, sticky=tk.W)
        self.cmap_5.grid(row=14, columnspan=4, sticky=tk.W)
        self.cmap_6.grid(row=15, columnspan=4, sticky=tk.W)
        self.cmap_7.grid(row=16, columnspan=4, sticky=tk.W)
        self.checkbox_antialiasing.grid(row=18, columnspan=4, sticky=tk.W)

        self.text_coords.grid(row=20, columnspan=4)
        self.text_coords1.grid(row=22, columnspan=4, sticky=tk.W)
        self.text_coords2.grid(row=24, sticky=tk.W)
        self.text_coords3.grid(row=24, column=1, columnspan=3, sticky=tk.W)
        """self.text_min_x.grid(row=22, column=0, sticky=tk.W)
        self.entry_min_x.grid(row=22, column=1, sticky=tk.W)
        self.text_max_x.grid(row=22, column=2, sticky=tk.W)
        self.entry_max_x.grid(row=22, column=3, sticky=tk.W)
        self.text_min_y.grid(row=23, column=0, sticky=tk.W)
        self.entry_min_y.grid(row=23, column=1, sticky=tk.W)
        self.text_max_y.grid(row=23, column=2, sticky=tk.W)
        self.entry_max_y.grid(row=23, column=3, sticky=tk.W)"""

        # self.button_update.grid(row=26, column=0, columnspan=2)                  not currently used
        self.button_reset.grid(row=26, column=0, columnspan=2)
        self.button_export.grid(row=26, column=2, columnspan=2)

        self.text_background.grid(row=28, columnspan=4)
        self.text_width.grid(row=30, column=0, sticky=tk.E)
        self.entry_width.grid(row=30, column=1, sticky=tk.W)
        self.text_height.grid(row=30, column=2, sticky=tk.E)
        self.entry_height.grid(row=30, column=3, sticky=tk.W)
        self.button_screenshot.grid(row=32, columnspan=4)

    def update_maxiter(self, _event):
        if self.entry_maxiter.get() != "":
            self.master.maxiter = int(self.entry_maxiter.get())

    def update_gamma(self, _event):
        if self.entry_gamma.get() != "":
            self.master.gamma = float(self.entry_gamma.get())

    def update_cmap(self):
        self.master.cmap = plt.get_cmap(self.new_cmap.get())
        self.master.create_image()

    def update_antialiasing(self):
        self.master.antialiasing = self.antialiasing.get()
        self.master.create_image()

    def update_image(self, _event):
        self.master.create_image()


class SelectionRectangle:
    def __init__(self, master):
        self.master = master
        self.start = None
        self.rect = None
        self.relative_y = None

    def drag(self, event):
        pointer_real = self.master.master.min_x+(self.master.master.max_x-self.master.master.min_x)*event.x / \
                       self.master.master.c_width
        pointer_imaginary = self.master.master.min_y+(self.master.master.max_y -
                                                      self.master.master.min_y)*event.y/self.master.master.c_height

        if pointer_imaginary < 0:      # checks if imaginary part is negative or positive
            negative_imaginary = "+"
        else:
            negative_imaginary = "-"

        self.master.master.info_frame.text_coords1.configure(text=f"c = {pointer_real:.2f} "
                                                                  f"{negative_imaginary} {abs(pointer_imaginary):.2f}i")

        if self.start is None:
            self.start = [event.x, event.y]
            return
        if self.rect is not None:
            self.master.delete(self.rect)
        self.relative_y = self.start[1]+((event.x-self.start[0]) *
                                         (self.master.master.c_height/self.master.master.c_width))
        self.rect = self.draw(self.start, (event.x, self.relative_y))

    def release(self, event):
        self.master.delete(self.rect)
        self.rect = None
        if abs(self.start[0]-event.x) > 10:
            self.master.master.update_image(min(self.start[0], event.x), max(self.start[0], event.x),
                                            min(self.start[1], self.relative_y), max(self.start[1], self.relative_y))
        self.start = None

    def draw(self, start, end):
        return self.master.create_rectangle(*(list(start), list(end)), fill='', width=2, outline='#ffffff')


class MandelbrotMain(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        """ setting up attributes """

        self.master = master
        self.maxiter = max_iterations
        self.gamma = gamma
        self.cmap = color_map
        self.antialiasing = True
        self.drag_start = None
        self.drag_current = None

        """ setting up canvas and information panel """

        self.canvas = tk.Canvas(self, bg=bgc, highlightthickness=1, cursor='tcross')
        self.info_frame = InfoFrame(self, bg=bgc, padx=3, highlightthickness=1, highlightcolor='white')
        self.pack(side='top', fill='both', expand=True)
        self.canvas.pack(side='left', fill='both', expand='true')
        self.info_frame.pack(side='right', fill='y')

        """ setting up external methods """

        self.rectangle = SelectionRectangle(self.canvas)

        """ get window size """

        self.master.master.update_idletasks()
        self.c_width = self.canvas.winfo_width()
        self.c_height = self.canvas.winfo_height()

        """ mandelbrot images """

        self.pilimg = None
        self.img = None
        self.current_image = None

        """ imaginary plane definition """
        self.min_x = -2.5
        self.max_x = 1.5
        self.max_y = (((self.max_x-self.min_x) * self.c_height) / self.c_width)/2
        self.min_y = - (((self.max_x-self.min_x) * self.c_height) / self.c_width)/2

        """ binding tkinter events """

        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<Button-1>', self.rectangle.drag)
        self.canvas.bind('<B1-Motion>', self.rectangle.drag)
        self.canvas.bind('<ButtonRelease-1>', self.rectangle.release)
        self.canvas.bind('<Button-3>', self.m3_drag_start)
        self.canvas.bind('<B3-Motion>', self.m3_dragging)
        self.canvas.bind('<ButtonRelease-3>', self.m3_drag_stop)
        self.canvas.bind('<MouseWheel>', self.zoom)

        """ calculating the mandelbrot image """

        self.create_image()

    def create_image(self):
        """ calculating the mandelbrot image """
        self.canvas.configure(cursor='wait')
        self.update_entries()
        start_time = ti.time()
        if self.current_image is not None:
            self.canvas.delete(self.current_image)
        array = create(self.min_x, self.max_x, self.min_y, self.max_y, self.c_width, self.c_height, self.maxiter,
                       self.antialiasing) ** self.gamma
        self.pilimg = Image.fromarray(np.uint8(self.cmap(array) * 255))
        self.img = ImageTk.PhotoImage(self.pilimg)
        self.current_image = self.canvas.create_image((self.c_width / 2, self.c_height / 2), image=self.img,
                                                      state="normal")
        self.master.master.status.set(f"Rechendauer: {round(ti.time()-start_time, 2)}s")
        self.canvas.configure(cursor='tcross')

    def save_image(self):
        path = os.getcwd()+'/screenshots/mandelbrot/'
        try:
            os.makedirs(path)
        except FileExistsError:
            # directory already exists
            pass
        self.pilimg.save(path+f"mandelbrot_{self.info_frame.new_cmap.get()}"
                         f"_{self.min_x:.12f}_{self.max_x:.12f}_{-self.max_y:.12f}_{-self.min_y:.12f}.png")

    def save_screenshot(self):
        """ creates an image with the selected resolution and saves it """
        self.canvas.configure(cursor='wait')
        start_time = ti.time()
        width = int(self.info_frame.entry_width.get())
        height = int(self.info_frame.entry_height.get())
        min_x = self.min_x
        max_x = self.max_x
        mid_y = (self.min_y + self.max_y) / 2

        min_y = mid_y - (((max_x-min_x) * height) / width)/2
        max_y = mid_y + (((max_x-min_x) * height) / width)/2

        array = create(min_x, max_x, min_y, max_y, width, height, self.maxiter, self.antialiasing)
        array = array ** self.gamma
        screenshot = Image.fromarray(np.uint8(self.cmap(array) * 255))
        self.master.master.status.set(f"Rechendauer: {round(ti.time()-start_time, 2)}s")
        self.canvas.configure(cursor='tcross')
        path = os.getcwd()+'/screenshots/mandelbrot/'
        try:
            os.makedirs(path)
        except FileExistsError:
            # directory already exists
            pass
        screenshot.save(path+f"{self.info_frame.new_cmap.get()}"
                        f"_{min_x:.3f}_{max_x:.3f}_{-max_y:.3f}_{-min_y:.3f}.png")

    def update_image(self, min_x, max_x, min_y, max_y, zoom=1.0):
        """ updating coordinates for the mandelbrot image and recreating it """
        new_min_x = self.min_x+(self.max_x-self.min_x)*min_x/self.c_width
        new_max_x = self.min_x+(self.max_x-self.min_x)*max_x/self.c_width
        new_min_y = self.min_y+(self.max_y-self.min_y)*min_y/self.c_height
        new_max_y = self.min_y+(self.max_y-self.min_y)*max_y/self.c_height
        self.min_x = new_min_x*zoom
        self.max_x = new_max_x*zoom
        self.min_y = new_min_y*zoom
        self.max_y = new_max_y*zoom
        self.create_image()

    def reset_image(self):
        """ resetting the coordinates and recreating the mandelbrot image """
        self.min_x = -2.5
        self.max_x = 1.5
        mid_y = 0
        self.max_y = mid_y + (((self.max_x-self.min_x) * self.c_height) / self.c_width)/2
        self.min_y = mid_y - (((self.max_x-self.min_x) * self.c_height) / self.c_width)/2
        self.create_image()

    def reset_settings(self):
        """ resetting settings and recreating hte mandelbrot image """
        self.maxiter = max_iterations
        self.info_frame.entry_maxiter.delete(0, tk.END)
        self.info_frame.entry_maxiter.insert(0, self.maxiter)
        self.gamma = gamma
        self.info_frame.entry_gamma.delete(0, tk.END)
        self.info_frame.entry_gamma.insert(0, self.gamma)
        self.create_image()

    def update_entries(self):
        self.info_frame.text_coords3.configure(text=f'{self.min_x:.10f}\n'
                                                    f'{self.max_x:.10f}\n'
                                                    f'{-self.max_y:.10f}\n'
                                                    f'{-self.min_y:.10f}')
        """ updates coordinate entries on the info panel """
        """self.info_frame.entry_min_x.delete(0, tk.END)
        self.info_frame.entry_max_x.delete(0, tk.END)
        self.info_frame.entry_min_y.delete(0, tk.END)
        self.info_frame.entry_max_y.delete(0, tk.END)
        self.info_frame.entry_min_x.insert(0, str(round(self.min_x, 2)))
        self.info_frame.entry_max_x.insert(0, str(round(self.max_x, 2)))
        self.info_frame.entry_min_y.insert(0, str(round(self.min_y, 2)))
        self.info_frame.entry_max_y.insert(0, str(round(self.max_y, 2)))"""

    def motion(self, event):
        """ updates the coordinates on the info panel to current mouse position """
        pointer_real = self.min_x+(self.max_x-self.min_x)*event.x/self.c_width
        pointer_imaginary = self.min_y+(self.max_y-self.min_y)*event.y/self.c_height

        if pointer_imaginary < 0:      # checks if imaginary part is negative or positive
            negative_imaginary = "+"
        else:
            negative_imaginary = "-"

        self.info_frame.text_coords1.configure(text=f"c = {pointer_real:.2f} "
                                                    f"{negative_imaginary} {abs(pointer_imaginary):.2f}i")

    def m3_drag_start(self, event):
        """ sets starting point for moving the image if right mouse button is held down and dragged """
        if self.drag_start is None:
            self.drag_start = [event.x, event.y]
            self.canvas.configure(cursor='fleur')
        if self.drag_current is None:
            self.drag_current = [event.x, event.y]

    def m3_dragging(self, event):
        """ moves the image on the canvas according to the current cursor position """
        self.canvas.move(self.current_image, event.x-self.drag_current[0], event.y-self.drag_current[1])
        self.drag_current = [event.x, event.y]

    def m3_drag_stop(self, event):
        """ sets ending point for moving the image and recreates the image with new coordinates """
        if abs(event.x-self.drag_start[0])+abs(event.y-self.drag_start[1]) > 10:
            self.update_image(-(event.x-self.drag_start[0]), (self.c_width-(event.x-self.drag_start[0])),
                              -(event.y-self.drag_start[1]), (self.c_height-(event.y-self.drag_start[1])))
        self.canvas.configure(cursor='tcross')
        if self.drag_start is not None:
            self.drag_start = None
        if self.drag_current is not None:
            self.drag_current = None

    def zoom(self, event):
        """
        min_x = event.x - self.c_width / 2
        max_x = event.x + self.c_width / 2
        min_y = event.y - self.c_height / 2
        max_y = event.y + self.c_height / 2
        self.update_image(min_x, max_x, min_y, max_y, zoom)"""
        pass
