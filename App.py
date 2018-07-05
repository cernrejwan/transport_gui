from Tkinter import *
from tkFont import Font
import tkFileDialog
from Pages import *
from Utils.OrderedDict import OrderedDict
from Utils.CSVHandler import *
import os


class AppManager(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.paths = csv2dict('./Data/paths.csv')
        self.configs_dict = csv2dict('./Data/default_configs.csv')

        self.curr_page = 0

        self.title("Transport Simulation Wizard")

        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.pages = OrderedDict()
        frame = WelcomePage(parent=self.container, controller=self)
        self.pages.add("WelcomePage", frame)
        frame.grid(row=0, column=0, sticky="nsew")

        self.pages[self.curr_page].tkraise()

    def load_configs(self):
        config_dir = self.pages["WelcomePage"].get_submit_dir()
        if config_dir:
            config_file = os.path.join(config_dir, 'configs.csv')
            extra_configs = csv2dict(config_file)
            self.configs_dict.update(extra_configs)

    def init_pages(self):
        for F in [GeneralPage, SimuParamsPage, ShapePage, HistoPage, StatisticsPage, SamplePage, SupportMainPage]:
            frame = F(parent=self.container, controller=self, **self.configs_dict)
            self.pages.add(F.__name__, frame)
            frame.grid(row=0, column=0, sticky="nsew")

    def next_page(self):
        finalized = self.pages[self.curr_page].finalize()
        if not finalized:
            return

        if self.curr_page == 0:
            if not self.pages[0].is_watch():
                self.load_configs()
                self.init_pages()

        self.curr_page += 1
        while self.curr_page < len(self.pages) and not self.pages[self.curr_page].show_page.get():
            self.curr_page += 1

        if self.curr_page == len(self.pages):
            self.summarize()
        else:
            self.pages[self.curr_page].tkraise()

    def prev_page(self):
        self.curr_page -= 1
        while self.curr_page >= 0 and not self.pages[self.curr_page].show_page.get():
            self.curr_page -= 1

        self.pages[self.curr_page].tkraise()

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
        iters = self.pages["StatisticsPage"].iters.get()
        output_dir = self.pages["GeneralPage"].output_dir.get()
        ear = self.pages["GeneralPage"].ear.get()

        frame = SubmitPage(self.container, self, iters)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        frame.update()

        frame.submit(cmd, iters, output_dir, ear)

    def summarize(self):
        final_page = FinalPage(parent=self.container, controller=self)
        final_page.grid(row=0, column=0, sticky="nsew")
        final_page.tkraise()

        summary_window = Toplevel(self)
        SummaryWindow(summary_window, self, self.pages)

    @staticmethod
    def save_to_csv(data_dict):
        save_path = tkFileDialog.asksaveasfilename(initialdir="~", filetypes=(("CSV", "*.csv"),))
        if not save_path.endswith('.csv'):
            save_path += '.csv'
        dict2csv(data_dict, save_path)

    def save_configs(self, save_path):
        configs_dict = dict()
        for F in self.pages:
            configs_dict.update(F.get_vars())
        dict2csv(configs_dict, save_path)

    def raise_error_message(self, message, title="Error!"):
        error_window = Toplevel(self)
        title_font = Font(family='Helvetica', size=15, weight="bold", slant="italic")
        Label(error_window, text=title, font=title_font).pack(side="top", fill="x", pady=10)
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

    def get_input_files(self, input_source=None):
        if not input_source:
            input_source = self.pages['StatisticsPage'].input_source.get()
        source = 'input_fluka' if input_source == 'FLUKA' else 'input_mcnp'
        ls = os.listdir(self.paths[source])
        input_files = [os.path.join(self.paths[source], f) for f in ls if f.endswith('_')]
        return sorted(input_files)


if __name__ == "__main__":
    app = AppManager()
    app.mainloop()
