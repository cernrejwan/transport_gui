from BaseWidget import *
from subprocess import Popen, PIPE


class Averager(BaseWidget):
    def __init__(self, app_manager, parent):
        BaseWidget.__init__(self, app_manager, parent, title='Create Plots')
        self.s2ns = IntVar(0)
        self.tof_vs_e = IntVar(0)

        Button(self.frame, text='Average 1D', command=lambda: self.average(1)).pack()
        Button(self.frame, text='Average 2D', command=lambda: self.average(2)).pack()
        Button(self.frame, text='Create ROOT file', command=self.create_root).pack()

    def average(self, d):
        submit_dir = self.get_submit_dir()
        if not submit_dir:
            return

        ls = os.listdir(os.path.join(submit_dir, 'output'))
        res = [os.path.join(submit_dir, 'output', i) for i in ls if i.startswith('res')]
        if len(res) < 2:
            self.app_manager.raise_error_message('Must be at least 2 files for the average.')
            return

        loc = self.app_manager.paths['average{d}d'.format(d=d)]
        out_path = os.path.join(submit_dir, 'output', 'out.hist')
        process = Popen([loc, out_path] + res, stdout=PIPE)
        process.wait()
        self.app_manager.raise_error_message('The average histogram was saved to the output folder under out.hist', title='Done!')

    def create_root(self):
        submit_dir = self.get_submit_dir()
        if not submit_dir:
            return

        window = Toplevel(self)
        Label(window, text='Create ROOT file', font=self.app_manager.title_font).pack()
        hist_type = Checkbutton(window, text='Tof vs Energy?', variable=self.tof_vs_e)
        Checkbutton(window, text='Convert s to ns?', variable=self.s2ns, command=lambda: hist_type.pack()).pack()
        Button(window, text='Convert', command=lambda: self.hist2root(window)).pack(side=BOTTOM)

    def hist2root(self, window):
        window.destroy()

        submit_dir = self.get_submit_dir()
        if not submit_dir:
            return

        out_file = os.path.join(submit_dir, 'output', 'out.hist')
        if not os.path.exists(out_file):
            self.app_manager.raise_error_message(
                'The file out.hist file does not exist in submit directory.\nPlease run the averade 1\\2D first, and then try again.')
            return

        loc = self.app_manager.paths['hist2root']
        cmd = [loc, '-F', out_file]
        if self.s2ns.get():
            cmd += ['-s', 1]
        if self.tof_vs_e.get():
            cmd += ['-S', 1]
        process = Popen(cmd, stdout=PIPE)
        process.wait()
        self.app_manager.raise_error_message('The ROOT file is now saved to the output directory.', title='Done!')
