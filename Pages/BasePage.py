from Tkinter import *
import tkFont as tkfont
import os


class BasePage(Frame):
    def __init__(self, parent, controller, title, has_prev=True):
        Frame.__init__(self, parent)
        self.page_name = self.__class__.__name__
        self.parent = parent
        self.controller = controller
        self.show_page = IntVar(self, 1)

        self.vars_list = list()

        self.navigation_bar = Frame(self)
        self.navigation_bar.pack(side=BOTTOM)

        if has_prev:
            self.prev_button = Button(self.navigation_bar, text="< Prev", command=self.controller.prev_page)
            self.prev_button.pack(side=LEFT)

        txt, cmd = self.get_next_button()
        self.next_button = Button(self.navigation_bar, text=txt, command=cmd)
        self.next_button.pack(side=RIGHT)

        self.title = title
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        Label(self, text=title, font=self.title_font).pack(side="top", fill="x", pady=10)

        self.frame = Frame(self)
        self.frame.pack()

    def get_next_button(self):
        return 'Next >', self.controller.next_page

    def get_data(self):
        return ''

    def get_cmd(self):
        return ''

    def get_vars_list(self):
        return self.vars_list

    def get_vars(self):
        if not self.show_page.get():
            return {}

        vars_list = self.get_vars_list()
        return {var: getattr(self, var).get() for var in vars_list}

    def finalize(self):
        return True

    def switch(self, bit):
        self.show_page.set(bit)
