from Tkinter import *
from tkFont import Font
import tkFileDialog
from Default import *
from Pages import *
from Utils.OrderedDict import OrderedDict


class AppManager(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.curr_frame = 0

        self.title("Transport Simulation Wizard")
        self.ear = StringVar(self, "EAR1")
        self.use_default = IntVar(self, 0)

        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.frames = OrderedDict()
        for F in [WelcomePage, SimuParamsPage, ShapePage, HistoPage, SamplePage, SupportMainPage]:
            frame = F(parent=self.container, controller=self)
            self.frames.add(frame)
            frame.grid(row=0, column=0, sticky="nsew")

        self.frames[self.curr_frame].tkraise()

    def next_frame(self):
        finalized = self.frames[self.curr_frame].finalize()
        if not finalized:
            return

        self.curr_frame += 1
        if self.use_default.get() or self.curr_frame == len(self.frames):
            self.summarize()
        else:
            self.frames[self.curr_frame].tkraise()

    def prev_frame(self):
        self.curr_frame -= 1
        self.frames[self.curr_frame].tkraise()

    def add_page(self, page):
        self.frames.add(page)
        page.grid(row=0, column=0, sticky="nsew")

    def add_page_if_not_exists(self, page_name):
        if page_name in self.frames:
            return

        cls = eval(page_name)
        frame = cls(parent=self.container, controller=self)
        self.frames.add(frame)
        frame.grid(row=0, column=0, sticky="nsew")

    def remove_page_by_name(self, page_name):
        self.frames.remove(page_name)

    def remove_page_by_value(self, page):
        self.frames.remove(page)

    def set_ear(self, ear):
        self.frames[0].set_collim(ear)
        ear_values = default_values[self.ear.get()]
        self.frames[1].length.set(ear_values['-L'])

    def get_cmd(self):
        cmds = [F.get_cmd() for F in self.frames]
        return ' '.join(cmds)

    def submit(self):
        cmd = self.get_cmd()
        iters = self.frames[3].iters.get()
        output = '''
for i in `seq 1 {iters}` ;
do
/eos/experiment/ntof/simul/transport/transport -d /afs/cern.ch/exp/ntof/simulations/FLUKA_spallation/${{i}}/EAR2.smooth {cmd}
done
        '''.format(iters=iters, cmd=cmd)

        return output

    def summarize(self):
        final_page = FinalPage(self.container, self)
        self.frames.add(final_page)
        final_page.grid(row=0, column=0, sticky="nsew")
        final_page.tkraise()

        summary_window = Toplevel(self)
        summary = SummaryWindow(summary_window, self)
        master = summary.frame
        curr_row = 1
        for F in self.frames:
            num_rows = F.get_summary(master, curr_row, summary.widths)
            curr_row += num_rows

        Button(summary_window, text="OK", command=summary_window.destroy).pack(side=BOTTOM)

    def raise_error_message(self, message):
        error_window = Toplevel(self)
        title_font = Font(family='Helvetica', size=15, weight="bold", slant="italic")
        Label(error_window, text='Error!', font=title_font).pack(side="top", fill="x", pady=10)
        Label(error_window, text=message).pack()
        Button(error_window, text="OK", command=error_window.destroy).pack(side=BOTTOM)

    @staticmethod
    def open_file_dialog(var, file_type):
        if file_type == 'dir':
            filename = tkFileDialog.askdirectory(initialdir="/", title="Select directory")
        else:
            filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                    filetypes=((file_type + " files", "*." + file_type), ("All files", "*.*")))
        var.set(filename)


if __name__ == "__main__":
    app = AppManager()
    app.mainloop()
