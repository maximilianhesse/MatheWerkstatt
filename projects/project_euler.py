import tkinter as tk
import sqlite3 as sql3


class EulerMain(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.master = master
        self.master.after(1, self.initialize)

    def initialize(self):
        pass


def euler_database_create():
    conn = sql3.connect('project_euler.db')


def euler_database_add():
    pass
