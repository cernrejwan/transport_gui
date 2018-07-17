import tkFileDialog
from Tkinter import *
from subprocess import Popen, PIPE
from tkFont import Font
from Widgets import *

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
        Button(self, text='Create plots', command=lambda: self.launch(Averager)).pack()
        Button(self, text='Exit', command=self.destroy).pack()

    def raise_error_message(self, message, title="Error!"):
        error_window = Toplevel(self)
        Label(error_window, text=title, font=self.title_font).pack(side="top", fill="x", pady=10)
        Label(error_window, text=message).pack()
        Button(error_window, text="OK", command=error_window.destroy).pack(side=BOTTOM)

    @staticmethod
    def open_file_dialog(var, file_type, initialdir="~"):
        initialdir = var.get() if var.get() else initialdir
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

    def get_condor_q(self):
        q = self.system(['condor_q', '-wide'])
        if 'failed' in q.lower():
            self.raise_error_message("Unfortunately, HTCondor is not available at the moment.\nPlease try again later.\nDon't worry, all your data is saved in the submit directory.")
            return None
        return q

    @staticmethod
    def system(cmd):
        print(' '.join(cmd))
        out = Popen(cmd, stdout=PIPE).communicate()[0]
        print(out)
        return out


if __name__ == "__main__":
    app = AppManager()
    app.mainloop()
