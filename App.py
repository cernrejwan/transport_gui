from Tkinter import *
from tkFont import Font
import tkFileDialog
from Pages import *
from Utils.OrderedDict import OrderedDict
from Utils.FileReader import *
import os


class AppManager(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.paths = csv2dict('./Data/paths.csv')
        self.configs_dict = csv2dict('./Data/default_configs.csv')

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
            extra_configs = csv2dict(config_file)
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

        if self.curr_frame == len(self.pages):
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
        iters = self.pages["HistoPage"].iters.get()
        output_dir = self.pages["GeneralPage"].output_dir.get()

        submit_dir = os.path.join(output_dir, "submit")
        if os.path.exists(submit_dir):
            ls = os.listdir(output_dir)
            ls = [int(f.split('_')[1]) for f in ls if f.startswith('submit_')]
            idx = '2' if not ls else max(ls) + 1
            submit_dir = os.path.join(output_dir, 'submit_' + str(idx))
            self.raise_error_message(
                "'submit' folder already exists in output directory.\nCreating folder 'submit_{}' instead.".format(idx))
        os.mkdir(submit_dir)

        for i in range(iters):
            job_file = os.path.join(submit_dir, 'job_{}.sh'.format(i))
            input_file = os.path.join(self.paths['transport_files'], str(i), self.pages["GeneralPage"].ear.get())
            output_file = os.path.join(submit_dir, 'res_{}'.format(i))
            out = self.paths['transport_simulation_code'] + ' -d ' + input_file + ' -o ' + output_file + cmd
            with open(job_file, 'w') as f:
                f.write(out)
            os.system('HTCondorSub.sh ' + job_file)

        frame = SubmitPage(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

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

    def save_configs(self):
        configs_dict = dict()
        for F in self.pages:
            configs_dict.update(F.get_vars())

        self.save_to_csv(configs_dict)

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
