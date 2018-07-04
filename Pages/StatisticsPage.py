from BasePage import *


class StatisticsPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Statistics")

        # vars:
        self.vars_list = ['min_e', 'max_e', 'min_t', 'max_t', 'iters']
        self.max_iters = len(self.controller.get_input_dirs())
        self.iters = IntVar(self, int(kwargs.get('iters', self.max_iters)))
        self.min_e = StringVar(self, kwargs['min_e'])
        self.max_e = StringVar(self, kwargs['max_e'])
        self.min_t = StringVar(self, kwargs['min_t'])
        self.max_t = StringVar(self, kwargs['max_t'])

        # gui
        Label(self.frame, text="Number of files for statistics (1 to {0})".format(self.max_iters)).grid(row=0, column=0)
        Entry(self.frame, textvariable=self.iters).grid(row=0, column=1)

        Label(self.frame, text="Energy cutoff [eV]").grid(row=1, columnspan=2)
        time_frame = Frame(self.frame)
        Label(time_frame, text="min:").pack(side=LEFT)
        Entry(time_frame, textvariable=self.min_e).pack(side=LEFT)
        Label(time_frame, text="max:").pack(side=LEFT)
        Entry(time_frame, textvariable=self.max_e).pack(side=LEFT)
        time_frame.grid(row=2, columnspan=4)

        Label(self.frame, text="Time cutoff [s]").grid(row=3, columnspan=2)
        time_frame = Frame(self.frame)
        Label(time_frame, text="min:").pack(side=LEFT)
        Entry(time_frame, textvariable=self.min_t).pack(side=LEFT)
        Label(time_frame, text="max:").pack(side=LEFT)
        Entry(time_frame, textvariable=self.max_t).pack(side=LEFT)
        time_frame.grid(row=4, columnspan=4)

    def get_cmd(self):
        cmd = '-e ' + str(self.min_e.get())
        cmd += ' -E ' + str(self.max_e.get())
        cmd += ' -c ' + str(self.min_t.get())
        cmd += ' -C ' + str(self.max_t.get())

    def finalize(self):
        if self.iters.get() not in range(1, self.max_iters + 1):
            self.controller.raise_error_message('Number of files for statistics must be between 1 and ' + str(self.max_iters))
            return False
        return True