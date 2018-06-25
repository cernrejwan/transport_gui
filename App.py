from Tkinter import *
from tkFont import Font
import tkFileDialog
from Default import *
from Pages import *
from Utils.OrderedDict import OrderedDict
import pandas as pd


class AppManager(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.curr_frame = 0

        self.title("Transport Simulation Wizard")
        self.ear = StringVar(self, "EAR1")

        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.frames = OrderedDict()
        frame = WelcomePage(parent=self.container, controller=self)
        self.frames.add("WelcomePage", frame)
        frame.grid(row=0, column=0, sticky="nsew")

        self.frames[self.curr_frame].tkraise()

    def load_configs(self):
        config_file = self.frames["WelcomePage"].get_config_file()
        if not config_file:
            return default_values

        configs_dict = pd.read_csv(config_file, index_col=0, squeeze=True).to_dict()
        return configs_dict

    def next_frame(self):
        finalized = self.frames[self.curr_frame].finalize()
        if not finalized:
            return

        if self.curr_frame == 0:
            configs_dict = self.load_configs()

            for F in [GeneralPage, SimuParamsPage, ShapePage, HistoPage, SamplePage, SupportMainPage]:
                frame = F(parent=self.container, controller=self)
                self.frames.add(F.__name__, frame)
                frame.grid(row=0, column=0, sticky="nsew")

        self.curr_frame += 1
        if self.curr_frame == len(self.frames): # or self.use_default.get()
            self.summarize()
        else:
            self.frames[self.curr_frame].tkraise()

    def prev_frame(self):
        self.curr_frame -= 1
        self.frames[self.curr_frame].tkraise()

    def add_page(self, page_name, count=1):
        if "FinalPage" in self.frames:
            self.remove_page("FinalPage")

        for i in range(count):
            cls = eval(page_name)
            page = cls(parent=self.container, controller=self, index=i+1)
            index = str(i+1) if count > 1 else ''
            self.frames.add(page_name + index, page)
            page.grid(row=0, column=0, sticky="nsew")

    def remove_page(self, page_name, count=1):
        for i in range(count):
            index = str(i + 1) if count > 1 else ''
            self.frames.remove(page_name + index)

    def set_ear(self, ear):
        self.frames["GeneralPage"].set_collim(ear)
        ear_values = default_values[self.ear.get()]
        self.frames["SimuParamsPage"].length.set(ear_values['-L'])
        self.frames["SimuParamsPage"].angle.set(ear_values['-a'])

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
        self.frames.add("FinalPage", final_page)
        final_page.grid(row=0, column=0, sticky="nsew")
        final_page.tkraise()

        summary_window = Toplevel(self)
        SummaryWindow(summary_window, self, self.frames)

    def save_configs(self):
        save_path = tkFileDialog.asksaveasfilename(initialdir="~", filetypes=(("CSV", "*.csv"),))
        if not save_path.endswith('.csv'):
            save_path += '.csv'

        configs_dict = dict()
        for F in self.frames:
            configs_dict.update(F.get_vars())

        pd.Series(configs_dict).to_csv(save_path)

    def raise_error_message(self, message):
        error_window = Toplevel(self)
        title_font = Font(family='Helvetica', size=15, weight="bold", slant="italic")
        Label(error_window, text='Error!', font=title_font).pack(side="top", fill="x", pady=10)
        Label(error_window, text=message).pack()
        Button(error_window, text="OK", command=error_window.destroy).pack(side=BOTTOM)

    @staticmethod
    def open_file_dialog(var, file_type):
        if file_type == 'dir':
            filename = tkFileDialog.askdirectory(initialdir="~", title="Select directory")
        else:
            filename = tkFileDialog.askopenfilename(initialdir="~", title="Select file",
                                                    filetypes=((file_type + " files", "*." + file_type), ("All files", "*.*")))
        var.set(filename)


if __name__ == "__main__":
    app = AppManager()
    app.mainloop()
