from BasePage import *
from Utils.CSVHandler import read_histogram_menus, read_histogram_types


class HistogramPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Histogram")

        # vars:
        self.vars_list = ['histogram_dim', 'histogram_type']
        self.histogram_dim = StringVar(self, kwargs['histogram_dim'])
        self.menus = read_histogram_menus()
        self.types = read_histogram_types()
        curr_menu = self.get_menu_for_dim(self.histogram_dim.get())
        self.histogram_type = StringVar(self, kwargs.get('histogram_type', curr_menu[0]))
        self.is_yield = IntVar(0)

        self.x_vars = dict()
        self.y_vars = dict()
        for key in ['bins', 'min', 'max']:
            self.x_vars[key] = StringVar(self)
            self.y_vars[key] = StringVar(self)

        self.text_x = StringVar(self)
        self.text_y = StringVar(self)
        self.set_hist_type(self.histogram_type.get())

        self.use_cutoffs = IntVar(0)
        self.e_vars = {'min': StringVar(self, kwargs['min_e']), 'max': StringVar(self, kwargs['max_e'])}
        self.t_vars = {'min': StringVar(self, kwargs['min_t']), 'max': StringVar(self, kwargs['max_t'])}

        # gui:
        self.header = Frame(self.frame)
        Label(self.header, text="Histogram type:").grid(row=0, column=0)
        OptionMenu(self.header, self.histogram_dim, *["1D", "2D"], command=self.set_hist_dim).grid(row=0, column=1)
        self.types_menu = OptionMenu(self.header, self.histogram_type, *curr_menu, command=self.set_hist_type)
        self.types_menu.grid(row=0, column=2)
        self.check_yield = Checkbutton(self.header, text='yield?', variable=self.is_yield,
                                       command=lambda: self.controller.switch_page("SamplePage", self.is_yield.get()))
        if self.histogram_dim.get() == '1D':
            self.check_yield.grid(row=0, column=3)
        self.header.pack()

        self.table = Frame(self.frame)
        for i, txt in enumerate(["bins", "min", "max"]):
            Label(self.table, text=txt).grid(row=0, column=i+2)

        Label(self.table, textvariable=self.text_x).grid(row=1, column=0)
        for i, var in enumerate(self.x_vars.values()):
            Entry(self.table, textvariable=var, width=15).grid(row=1, column=i+1)

        self.y_values = [Label(self.table, textvariable=self.text_y)]
        self.y_values += [Entry(self.table, textvariable=var, width=15) for var in self.y_vars.values()]
        self.grid_y(self.histogram_dim.get() == '2D')
        self.table.pack()

        Label(self.frame, text="Cutoff", font=self.title_font).pack()
        Checkbutton(self.frame, text="Use cutoffs?", variable=self.use_cutoffs, command=self.show_cutoff_frame).pack()
        self.cutoff_frame = Frame(self.frame)
        Label(self.cutoff_frame, text="min").grid(row=0, column=1)
        Label(self.cutoff_frame, text="max").grid(row=0, column=2)

        for i, text, vars_dict in zip([1, 2], ["Energy [eV]", "Tof [s]"], [self.e_vars, self.t_vars]):
            Label(self.cutoff_frame, text=text).grid(row=i, column=0)
            Entry(self.cutoff_frame, textvariable=vars_dict['min']).grid(row=i, column=1)
            Entry(self.cutoff_frame, textvariable=vars_dict['max']).grid(row=i, column=2)

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
        name = self.menus[hist_type]['name_' + axis]
        return self.types[name]['unit']

    def set_hist_dim(self, hist_dim):
        curr_menu = self.get_menu_for_dim(hist_dim)
        self.histogram_type.set(curr_menu[0])
        self.set_hist_type(curr_menu[0])
        self.types_menu.grid_forget()
        self.types_menu = OptionMenu(self.header, self.histogram_type, *curr_menu, command=self.set_hist_type)
        self.types_menu.grid(row=0, column=2)
        self.grid_y(hist_dim == '2D')
        if hist_dim == '1D':
            self.check_yield.grid(row=0, column=3)
        else:
            self.check_yield.grid_forget()

    def set_hist_type(self, hist_type):
        curr_dict = self.menus[hist_type]
        self.set_axis_type('x', curr_dict['name_x'])

        if self.histogram_dim.get() == '2D':
            self.set_axis_type('y', curr_dict['name_y'])

    def set_axis_type(self, axis, hist_type):
        if axis == 'x':
            vars_dict = self.x_vars
            text_var = self.text_x
        else:
            vars_dict = self.y_vars
            text_var = self.text_y

        params = self.types[hist_type]
        text_var.set('{name} [{unit}]'.format(name=hist_type, unit=params['unit']))
        for var, key in zip(vars_dict.values(), ['bins', 'min', 'max']):
            var.set(params[key])

    def get_vars_list(self):
        if self.histogram_dim.get() == '2D':
            self.vars_list.extend(['bins_y', 'min_y', 'max_y'])
        return self.vars_list

    def get_cmd(self):
        cmd = '-T' + self.menus[self.histogram_type.get()]['cmd']

        for arg, var in zip([' -n ', ' -h ', ' -H '], ['bins', 'min', 'max']):
            cmd += arg + str(self.x_vars[var].get())

        if self.histogram_dim.get() == "2D":
            for arg, var in zip([' -m ', ' -b ', ' -N '], ['bins', 'min', 'max']):
                cmd += arg + str(self.y_vars[var].get())

        if self.use_cutoffs.get():
            for arg, var in zip([' -e ', ' -E '], ['min', 'max']):
                cmd += arg + str(self.e_vars[var].get())

            for arg, var in zip([' -c ', ' -C '], ['min', 'max']):
                cmd += arg + str(self.t_vars[var].get())
        return cmd

    def get_data(self):
        data = 'Histogram: ' + self.histogram_type.get()
        if self.is_yield.get():
            data += ' (yield)'
        data += '\nBins (x) = {bins_x}\nRange (x) = {min_x} - {max_x} [{unit_x}]'.format(
                bins_x=self.x_vars['bins'].get(), min_x=self.x_vars['min'].get(),
                max_x=self.x_vars['max'].get(), unit_x=self.get_unit(self.histogram_type.get(), 'x'))

        if self.histogram_dim.get() == '2D':
            data += '\nBins (y) = {bins_y}\nRange (y) = {min_y} - {max_y} [{unit_y}]'.format(
                bins_y=self.y_vars['bins'].get(), min_y=self.y_vars['min'].get(),
                max_y=self.y_vars['max'].get(), unit_y=self.get_unit(self.histogram_type.get(), 'y'))

        if self.use_cutoffs.get():
            data += '\nEnergy cutoff: {0} - {1} [eV]'.format(self.e_vars['min'].get(), self.e_vars['max'].get())
            data += '\nTime cutoff: {0} - {1} [s]'.format(self.t_vars['min'].get(), self.t_vars['max'].get())
        return data

    def finalize(self):
        self.controller.switch_page("SamplePage", self.is_yield.get())
        return True
