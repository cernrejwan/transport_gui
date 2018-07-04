from BasePage import *
from Utils.CSVHandler import read_histogram_menus


class HistoPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Histogram")

        # vars:
        self.vars_list = ['histogram_dim', 'histogram_type', 'bins_x', 'min_x', 'max_x']
        self.histogram_dim = StringVar(self, kwargs['histogram_dim'])
        self.menus = read_histogram_menus(self.controller.paths['histogram_menus_path'])
        curr_menu = self.get_menu_for_dim(self.histogram_dim.get())
        self.histogram_type = StringVar(self, kwargs.get('histogram_type', curr_menu[0]))

        self.bins_x = IntVar(self, kwargs['bins_x'])
        self.bins_y = IntVar(self, kwargs['bins_y'])
        self.iters = IntVar(self, int(kwargs.get('iters', 1)))
        self.max_iters = len(self.controller.get_input_dirs())
        self.min_x = StringVar(self, kwargs['min_x'])
        self.max_x = StringVar(self, kwargs['max_x'])
        self.min_y = StringVar(self, kwargs['min_y'])
        self.max_y = StringVar(self, kwargs['max_y'])

        # gui:
        self.header = Frame(self.frame)
        Label(self.header, text="Number of dimensions:").grid(row=0, column=0)
        OptionMenu(self.header, self.histogram_dim, "1D", "2D", command=self.set_hist_dim).grid(row=0, column=1)
        Label(self.header, text="Histogram type:").grid(row=1, column=0)
        self.types_menu = OptionMenu(self.header, self.histogram_type, *curr_menu, command=self.set_hist_type)
        self.types_menu.grid(row=1, column=1)
        Label(self.header, text="Number of files for statistics (1 to {0})".format(self.max_iters)).grid(row=2, column=0)
        Entry(self.header, textvariable=self.iters).grid(row=2, column=1)
        self.header.pack()

        self.x_frame = Frame(self.frame)
        Label(self.x_frame, text="Number of bins (x):").grid(row=0, column=0)
        Entry(self.x_frame, textvariable=self.bins_x).grid(row=0, column=1)
        self.x_range_label = Label(self.x_frame, text="x range [{0}]".format(self.get_unit(self.histogram_type.get(), 'x')))
        self.x_range_label.grid(row=1, column=0, columnspan=2)
        x_range_frame = Frame(self.x_frame)
        Label(x_range_frame, text="min:").pack(side=LEFT)
        Entry(x_range_frame, textvariable=self.min_x).pack(side=LEFT)
        Label(x_range_frame, text="max:").pack(side=LEFT)
        Entry(x_range_frame, textvariable=self.max_x).pack(side=LEFT)
        x_range_frame.grid(row=3, columnspan=4, rowspan=4)
        self.x_frame.pack()

        self.y_frame = Frame(self.frame)
        Label(self.y_frame, text="Number of bins (y):").grid(row=0, column=0)
        Entry(self.y_frame, textvariable=self.bins_y).grid(row=0, column=1)
        self.y_range_label = Label(self.y_frame, text="y range [{0}]".format(self.get_unit(self.histogram_type.get(), 'y')))
        self.y_range_label.grid(row=1, column=0, columnspan=2)
        y_range_frame = Frame(self.y_frame)
        Label(y_range_frame, text="min:").pack(side=LEFT)
        Entry(y_range_frame, textvariable=self.min_y).pack(side=LEFT)
        Label(y_range_frame, text="max:").pack(side=LEFT)
        Entry(y_range_frame, textvariable=self.max_y).pack(side=LEFT)
        y_range_frame.grid(row=3, columnspan=4, rowspan=4)

        if self.histogram_dim.get() == '2D':
            self.y_frame.pack()

    def get_menu_for_dim(self, dim):
        menu = [name for name, value in self.menus.iteritems() if value['dim'] == dim]
        return list(menu)

    def get_unit(self, hist_type, axis):
        return self.menus[hist_type]['unit_' + axis]

    def set_hist_dim(self, hist_dim):
        curr_menu = self.get_menu_for_dim(hist_dim)
        self.histogram_type.set(curr_menu[0])
        self.set_hist_type(curr_menu[0])
        self.types_menu.grid_forget()
        self.types_menu = OptionMenu(self.header, self.histogram_type, *curr_menu, command=self.set_hist_type)
        self.types_menu.grid(row=1, column=1)

        if hist_dim == '1D':
            self.y_frame.pack_forget()
        else:
            self.y_frame.pack(side=BOTTOM)

    def set_hist_type(self, hist_type):
        self.x_range_label.grid_forget()
        self.x_range_label = Label(self.x_frame, text="x range [{0}]".format(self.get_unit(hist_type, 'x')))
        self.x_range_label.grid(row=1, column=0, columnspan=2)

        if self.histogram_dim.get() == '2D':
            self.y_range_label.grid_forget()
            self.y_range_label = Label(self.y_frame, text="y range [{0}]".format(self.get_unit(hist_type, 'y')))
            self.y_range_label.grid(row=1, column=0, columnspan=2)

    def get_vars_list(self):
        if self.histogram_dim.get() == '2D':
            self.vars_list.extend(['bins_y', 'min_y', 'max_y'])
        return self.vars_list

    def get_cmd(self):
        cmd = '-T' + self.menus[self.histogram_type.get()]['cmd']
        cmd += ' -n ' + str(self.bins_x.get())
        cmd += ' -h ' + str(self.min_x.get())
        cmd += ' -H ' + str(self.max_x.get())

        if self.histogram_dim.get() == "2D":
            cmd += ' -m ' + str(self.bins_y.get())
            cmd += ' -b ' + str(self.min_y.get())
            cmd += ' -B ' + str(self.max_y.get())

        return cmd

    def get_data(self):
        data = 'Histogram: {hist_type}\nBins (x) = {bins_x}\nRange (x) = {min_x} - {max_x} [{unit_x}]'.format(
                hist_type=self.histogram_type.get(), bins_x=self.bins_x.get(), min_x=self.min_x.get(),
                max_x=self.max_x.get(), unit_x=self.get_unit(self.histogram_type.get(), 'x'))

        if self.histogram_dim.get() == '2D':
            data += '\nBins (y) = {bins_y}\nRange (y) = {min_y} - {max_y} [{unit_y}]'.format(
                bins_y=self.bins_y.get(), min_y=self.min_y.get(),
                max_y=self.max_y.get(), unit_y=self.get_unit(self.histogram_type.get(), 'y'))

        return data

    def is_yield(self, histogram_type):
        return self.menus[histogram_type]['yield']

    def finalize(self):
        if self.is_yield(self.histogram_type.get()):
            self.controller.switch_page("SamplePage", 1)
            self.controller.switch_page("SupportMainPage", 1)
        else:
            self.controller.switch_page("SamplePage", 0)
            self.controller.switch_page("SupportMainPage", 0)

        if self.iters.get() not in range(1, self.max_iters + 1):
            self.controller.raise_error_message('Number of files for statistics must be between 1 and ' + str(self.max_iters))
            return False
        return True
