from BaseWidget import *
from subprocess import Popen, PIPE
from Utils.CSVHandler import csv2dict, paths

allow_rebinning = True


class Averager(BaseWidget):
    def __init__(self, app_manager, parent):
        BaseWidget.__init__(self, app_manager, parent, title='Create Plots')

        self.rebinning_window = None
        self.rebinning_vars = dict()
        self.rebin = IntVar(0)
        self.configs = None
        self.histogram_name = StringVar(self)

        Label(self.frame, textvariable=self.histogram_name).pack()
        Button(self.frame, text='Average', command=self.average).pack()
        Button(self.frame, text='Create ROOT file', command=self.open_rebinning_window if allow_rebinning else self.convert).pack()

    def open_file_dialog(self):
        BaseWidget.open_file_dialog(self)
        submit_dir = self.get_submit_dir()
        if not submit_dir:
            return
        self.configs = csv2dict(os.path.join(submit_dir, 'configs.csv'))
        name = self.configs['histogram_type']
        if self.configs['histogram_dim'] == '1D':
            name += ' (yield)' if self.configs.get('is_yield', 0) else ' (fluence)'
        self.histogram_name.set('Histogram type: ' + name)

    def average(self):
        submit_dir = self.get_submit_dir()
        ls = os.listdir(os.path.join(submit_dir, 'output'))
        res = [os.path.join(submit_dir, 'output', i) for i in ls if i.startswith('res')]
        if len(res) < 2:
            self.app_manager.raise_error_message('Must be at least 2 files for the average.')
            return

        loc = paths['average{d}'.format(d=self.configs['histogram_dim'].lower())]
        out_path = os.path.join(submit_dir, 'output', 'out.hist')
        process = Popen([loc, out_path] + res, stdout=PIPE)
        process.wait()
        self.app_manager.raise_error_message(
            'The average histogram for {name} was saved to the output folder under out.hist'.format(name=self.configs['histogram_type']), title='Done!')

    def open_rebinning_window(self):
        self.rebinning_window = Toplevel(self)
        Label(self.rebinning_window, text='Create ROOT file', font=self.app_manager.title_font).pack()
        self.rebinning_frame = Frame(self.rebinning_window)
        Checkbutton(self.rebinning_window, text='Re-bin?', variable=self.rebin,
                    command=lambda: self.rebinning_frame.pack()).pack()
        Button(self.rebinning_window, text='Convert', command=self.convert).pack(side=BOTTOM)

        # init rebinning_vars to values of run
        axis = ['x']
        if self.configs['histogram_dim'] == '2D':
            axis.append('y')

        for curr_axis in axis:
            self.rebinning_vars[curr_axis] = dict()
            for var in ['bins', 'min', 'max']:
                self.rebinning_vars[curr_axis][var] = StringVar(self, self.configs.get(var + '_' + curr_axis, ''))

        # rebinning frame
        for j, var in enumerate(['bins', 'min', 'max']):
            Label(self.rebinning_frame, text=var).grid(row=0, column=j + 1)

        for i, curr_axis in enumerate(axis):
            Label(self.rebinning_frame, text=curr_axis).grid(row=i+1, column=0)
            for j, var in enumerate(['bins', 'min', 'max']):
                Entry(self.rebinning_frame, textvariable=self.rebinning_vars[curr_axis][var], width=15).grid(row=i+1, column=j+1)

    def show_rebinning_frame(self):
        if self.rebin.get():
            self.rebinning_frame.pack()
        else:
            self.rebinning_frame.pack_forget()

    def get_rebinning_cmd(self):
        if not self.rebin.get():
            return []

        cmd = []

        # x
        for arg, var in zip(['n', 'f', 'l'], ['bins', 'min', 'max']):
            cmd.append('-' + arg)
            cmd.append(str(self.rebinning_vars['x'][var].get()))

        # y
        if self.configs['histogram_dim'] == '2D':
            for arg, var in zip(['N', 'F', 'L'], ['bins', 'min', 'max']):
                cmd.append('-' + arg)
                cmd.append(str(self.rebinning_vars['y'][var].get()))

        return cmd

    def convert(self):
        if self.rebinning_window:
            self.rebinning_window.destroy()

        submit_dir = self.get_submit_dir()
        out_file = os.path.join(submit_dir, 'output', 'out.hist')
        if not os.path.exists(out_file):
            self.app_manager.raise_error_message(
                'The file out.hist file does not exist.\nPlease run the average first, and then try again.')
            return

        loc = paths['hist2root']
        cmd = [loc, '-F', out_file]
        cmd += self.get_rebinning_cmd()
        process = Popen(cmd, stdout=PIPE)
        process.wait()
        self.app_manager.raise_error_message('The ROOT file is now saved to the output directory.', title='Done!')
