from Tkinter import *
from tkFont import Font


class SummaryWindow:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

        title_font = Font(family='Helvetica', size=15, weight="bold", slant="italic")
        Label(self.parent, text='Summary', font=title_font).pack(side="top", fill="x", pady=10)

        self.widths = [15, 30, 50]

        self.frame = Frame(self.parent)
        self.frame.pack()
        font = Font(family='Helvetica', weight="bold", slant="italic")
        myLabel = lambda col, txt: Label(self.frame, text=txt, relief=RIDGE, width=int(self.widths[col]),
                                         height=3, font=font).grid(row=0, column=col)

        myLabel(0, "Section")
        myLabel(1, "Parameters")
        myLabel(2, "cmd")