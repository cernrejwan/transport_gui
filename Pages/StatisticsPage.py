from BasePage import *


class StatisticsPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Statistics")

        # vars:
        self.vars_list = ['iters', 'input_source']
        self.input_source = StringVar(self, kwargs['input_source'])
        self.max_iters = IntVar(self, len(self.controller.get_input_files(self.input_source.get())))
        self.num_prelim = StringVar(self, self.get_num_prelim(self.input_source.get()))
        self.iters = IntVar(self, int(kwargs.get('iters', 2)))

        # gui
        Label(self.frame, text="Select input files source:").grid(row=0, column=0)
        OptionMenu(self.frame, self.input_source, *["FLUKA", "FLUKA + MCNP"], command=self.set_source).grid(row=0, column=1)
        Label(self.frame, text="Number of available source files:").grid(row=1, column=0)
        Label(self.frame, textvariable=self.max_iters).grid(row=1, column=1)
        Label(self.frame, text='Number of preliminaries in each file:').grid(row=2, column=0)
        Label(self.frame, textvariable=self.num_prelim).grid(row=2, column=1)
        Label(self.frame, text="Number of files for statistics:").grid(row=3, column=0)
        Entry(self.frame, textvariable=self.iters).grid(row=3, column=1)

    def get_data(self):
        data = 'Input files source: ' + self.input_source.get()
        data += '\nNumber of statistics: ' + str(self.iters.get())
        return data

    def set_source(self, source):
        self.max_iters.set(len(self.controller.get_input_files(source)))
        self.num_prelim.set(self.get_num_prelim(source))

    def finalize(self):
        if self.iters.get() not in range(2, self.max_iters.get() + 1):
            self.controller.raise_error_message('Number of files for statistics must be between 2 and ' + str(self.max_iters.get()))
            return False
        return True

    @staticmethod
    def get_num_prelim(source):
        return '1e9' if source == 'FLUKA' else '2e8'
