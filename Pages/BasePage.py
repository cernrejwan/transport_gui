from Tkinter import *
import tkFont as tkfont
from Default import default_values
import os


class BasePage(Frame):
    def __init__(self, parent, controller, title, has_prev=True):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.use = IntVar(self, 1)

        self.vars_list = list()

        self.navigation_bar = Frame(self)
        self.navigation_bar.pack(side=BOTTOM)

        if has_prev:
            self.prev_button = Button(self.navigation_bar, text="< Prev", command=self.controller.prev_frame)
            self.prev_button.pack(side=LEFT)

        self.next_button = Button(self.navigation_bar, text="Next >", command=self.controller.next_frame)
        self.next_button.pack(side=RIGHT)

        self.title = title
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        Label(self, text=title, font=self.title_font).pack(side="top", fill="x", pady=10)

        self.frame = Frame(self)

    def get_data(self):
        return ''

    def get_cmd(self):
        raise NotImplemented

    def get_vars(self):
        return {var: getattr(self, var).get() for var in self.vars_list}

    def finalize(self):
        return True

    def get_summary(self, master, row, widths):
        if not self.use.get():
            return 0

        data = self.get_data()
        if data == '':
            return 0

        num_lines = len(data.split('\n')) + 1

        Label(master, text=self.title, relief=SUNKEN, width=widths[0], height=num_lines).grid(row=row, column=0)
        Label(master, bg='white', text=data, relief=SUNKEN, width=widths[1], height=num_lines).grid(row=row, column=1)
        Label(master, bg='white', text=self.get_cmd(), relief=SUNKEN, width=widths[2], height=num_lines, wraplength=widths[2]*6).grid(row=row, column=2)
        return 1  # number of added rows

    def show(self):
        if self.use.get():
            self.frame.pack()
        else:
            self.frame.pack_forget()
