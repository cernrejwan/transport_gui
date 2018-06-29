from Tkinter import *
from tkFont import Font
import tkFileDialog
from Pages import *
from Utils.OrderedDict import OrderedDict
import pandas as pd


class AppManager(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.paths = pd.read_csv('./Data/paths.csv', index_col=0, header=None, squeeze=True).to_dict()
        self.configs_dict = pd.read_csv('./Data/default_configs.csv', index_col=0, header=None, squeeze=True).to_dict()

        self.curr_frame = 0

        self.title("Transport Simulation Wizard")

        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.pages = OrderedDict()
        frame = WelcomePage(parent=self.container, controller=self)
        self.pages.add("WelcomePage", frame)
        frame.grid(row=0, column=0, sticky="nsew")

        self.pages[self.curr_frame].tkraise()

    def load_configs(self):
        config_file = self.pages["WelcomePage"].get_config_file()
        if config_file:
            extra_configs = pd.read_csv(config_file, index_col=0, header=None, squeeze=True).to_dict()
            self.configs_dict.update(extra_configs)

    def init_pages(self):
        for F in [GeneralPage, SimuParamsPage, ShapePage, HistoPage, SamplePage, SupportMainPage]:
            frame = F(parent=self.container, controller=self, **self.configs_dict)
            self.pages.add(F.__name__, frame)
            frame.grid(row=0, column=0, sticky="nsew")

    def next_page(self):
        finalized = self.pages[self.curr_frame].finalize()
        if not finalized:
            return

        if self.curr_frame == 0:
            self.load_configs()
            self.init_pages()

        self.curr_frame += 1
        while self.curr_frame < len(self.pages) and not self.pages[self.curr_frame].show_page.get():
            self.curr_frame += 1

        if self.curr_frame == len(self.pages): # or self.use_default.get()
            self.summarize()
        else:
            self.pages[self.curr_frame].tkraise()

    def prev_page(self):
        self.curr_frame -= 1
        while self.curr_frame >= 0 and not self.pages[self.curr_frame].show_page.get():
            self.curr_frame -= 1

        self.pages[self.curr_frame].tkraise()

    def switch_page(self, page_name, bit):
        self.pages[page_name].switch(bit)

    def add_page(self, cls, page_name, **kwargs):
        page = cls(parent=self.container, controller=self, **kwargs)
        self.pages.add(page_name, page)
        page.grid(row=0, column=0, sticky="nsew")

    def remove_page(self, page_name):
        if page_name in self.pages:
            self.pages.remove(page_name)

    def get_ear(self):
        return self.pages["GeneralPage"].ear.get()

    def set_ear(self, ear):
        self.pages["GeneralPage"].set_collim(ear)
        self.pages["SimuParamsPage"].length.set(self.configs_dict[ear + '_length'])
        self.pages["SimuParamsPage"].angle.set(self.configs_dict[ear + '_max_angle'])

    def get_cmd(self):
        cmds = [F.get_cmd() for F in self.pages]
        return ' '.join(cmds)

    def submit(self):
        cmd = self.get_cmd()
        iters = self.pages[3].iters.get()
        output = '''
for i in `seq 1 {iters}` ;
do
/eos/experiment/ntof/simul/transport/transport -d /afs/cern.ch/exp/ntof/simulations/FLUKA_spallation/${{i}}/EAR2.smooth {cmd}
done
        '''.format(iters=iters, cmd=cmd)

        return output

    def summarize(self):
        final_page = FinalPage(parent=self.container, controller=self)
        final_page.grid(row=0, column=0, sticky="nsew")
        final_page.tkraise()

        summary_window = Toplevel(self)
        SummaryWindow(summary_window, self, self.pages)

    @staticmethod
    def save_df(df):
        save_path = tkFileDialog.asksaveasfilename(initialdir="~", filetypes=(("CSV", "*.csv"),))
        if not save_path.endswith('.csv'):
            save_path += '.csv'
        df.to_csv(save_path)

    def save_configs(self):
        configs_dict = dict()
        for F in self.pages:
            configs_dict.update(F.get_vars())

        configs_df = pd.Series(configs_dict)
        self.save_df(configs_df)

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

    def open_atob_window(self, material_name, mass, atob_var, **kwargs):
        if not mass:
            self.raise_error_message("Must provide a material first.")
            return
        new_window = Toplevel(self)
        atob_calculator = AtobCalculator(new_window, self, material_name, mass, atob_var, **kwargs)
        atob_calculator.pack()


if __name__ == "__main__":
    app = AppManager()
    app.mainloop()
