from subprocess import Popen, PIPE
import os
from Tkinter import *


class JobsInspector(Frame):
    def __init__(self, app_manager, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.app_manager = app_manager
        self.submit_dir = StringVar(self)
        self.verify_kill = False

        Label(self, text='Check Status', font=self.app_manager.title_font).pack(side="top", fill="x", pady=10)
        Label(self, text="Specify the submit directory for which you want to check jobs status:").pack()
        load_frame = Frame(self)
        Entry(load_frame, textvariable=self.submit_dir, width=45).grid(row=1, column=0)
        Button(load_frame, text="Load", command=lambda: self.app_manager.open_file_dialog(self.submit_dir, 'dir')).grid(row=1, column=1)
        load_frame.pack()
        Button(self, text="Update", command=self.show_status).pack()
        self.table = Frame(self)
        self.table.pack()

    @staticmethod
    def get_job_ids(submit_dir):
        filename = os.path.join(submit_dir, 'job_ids.txt')
        with open(filename, 'r') as f:
            ids = f.readlines()
        return [id.strip() for id in ids]

    @staticmethod
    def get_condor_q():
        q = Popen('condor_q', stdout=PIPE).communicate()[0]
        return q

    @staticmethod
    def get_output_files(submit_dir):
        output_dir = os.path.join(submit_dir, 'output')
        ls = os.listdir(output_dir)
        result = [int(i.split('_')[1].split('.')[0]) for i in ls]
        return result

    def show_status(self):
        def get_status(i, id):
            if i in outputs:
                return 1    # done
            elif id in q:
                return 2    # running
            return 3    # dead

        submit_dir = self.submit_dir.get()
        ls = os.listdir(submit_dir)
        if 'job_ids.txt' not in ls or 'output' not in ls:
            self.app_manager.raise_error_message("The specified path is not a valid submit directory/\nPlease try a different one.")
            return

        q = self.app_manager.get_condor_q()
        if not q:
            return

        ids = self.get_job_ids(submit_dir)
        outputs = self.get_output_files(submit_dir)
        running_jobs = list()

        for child in self.table.winfo_children():
            child.grid_forget()

        for col, txt in enumerate(['Job', 'Done', 'Running', 'Dead']):
            Label(self.table, text=txt).grid(row=0, column=col)

        for i, job_id in enumerate(ids):
            status = get_status(i, job_id)
            Label(self.table, text=str(i)).grid(row=i+1, column=0)
            Label(self.table, text='X').grid(row=i+1, column=status)
            if status == 2:
                running_jobs.append((i, job_id))

        if len(running_jobs) > 0:
            curr_row = len(ids) + 1
            Label(self.table, text='Push the red button to kill all running jobs').grid(row=curr_row, columnspan=4)
            Button(self.table, text='KILL', bg='red', command=lambda: self.kill_jobs(running_jobs)).grid(row=curr_row + 1, columnspan=4)

        self.table.update()

    def raise_warning(self, num_jobs):
        message = 'Are you sure you want to kill {0} running jobs?'.format(num_jobs)
        error_window = Toplevel(self)
        Label(error_window, text='Warning', font=self.app_manager.title_font).pack(side="top", fill="x", pady=10)
        Label(error_window, text=message).pack()

        buttons_frame = Frame(error_window)
        buttons_frame.pack(side=BOTTOM)

        def verify(value):
            self.verify_kill = value
            error_window.destroy()

        Button(buttons_frame, text="Yes", command=lambda: verify(True)).grid(row=0, column=0)
        Button(buttons_frame, text="No", command=lambda: verify(False)).grid(row=0, column=1)

    def kill_jobs(self, running_jobs):
        self.raise_warning(len(running_jobs))
        if not self.verify_kill:
            return

        window = Toplevel(self)
        Label(window, text='Waiting for respond from HTCondor.').pack()
        for i, job_id in running_jobs:
            out = Popen('condor_rm ' + str(job_id), stdout=PIPE).communicate()[0]
            if out.startswith('All jobs in cluster'):
                txt = 'job_{0} killed successfully.'.format(i)
            else:
                txt = 'Problem with killing job_{0}. Skipping.'.format(i)
            Label(window, text=txt).pack()
            window.update()

        Label(window, text='Done!').pack()
        Button(window, text='OK', command=window.destroy).pack(side=BOTTOM)
        window.update()
