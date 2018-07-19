from BaseWidget import *
from Utils.CircularButton import CircularButton


class JobsInspector(BaseWidget):
    def __init__(self, app_manager, parent):
        BaseWidget.__init__(self, app_manager, parent, title='Check Status')
        Button(self.frame, text="Update", command=self.show_status).pack()
        self.table = Frame(self.frame)
        self.table.pack()

    @staticmethod
    def get_job_ids(submit_dir):
        filename = os.path.join(submit_dir, 'jobs', 'job_ids.txt')
        with open(filename, 'r') as f:
            ids = f.readlines()
        return [id.strip() for id in ids]

    def show_status(self):
        def get_status(i, id):
            if i in outputs:
                return 1    # done
            elif id in q:
                return 2    # running
            return 3    # dead

        submit_dir = self.get_submit_dir()
        if not submit_dir:
            return

        q = self.app_manager.get_condor_q()
        if not q:
            return

        ids = self.get_job_ids(submit_dir)
        outputs = self.get_output_files(submit_dir)
        self.running_jobs = list()

        for child in self.table.winfo_children():
            child.grid_forget()

        for col, txt in enumerate(['Job', 'Done', 'Running', 'Dead']):
            Label(self.table, text=txt).grid(row=0, column=col)

        for i, job_id in enumerate(ids):
            status = get_status(i, job_id)
            Label(self.table, text=str(i)).grid(row=i+1, column=0)
            Label(self.table, text='X').grid(row=i+1, column=status)
            if status == 2:
                self.running_jobs.append((i, job_id))

        if len(self.running_jobs) > 0:
            curr_row = len(ids) + 1
            Label(self.table, text='Push the red button to kill all running jobs').grid(row=curr_row, columnspan=4)
            CircularButton(self.table, 100, 'red', text='KILL', command=self.raise_warning).grid(row=curr_row + 1, columnspan=4)

        self.table.update()

    def raise_warning(self):
        num_jobs = len(self.running_jobs)
        message = 'Are you sure you want to kill {0} running jobs?'.format(num_jobs)
        self.app_manager.raise_warning(message, self.kill_jobs)

    def kill_jobs(self):
        window = Toplevel(self)
        Label(window, text='Killing jobs...', font=self.app_manager.title_font).pack(side='top', fill="x", pady=10)
        Label(window, text='Waiting for respond from HTCondor.').pack()
        window.update()
        for i, job_id in self.running_jobs:
            out = self.app_manager.system(['condor_rm', str(job_id)])
            if out.startswith('All jobs in cluster'):
                txt = 'job_{0} killed successfully.'.format(i)
            else:
                txt = 'Problem with killing job_{0}. Skipping.'.format(i)
            Label(window, text=txt).pack()
            window.update()

        Label(window, text='Done!').pack()
        Button(window, text='OK', command=window.destroy).pack(side=BOTTOM)
        window.update()
