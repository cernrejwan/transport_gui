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
        font = Font(family='Helvetica', weight="bold", slant="italic")

        for col, txt in enumerate(["Section", "Parameters", "cmd"]):
            Label(self.frame, text=txt, relief=RIDGE, width=int(self.widths[col]), height=3, font=font).grid(row=0, column=col)

        curr_row = 1
        for F in frames:
            num_rows = F.get_summary(self.frame, curr_row, self.widths)
            curr_row += num_rows

        buttons_frame = Frame(self.parent)
        buttons_frame.pack(side=BOTTOM)
        Button(buttons_frame, text="Save", command=self.controller.save_configs).grid(row=0, column=0)
        Button(buttons_frame, text="Exit", command=self.parent.destroy).grid(row=0, column=1)
