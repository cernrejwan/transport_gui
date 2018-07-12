import tkFileDialog
from Tkinter import *
from Pages import *
from Utils.OrderedDict import OrderedDict
from Utils.CSVHandler import *
import os


class ConfigsWizard(Frame):
    def __init__(self, app_manager, parent):
        Frame.__init__(self, parent)

        self.paths = csv2dict('./Data/paths.csv')
        self.configs_dict = csv2dict('./Data/default_configs.csv')

        self.app_manager = app_manager
        self.curr_page = 0

        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.navigation_header = Frame(self.container)

        self.pages = OrderedDict()
        frame = WelcomePage(parent=self.container, controller=self)
        self.pages.add("WelcomePage", frame)
        frame.grid(row=1, column=0, sticky="nsew")

        self.pages[self.curr_page].tkraise()

    def load_configs(self):
        config_file = self.pages["WelcomePage"].get_config_file()
        if config_file:
            extra_configs = csv2dict(config_file)
            self.configs_dict.update(extra_configs)

    def init_pages(self):
        self.navigation_header.grid(row=0)

        for F in [GeneralPage, SimulationPage, ShapePage, HistogramPage, StatisticsPage, SamplePage, SupportPage]:
            page_name = F.__name__
            page_short_name = page_name.split('Page')[0]
            page = F(parent=self.container, controller=self, **self.configs_dict)
            self.pages.add(page_name, page)
            Button(self.navigation_header, text=page_short_name, command=self.pages[page_name].raise_page).pack(side=LEFT)
            page.grid(row=1, column=0, sticky="nsew")

        Button(self.navigation_header, text='Summary', command=self.summarize).pack(side=LEFT)

    def set_curr_page(self, page_name):
        self.curr_page = self.pages.get_index(page_name)

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
        page.grid(row=1, column=0, sticky="nsew")

    def remove_page(self, page_name):
        if page_name in self.pages:
            self.pages.remove(page_name)

    def get_ear(self):
        return self.pages["GeneralPage"].ear.get()

    def set_ear(self, ear):
        self.pages["GeneralPage"].set_collim(ear)
        self.pages["SimulationPage"].length.set(self.configs_dict[ear + '_length'])
        self.pages["SimulationPage"].angle.set(self.configs_dict[ear + '_max_angle'])

    def get_cmd(self):
        cmds = [F.get_cmd() for F in self.pages]
        return ' '.join(cmds)

    def submit(self):
        cmd = self.get_cmd()
        iters = self.pages["StatisticsPage"].iters.get()
        output_dir = self.pages["GeneralPage"].output_dir.get()
        ear = self.pages["GeneralPage"].ear.get()

        self.navigation_header.grid_forget()

        frame = SubmitPage(self.container, self, iters)
        frame.grid(row=1, column=0, sticky="nsew")
        frame.tkraise()
        frame.update()

        frame.submit(cmd, iters, output_dir, ear)

    def summarize(self):
        for page in self.pages:
            res = page.finalize()
            if not res:
                return

        final_page = FinalPage(parent=self.container, controller=self)
        final_page.grid(row=1, column=0, sticky="nsew")
        final_page.tkraise()

        summary_window = Toplevel(self)
        SummaryWindow(summary_window, self, self.pages)

    def save_configs(self, save_path):
        configs_dict = dict()
        for F in self.pages:
            configs_dict.update(F.get_vars())
        dict2csv(configs_dict, save_path)

    def open_atob_window(self, material_name, mass, atob_var, **kwargs):
        if not mass:
            self.app_manager.raise_error_message("Must provide a material first.")
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

    def raise_error_message(self, message, title="Error!"):
        self.app_manager.raise_error_message(message, title=title)

    @staticmethod
    def save_to_csv(data_dict):
        save_path = tkFileDialog.asksaveasfilename(initialdir="~", filetypes=(("CSV", "*.csv"),))
        if not save_path.endswith('.csv'):
            save_path += '.csv'
        dict2csv(data_dict, save_path)