from BasePage import *
import re


class HistoPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Histogram")

        # vars:
        self.hist_dim = StringVar(self, '1D')
        self.types_list = default_values['histogram'][self.hist_dim.get()]
        self.hist_type = StringVar(self, self.types_list[0])

        self.bins_x = IntVar(self, default_values['histogram']['-n'])
        self.bins_y = IntVar(self, default_values['histogram']['-m'])
        self.iters = IntVar(self, default_values['histogram']['num_iters'])
        self.min_x = StringVar(self, default_values['histogram']['-h'])
        self.max_x = StringVar(self, default_values['histogram']['-H'])
        self.min_y = StringVar(self, default_values['histogram']['-b'])
        self.max_y = StringVar(self, default_values['histogram']['-B'])

        # gui:
        self.frame.pack()
        self.header = Frame(self.frame)
        Label(self.header, text="Please select the number of dimensions:").grid(row=0, column=0)
        OptionMenu(self.header, self.hist_dim, "1D", "2D", command=self.set_hist_dim).grid(row=0, column=1)
        Label(self.header, text="Please select histogram type:").grid(row=1, column=0)
        self.types_menu = OptionMenu(self.header, self.hist_type, *self.types_list, command=self.set_hist_type)
        self.types_menu.grid(row=1, column=1)
        Label(self.header, text="Number of files for statistics (20 to 100)").grid(row=2, column=0)
        Entry(self.header, textvariable=self.iters).grid(row=2, column=1)
        self.header.pack()

        x_frame = Frame(self.frame)
        Label(x_frame, text="Number of bins (x):").grid(row=0, column=0)
        Entry(x_frame, textvariable=self.bins_x).grid(row=0, column=1)
        Label(x_frame, text="Please set x range:").grid(row=1, column=0, columnspan=2)
        x_range_frame = Frame(x_frame)
        Label(x_range_frame, text="min:").pack(side=LEFT)
        Entry(x_range_frame, textvariable=self.min_x).pack(side=LEFT)
        Label(x_range_frame, text="max:").pack(side=LEFT)
        Entry(x_range_frame, textvariable=self.max_x).pack(side=LEFT)
        x_range_frame.grid(row=3, columnspan=4, rowspan=4)
        x_frame.pack()

        self.y_frame = Frame(self.frame)
        Label(self.y_frame, text="Number of bins (y):").grid(row=0, column=0)
        Entry(self.y_frame, textvariable=self.bins_y).grid(row=0, column=1)
        Label(self.y_frame, text="Please set y range:").grid(row=1, column=0, columnspan=2)
        y_range_frame = Frame(self.y_frame)
        Label(y_range_frame, text="min:").pack(side=LEFT)
        Entry(y_range_frame, textvariable=self.min_y).pack(side=LEFT)
        Label(y_range_frame, text="max:").pack(side=LEFT)
        Entry(y_range_frame, textvariable=self.max_y).pack(side=LEFT)
        y_range_frame.grid(row=3, columnspan=4, rowspan=4)

    def set_hist_dim(self, hist_dim):
        self.types_list = default_values['histogram'][hist_dim]
        self.hist_type.set(self.types_list[0])
        self.types_menu.grid_forget()
        self.types_menu = OptionMenu(self.header, self.hist_type, *self.types_list, command=self.set_hist_type)
        self.types_menu.grid(row=1, column=1)

        if hist_dim == '1D':
            self.y_frame.pack_forget()
        else:
            self.y_frame.pack(side=BOTTOM)

    def set_hist_type(self, hist_type):
        pass
    #     switch = {
    #         "Energy [eV]": (1e-3, 1e9),
    #         "Time [s]": (0, 0.1),
    #         "Lambda [cm]": (0, 200),
    #         "Profile [cm]": (-2, 2)
    #     }
    #     min_x, max_x = switch[hist_type]
    #     self.min_x.set(min_x)
    #     self.max_x.set(max_x)

    def get_cmd(self):
        cmd = '-T?'
        cmd += ' -n ' + str(self.bins_x.get())
        cmd += ' -h ' + str(self.min_x.get())
        cmd += ' -H ' + str(self.max_x.get())

        if self.hist_dim.get() == "2D":
            cmd += ' -m ' + str(self.bins_y.get())
            cmd += ' -b ' + str(self.min_y.get())
            cmd += ' -B ' + str(self.max_y.get())

        return cmd

    def get_data(self):
        unit_x = re.search(r'\[(.*?)\]', self.hist_type.get()).group(1)
        data = 'Histogram: {hist_type}\nBins (x) = {bins_x}\nRange (x) = {min_x} - {max_x} [{unit_x}]'.format(
                hist_type=self.hist_type.get(), bins_x=self.bins_x.get(), min_x=self.min_x.get(),
                max_x=self.max_x.get(), unit_x=unit_x)

        if self.hist_dim.get() == '2D':
            unit_y = re.search(r'\[(.*?)\]', self.hist_type.get().split('vs')[1]).group(1)
            data += '\nBins (y) = {bins_y}\nRange (y) = {min_y} - {max_y} [{unit_y}]'.format(
                bins_y=self.bins_y.get(), min_y=self.min_y.get(),
                max_y=self.max_y.get(), unit_y=unit_y)

        return data