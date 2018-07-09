from BasePage import *
from Utils.CSVHandler import read_histogram_menus


class HistogramPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Histogram")

        # vars:
        self.vars_list = ['histogram_dim', 'histogram_type', 'bins_x', 'min_x', 'max_x',
                          'min_e', 'max_e', 'min_t', 'max_t']
        self.histogram_dim = StringVar(self, kwargs['histogram_dim'])
        self.menus = read_histogram_menus(self.controller.paths['histogram_menus_path'])
        curr_menu = self.get_menu_for_dim(self.histogram_dim.get())
        self.histogram_type = StringVar(self, kwargs.get('histogram_type', curr_menu[0]))

        self.bins_x = IntVar(self, kwargs['bins_x'])
        self.bins_y = IntVar(self, kwargs['bins_y'])
        self.min_x = StringVar(self, kwargs['min_x'])
        self.max_x = StringVar(self, kwargs['max_x'])
        self.min_y = StringVar(self, kwargs['min_y'])
        self.max_y = StringVar(self, kwargs['max_y'])

        self.use_cutoffs = IntVar(0)
        self.min_e = StringVar(self, kwargs['min_e'])
        self.max_e = StringVar(self, kwargs['max_e'])
        self.min_t = StringVar(self, kwargs['min_t'])
        self.max_t = StringVar(self, kwargs['max_t'])

        self.unit_x = StringVar(self, "[{0}]".format(self.get_unit(self.histogram_type.get(), 'x')))
        self.unit_y = StringVar(self, "[{0}]".format(self.get_unit(self.histogram_type.get(), 'y')))

        # gui:
        self.header = Frame(self.frame)
        Label(self.header, text="Histogram type:").grid(row=0, column=0)
        OptionMenu(self.header, self.histogram_dim, *["1D", "2D"], command=self.set_hist_dim).grid(row=0, column=1)
        self.types_menu = OptionMenu(self.header, self.histogram_type, *curr_menu, command=self.set_hist_type)
        self.types_menu.grid(row=0, column=2)
        self.header.pack()

        self.table = Frame(self.frame)
        for i, txt in enumerate(["bins", "min", "max"]):
            Label(self.table, text=txt).grid(row=0, column=i+2)

        Label(self.table, text="x").grid(row=1, column=0)
        Label(self.table, textvariable=self.unit_x).grid(row=1, column=1)
        for i, var in enumerate([self.bins_x, self.min_x, self.max_x]):
            Entry(self.table, textvariable=var, width=15).grid(row=1, column=i+2)

        self.y_values = [Label(self.table, text="y"), Label(self.table, textvariable=self.unit_y)]
        self.y_values += [Entry(self.table, textvariable=var, width=15) for var in [self.bins_y, self.min_y, self.max_y]]
        self.grid_y(self.histogram_dim.get() == '2D')
        self.table.pack()

        Label(self.frame, text="Cutoff", font=self.title_font).pack()
        Checkbutton(self.frame, text="Use cutoffs?", variable=self.use_cutoffs, command=self.show_cutoff_frame).pack()
        self.cutoff_frame = Frame(self.frame)
        Label(self.cutoff_frame, text="min").grid(row=0, column=1)
        Label(self.cutoff_frame, text="max").grid(row=0, column=2)

        Label(self.cutoff_frame, text="Energy [eV]").grid(row=1, column=0)
        Entry(self.cutoff_frame, textvariable=self.min_e).grid(row=1, column=1)
        Entry(self.cutoff_frame, textvariable=self.max_e).grid(row=1, column=2)

        Label(self.cutoff_frame, text="Time [s]").grid(row=2, column=0)
        Entry(self.cutoff_frame, textvariable=self.min_t).grid(row=2, column=1)
        Entry(self.cutoff_frame, textvariable=self.max_t).grid(row=2, column=2)

    def show_cutoff_frame(self):
        if self.use_cutoffs.get():
            self.cutoff_frame.pack()
        else:
            self.cutoff_frame.pack_forget()

    def grid_y(self, show):
        for i, item in enumerate(self.y_values):
            if show:
                item.grid(row=2, column=i)
            else:
                item.grid_forget()

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
        self.types_menu.grid(row=0, column=2)
        self.grid_y(hist_dim == '2D')

    def set_hist_type(self, hist_type):
        self.unit_x.set("[{0}]".format(self.get_unit(hist_type, 'x')))
        bit = int(self.is_yield(hist_type))
        self.controller.switch_page("SamplePage", bit)

        if self.histogram_dim.get() == '2D':
            self.unit_y.set("[{0}]".format(self.get_unit(hist_type, 'y')))

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

        if self.use_cutoffs.get():
            cmd = '-e ' + str(self.min_e.get())
            cmd += ' -E ' + str(self.max_e.get())
            cmd += ' -c ' + str(self.min_t.get())
            cmd += ' -C ' + str(self.max_t.get())
        return cmd

    def get_data(self):
        data = 'Histogram: {hist_type}\nBins (x) = {bins_x}\nRange (x) = {min_x} - {max_x} [{unit_x}]'.format(
                hist_type=self.histogram_type.get(), bins_x=self.bins_x.get(), min_x=self.min_x.get(),
                max_x=self.max_x.get(), unit_x=self.get_unit(self.histogram_type.get(), 'x'))

        if self.histogram_dim.get() == '2D':
            data += '\nBins (y) = {bins_y}\nRange (y) = {min_y} - {max_y} [{unit_y}]'.format(
                bins_y=self.bins_y.get(), min_y=self.min_y.get(),
                max_y=self.max_y.get(), unit_y=self.get_unit(self.histogram_type.get(), 'y'))

        if self.use_cutoffs.get():
            data += '\nEnergy cutoff: {0} - {1} [eV]'.format(self.min_e.get(), self.max_e.get())
            data += '\nTime cutoff: {0} - {1} [s]'.format(self.min_t.get(), self.max_t.get())
        return data

    def is_yield(self, histogram_type):
        return self.menus[histogram_type]['yield']

    def finalize(self):
        bit = int(self.is_yield(self.histogram_type.get()))
        self.controller.switch_page("SamplePage", bit)
        return True
