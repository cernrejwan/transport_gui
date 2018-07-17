from Tkinter import *
import os


class BaseWidget(Frame):
    def __init__(self, app_manager, parent, title):
        Frame.__init__(self, parent)
        self.parent = parent
        self.app_manager = app_manager
        self.submit_dir = StringVar(self)
        self.running_jobs = list()

        Label(self, text=title, font=self.app_manager.title_font).pack(side="top", fill="x", pady=10)
        Label(self, text="Specify the submit directory for which you want to check jobs status:").pack()
        load_frame = Frame(self)
        Entry(load_frame, textvariable=self.submit_dir, width=45).grid(row=1, column=0)
        Button(load_frame, text="Load", command=self.open_file_dialog).grid(row=1, column=1)
        load_frame.pack()

        self.frame = Frame(self)
        self.frame.pack()

        Button(self, text="Exit", command=self.parent.destroy).pack(side=BOTTOM)

    @staticmethod
    def get_output_files(submit_dir):
        output_dir = os.path.join(submit_dir, 'output')
        ls = os.listdir(output_dir)
        result = [int(i.split('_')[1].split('.')[0]) for i in ls]
        return result

    def get_submit_dir(self):
        submit_dir = self.submit_dir.get()
        if not submit_dir or not os.path.exists(submit_dir):
            self.app_manager.raise_error_message('Submit directory does not exist.\nPlease specify another one.')
            return

        ls = os.listdir(submit_dir)
        if 'jobs' not in ls or 'output' not in ls:
            self.app_manager.raise_error_message(
                "The specified path is not a valid submit directory.\nPlease try a different one.")
            return
        return submit_dir

    def open_file_dialog(self):
        self.app_manager.open_file_dialog(self.submit_dir, 'dir')
