import tkinter as tk
import random as rd
import codecs as co
import pathlib as pl
import datetime as dt
import time as ti
import projects as pj
import sys as sys
import config as cfg

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
"""                                                 classes                                                          """
"""                                                                                                                  """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class MenuBar(tk.Menu):
    def __init__(self, master, *args, **kwargs):
        tk.Menu.__init__(self, master, bg=bgc, fg=fgc, activebackground=hbgc, activeforeground=hfgc, *args, **kwargs)
        self.master = master

        self.file_menu = MenuItem(self, tearoff=0)                           # creation of file menu cascade
        self.file_menu.add_command(label="Öffnen")
        self.file_menu.add_command(label="Speichern")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Beenden", command=quit)
        self.add_cascade(label="Datei", menu=self.file_menu)

        self.project_menu = MenuItem(self, tearoff=0)                        # creation of project menu cascade
        self.project_menu.add_command(label="Mandelbrot", command=self.mandelbrot)
        self.project_menu.add_command(label="Sieb des Erathostenes", command=self.erathostenes)
        self.add_cascade(label="Projekte", menu=self.project_menu)

        self.help_menu = MenuItem(self, tearoff=0)                           # creation of help menu cascade
        self.help_menu.add_command(label="Über", command=self.about)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="Einstellungen")
        self.add_cascade(label="Hilfe", menu=self.help_menu)

    def about(self):
        last_modification = dt.datetime.fromtimestamp(pl.Path("main.py").stat().st_mtime)

        new = tk.Frame(self.master.main, bg=bgc, highlightthickness=1, highlightcolor=fgc)
        top = tk.Label(new, text="Mathe Werkstatt", bg=bgc, fg=fgc, font=('Ebrima', 34, 'bold'))
        logo = tk.PhotoImage(file='logo.gif')
        label_logo = tk.Label(new, image=logo, bg=bgc)
        label_logo.image = logo
        left1 = tk.Label(new, text="Erstellt von:", bg=bgc, fg=fgc, font=font_text, justify='left')
        right1 = tk.Label(new, text="Maximilian Hesse", bg=bgc, fg=fgc, font=font_text, justify='left')
        left2 = tk.Label(new, text="E-Mail:", bg=bgc, fg=fgc, font=font_text, justify='left')
        right2 = tk.Label(new, text="maximilian.hesse@uni-oldenburg.de", bg=bgc, fg=fgc, font=font_text,
                          justify='left')
        left3 = tk.Label(new, text="Letztes Update:", bg=bgc, fg=fgc, font=font_text, justify='left')
        right3 = tk.Label(new, text=str(last_modification), bg=bgc, fg=fgc, font=font_text, justify='left')
        left4 = tk.Label(new, text="Erstellt mit:", bg=bgc, fg=fgc, font=font_text, justify='left')
        right4 = tk.Label(new, text="PyCharm (Community Edition)", bg=bgc, fg=fgc, font=font_text, justify='left')
        left5 = tk.Label(new, text="Python Version:", bg=bgc, fg=fgc, font=font_text, justify='left')
        right5 = tk.Label(new, text=f"{sys.version_info[0]}.{sys.version_info[1]}", bg=bgc, fg=fgc,
                          font=font_text, justify='left')
        left6 = tk.Label(new, text="Lizenz:", bg=bgc, fg=fgc, font=font_text, justify='left')
        right6 = tk.Label(new, text="Freeware für nicht-kommerziellen Einsatz", bg=bgc, fg=fgc, font=font_text,
                          justify='left')

        top.grid(row=1, column=5, columnspan=3, sticky=tk.NW)
        label_logo.grid(row=1, column=1, rowspan=7, sticky=tk.S)
        left1.grid(row=2, column=5, sticky=tk.NW)
        right1.grid(row=2, column=6, sticky=tk.NW)
        left2.grid(row=3, column=5, sticky=tk.NW)
        right2.grid(row=3, column=6, sticky=tk.NW)
        left3.grid(row=4, column=5, sticky=tk.NW)
        right3.grid(row=4, column=6, sticky=tk.NW)
        left4.grid(row=5, column=5, sticky=tk.NW)
        right4.grid(row=5, column=6, sticky=tk.NW)
        left5.grid(row=6, column=5, sticky=tk.NW)
        right5.grid(row=6, column=6, sticky=tk.NW)
        left6.grid(row=7, column=5, sticky=tk.NW)
        right6.grid(row=7, column=6, sticky=tk.NW)

        self.master.main.del_current()
        self.master.main.recreate_current(new)

        self.master.main.current.columnconfigure(0, weight=1)
        self.master.main.current.rowconfigure(0, weight=1)
        self.master.main.current.columnconfigure(20, weight=1)
        self.master.main.current.rowconfigure(20, weight=1)

    def change_fact(self):
        self.master.status.change_fact()

    def mandelbrot(self):
        self.master.main.del_current()
        new = pj.mandelbrot.MandelbrotMain(self.master.main, bg=bgc)
        self.master.main.recreate_current(new)

    def erathostenes(self):
        self.master.main.del_current()
        new = pj.erathostenes.ErathostenesMain(self.master.main, bg=bgc)
        self.master.main.recreate_current(new)


class MenuItem(tk.Menu):
    def __init__(self, master, description='', *args, **kwargs):
        tk.Menu.__init__(self, master, bg=bgc, fg=fgc, activebackground=hbgc, activeforeground=hfgc, *args, **kwargs)
        self.master = master
        self.description = description


class StatusBar(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        self.status = tk.Label(self, text='', bg=bgc, fg=fgc)
        self.status.pack(side='left')
        self.clock = tk.Label(self, text='', bg=bgc, fg=fgc)
        self.clock.pack(side='right')
        self.clock_tick()
        self.fact = tk.Label(self, text='', bg=bgc, fg=fgc)
        self.fact.pack(side='right', fill='x', expand=True)
        self.fact.bind("<Button-1>", self.change_fact)
        self.factnr = 0
        self.change_fact()

    def set(self, text):
        self.status.config(text=text)

    def clear(self):
        self.status.config(text="")

    def change_fact(self, *args):
        print(str(*args))
        with co.open("mathfacts.txt", "r", "utf-8") as mf:
            math_facts = [line.rstrip('\n') for line in mf]
        prior_fact = self.factnr
        while self.factnr == prior_fact:
            self.factnr = rd.randint(1, len(math_facts))
        self.fact.configure(text=f'Zufälliger Mathe-Fact #{self.factnr}: {math_facts[self.factnr - 1]}')

    def clock_tick(self):
        self.clock.config(text=ti.strftime('%H:%M:%S'))
        self.after(1000, self.clock_tick)


class Main(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.current = tk.Frame(self, bg=bgc)
        self.current.pack(side="top", fill="both", expand=True)

    def del_current(self):
        self.master.status.set('')
        self.current.pack_forget()
        self.current.destroy()

    def recreate_current(self, new):
        self.current = new
        self.current.pack(side="top", fill="both", expand=True)


class MainApp(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        self.menu = MenuBar(self)
        self.main = Main(self, bg=bgc)
        self.status = StatusBar(self, bg=bgc, highlightthickness=1, highlightcolor=fgc)

        self.master.config(menu=self.menu)
        self.main.pack(side="top", fill="both", expand=True)
        self.status.pack(side="bottom", fill="x")

        self.menu.about()
        self.master.title("Mathe Werkstatt")
        self.status.set('Mathe Werkstatt initialisiert...')
        self.master.bind('<Escape>', quit)


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    MainApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
