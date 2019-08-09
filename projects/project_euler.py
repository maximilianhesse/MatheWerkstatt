import tkinter as tk
import sqlite3 as sql3
import config as cfg


class EulerMain(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        # initialization of attributes
        self.master = master
        self.width = None
        self.height = None
        self.num_frame_container = None
        self.num_frame = None
        self.left_button = None
        self.right_button = None
        self.num_label = None
        self.num_entry = None
        self.problem_frame = None
        self.problem_label = None
        self.code_frame = None
        self.code_text = None

        # connection to database
        self.conn = sql3.connect(':memory:')
        self.c = self.conn.cursor()
        self.database_create()
        self.database_add()
        self.conn.commit()

        # create a list of all problem-numbers
        self.nums = None
        self.create_num_list()

        # creating attributes for current problem and fetching first problem
        self.num = self.nums[0]
        self.problem = None
        self.code = None
        self.solution_code = None
        self.solution = None
        self.fetch_current()

        # initialization of stuff that depends on window size
        self.master.after(1, self.initialize)

    def initialize(self):

        # initializing the UI
        self.num_frame_container = tk.Frame(self, bg=cfg.bgc, highlightthickness=1)
        self.num_frame = tk.Frame(self.num_frame_container, bg=cfg.bgc)
        self.left_button = tk.Button(self.num_frame, text="Vorheriges Problem", command=self.previous)
        self.right_button = tk.Button(self.num_frame, text="Nächstes Problem", command=self.next)
        self.num_label = tk.Label(self.num_frame, text="Problem:", font=cfg.font_text, bg=cfg.bgc, fg=cfg.fgc,
                                  justify=tk.LEFT)
        self.num_entry = tk.Label(self.num_frame, text=self.num, font=cfg.font_text, bg=cfg.bgc, fg=cfg.fgc,
                                  justify=tk.LEFT)

        self.problem_frame = tk.Frame(self, bg=cfg.bgc, highlightthickness=1)
        self.problem_label = tk.Label(self.problem_frame, text=self.problem, font=cfg.font_text, bg=cfg.bgc, fg=cfg.fgc,
                                      justify=tk.LEFT, wraplength=self.winfo_width()-10)

        self.code_frame = tk.Frame(self, bg=cfg.bgc, highlightthickness=1, padx=10, pady=10)
        self.code_text = tk.Text(self.code_frame, font=cfg.font_text, bg=cfg.bgc, fg=cfg.fgc, relief=tk.FLAT,
                                 selectforeground=cfg.hfgc, selectbackground=cfg.hbgc, undo=True)
        self.code_text.insert(tk.END, self.code)

        # displaying the UI
        self.num_frame_container.pack(side=tk.TOP, fill=tk.X)
        self.num_frame.pack(anchor=tk.CENTER)
        self.left_button.pack(side=tk.LEFT)
        self.num_label.pack(side=tk.LEFT)
        self.num_entry.pack(side=tk.LEFT)
        self.right_button.pack(side=tk.LEFT)

        self.problem_frame.pack(side=tk.TOP, fill=tk.X)
        self.problem_label.pack(anchor=tk.CENTER)

        self.code_frame.pack(side=tk.TOP, fill=tk.X)
        self.code_text.pack(side=tk.TOP, fill=tk.X)

    def update_page(self):
        self.num_entry.config(text=self.num)
        self.problem_label.config(text=self.problem)

    def create_num_list(self):
        nums = self.c.execute("SELECT num FROM problems").fetchall()
        self.nums = [nums[i][0] for i in range(len(nums))]
        self.nums.sort()

    def fetch_current(self):
        """ sets main classes attributes problem, code and solution to the current problems number """
        row = self.c.execute("SELECT * FROM problems WHERE num=?", (self.num,)).fetchone()
        self.problem = row[1]
        self.code = row[2]
        self.solution_code = row[3]
        self.solution = row[4]

    def database_create(self):
        self.c.execute("""CREATE TABLE problems (
            num integer,
            problem text,
            code text,
            solution_code text,
            solution float        
        )""")

    def database_add(self):
        self.c.execute("INSERT INTO problems VALUES (1, 'Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1, Das ist der Problemtext von Problem 1',"
                       "'Beispielcode Problem 1', 'Das ist der Lösungscode von Problem 1', 111.1)")
        self.c.execute("INSERT INTO problems VALUES (5, 'Das ist der Problemtext von Problem 5',"
                       "'Beispielcode Problem 5', 'Das ist der Lösungscode von Problem 5', 555.5)")
        self.c.execute("INSERT INTO problems VALUES (2, 'Das ist der Problemtext von Problem 2',"
                       "'Beispielcode Problem 2', 'Das ist der Lösungscode von Problem 2', 222.2)")
        self.c.execute("INSERT INTO problems VALUES (3, 'Das ist der Problemtext von Problem 3',"
                       "'Beispielcode Problem 3', 'Das ist der Lösungscode von Problem 3', 333.3)")

    def previous(self):
        """ swaps to the previous problem or to the last if you are at the first problem """
        i = self.nums.index(self.num)
        if i == 0:
            self.num = self.nums[-1]
        else:
            self.num = self.nums[i-1]
        self.fetch_current()
        self.update_page()

    def next(self):
        """ swaps to the next problem or to the first if you are at the last problem """
        i = self.nums.index(self.num)
        if i == len(self.nums)-1:
            self.num = self.nums[0]
        else:
            self.num = self.nums[i+1]
        self.fetch_current()
        self.update_page()

