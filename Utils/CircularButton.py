from Tkinter import Canvas


class CircularButton(Canvas):
    def __init__(self, parent, radius, color, command=None):
        Canvas.__init__(self, parent, borderwidth=1, relief="raised", highlightthickness=0)
        self.command = command

        padding = 4
        self.create_oval((padding, padding, radius + padding, radius + padding), outline=color, fill=color)
        (x0, y0, x1, y1) = self.bbox("all")
        radius = (x1 - x0) + padding
        self.configure(width=radius, height=radius)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.configure(relief="sunken")

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            self.command()
