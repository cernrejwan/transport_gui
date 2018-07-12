from Tkinter import *
from tkFont import Font
import tkFileDialog
from ConfigsWizard import ConfigsWizard
from JobsInspector import JobsInspector


txt = """Welcome to the transport simulation configuration tool!
Use it to launch a simulation, check its status or view its output.
What would you like to do?"""


class AppManager(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Transport Simulation")

        self.title_font = Font(family='Helvetica', size=18, weight="bold", slant="italic")
        Label(self, text='Welcome!', font=self.title_font).pack(side="top", fill="x", pady=10)

        Label(self, text=txt, justify=LEFT).pack()
        Button(self, text='Launch simulation', command=lambda: self.launch(ConfigsWizard)).pack()
        Button(self, text='Check status', command=lambda: self.launch(JobsInspector)).pack()

    def raise_error_message(self, message, title="Error!"):
        error_window = Toplevel(self)
        Label(error_window, text=title, font=self.title_font).pack(side="top", fill="x", pady=10)
        Label(error_window, text=message).pack()
        Button(error_window, text="OK", command=error_window.destroy).pack(side=BOTTOM)

    @staticmethod
    def open_file_dialog(var, file_type, initialdir="~"):
        if file_type == 'dir':
            filename = tkFileDialog.askdirectory(initialdir=initialdir, title="Select directory")
        else:
            filename = tkFileDialog.askopenfilename(initialdir=initialdir, title="Select file",
                                                    filetypes=((file_type + " files", "*." + file_type), ("All files", "*.*")))
        var.set(filename)

    def launch(self, cls):
        window = Toplevel(self)
        frame = cls(self, window)
        frame.pack()


if __name__ == "__main__":
    app = AppManager()
    app.mainloop()