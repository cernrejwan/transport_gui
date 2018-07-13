from BaseWidget import *


class Averager(BaseWidget):
    def __init__(self, app_manager, parent):
        BaseWidget.__init__(self, app_manager, parent, title='Create Plots')
        Button(self.frame, text='Average 1D', command=lambda: self.average(1)).pack()
        Button(self.frame, text='Average 1D', command=lambda: self.average(2)).pack()

    def average(self, d):
        submit_dir = self.get_submit_dir()
        if not submit_dir:
            return

        loc = self.app_manager.paths['average{d}d'.format(d=d)]
        out_path = os.path.join(submit_dir, 'output', 'out.hist')
        res_path = os.path.join(submit_dir, 'output', 'res_*')
        os.system(' '.join([loc, out_path, res_path]))

    def hist2root(self):
        submit_dir = self.get_submit_dir()
        if not submit_dir:
            return

        out_file = os.path.join(submit_dir, 'output', 'out.hist')
        if not os.path.exists(out_file):
            self.app_manager.raise_error_message('The file out.hist file does not exist in submit directory.\nPlease run the averade 1\\2D first, and then try again.')
        loc = self.app_manager.paths['hist2root']
