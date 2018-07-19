from Tkinter import *
from tkFont import Font


class CircularButton(Canvas):
    def __init__(self, parent, radius, color, text='', command=None):
        Canvas.__init__(self, parent, borderwidth=1, relief="raised", highlightthickness=0)
        self.command = command

        padding = 4
        self.circle = self.create_oval((padding, padding, radius + padding, radius + padding), width=1.5, fill=color)
        (x0, y0, x1, y1) = self.bbox("all")
        radius = (x1 - x0) + padding
        self.configure(width=radius, height=radius, relief=FLAT)
        font = Font(family='Helvetica', size=18, weight="bold")
        self.create_text(padding + radius / 2, padding + radius / 2, text=text, font=font)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.itemconfig(self.circle, outline="gray")

    def _on_release(self, event):
        self.itemconfig(self.circle, outline="black")
        if self.command is not None:
            self.command()
