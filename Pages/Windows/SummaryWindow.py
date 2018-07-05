from Tkinter import *
from tkFont import Font


class SummaryWindow:
    def __init__(self, parent, controller, frames):
        self.parent = parent
        self.controller = controller

        title_font = Font(family='Helvetica', size=15, weight="bold", slant="italic")
        Label(self.parent, text='Summary', font=title_font).pack(side="top", fill="x", pady=10)

        self.widths = [18, 40, 60]

        self.frame = Frame(self.parent)
        self.frame.pack()
        font = Font(weight="bold", slant="italic") # family='Helvetica',

        for col, txt in enumerate(["Section", "Parameters", "cmd"]):
            Label(self.frame, text=txt, relief=RIDGE, width=int(self.widths[col]), height=3, font=font).grid(row=0, column=col)

        curr_row = 1
        for F in frames:
            num_rows = self.get_summary(curr_row, F.get_data(), F.title, F.get_cmd())
            curr_row += num_rows

        Button(self.parent, text="Exit", command=self.parent.destroy).pack(side=BOTTOM)

    def get_summary(self, row, data, title, cmd):
        if not data:
            return 0

        num_lines = len(data.split('\n')) + 1

        Label(self.frame, text=title, relief=SUNKEN, width=self.widths[0], height=num_lines).grid(row=row, column=0)
        text_data = Text(self.frame, height=num_lines, width=self.widths[1])
        text_data.insert(INSERT, data)
        text_data.grid(row=row, column=1)

        text_cmd = Text(self.frame, height=num_lines, width=self.widths[2], wrap=CHAR)
        text_cmd.insert(INSERT, cmd)
        text_cmd.grid(row=row, column=2)

        return 1  # number of added rows
