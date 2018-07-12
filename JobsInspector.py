import tkFileDialog
from subprocess import Popen, PIPE
import os
from Tkinter import *


class JobsInspector(Frame):
    def __init__(self, app_manager, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.app_manager = app_manager
        self.job_ids = list()
        self.submit_dir = StringVar(self)

        Label(self, text='Check Status', font=self.app_manager.title_font).pack(side="top", fill="x", pady=10)
        Label(self, text="Specify the submit directory for which you want to check jobs status:").pack()
        load_frame = Frame(self)
        Entry(load_frame, textvariable=self.submit_dir).grid(row=1, column=0)
        Button(load_frame, text="Load", command=self.load_jobs_ids).grid(row=1, column=1)
        load_frame.pack()
        Button(self, text="Show", command=self.show_status).pack()

    def load_jobs_ids(self):
        submit_dir = tkFileDialog.askdirectory(initialdir='~', title="Select directory")
        self.submit_dir.set(submit_dir)
        filename = os.path.join(submit_dir, 'job_ids.txt')
        if not os.path.exists(filename):
            self.app_manager.raise_error_message("The specified path is not a valid submit directory/\nPlease try a different one.")
            return

        with open(filename, 'r') as f:
            ids = f.readlines()
        self.job_ids = ids

    @staticmethod
    def get_condor_q():
        q = Popen('condor_q', stdout=PIPE).communicate()[0]
        return q

    def show_status(self):
        q = self.get_condor_q()
        print(q)
