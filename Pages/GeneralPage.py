from BasePage import *


class GeneralPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "General Configurations", has_prev=False)

        # vars:
        self.vars_list = ['ear', 'collimation']
        self.ear = StringVar(self, "EAR1")
        self.collimation = StringVar(self, kwargs['collimation'])
        self.user_collimation_file = StringVar(self, kwargs.get('user_collimation_file', ''))
        self.output_dir = StringVar(self, os.path.expanduser('~'))

        self.collim_lists = dict()
        self.init_collim_list(self.controller.paths['collimation_files_path'])
        currList = self.collim_lists[self.ear.get()]

        # gui:
        self.frame.pack()
        Label(self.frame, text="Select experiment area:").grid(row=1, column=0)
        OptionMenu(self.frame, self.ear, "EAR1", "EAR2", command=controller.set_ear).grid(row=1, column=1)
        Label(self.frame, text="Select collimation input file:").grid(row=2, column=0)
        self.collim_option = OptionMenu(self.frame, self.collimation, *currList, command=self.set_other_file)
        self.collim_option.grid(row=2, column=1)

        self.other_collim_frame = Frame(self.frame)
        Label(self.other_collim_frame, text="Specify the path for the collimation file:").grid(row=0, column=0)
        Entry(self.other_collim_frame, textvariable=self.user_collimation_file).grid(row=0, column=1)
        Button(self.other_collim_frame, text="Select",
               command=lambda: self.controller.open_file_dialog(self.user_collimation_file, file_type='inp')).grid(row=0, column=2)

        Label(self.frame, text="Specify the output directory:").grid(row=4, column=0)
        Entry(self.frame, textvariable=self.output_dir).grid(row=4, column=1)
        Button(self.frame, text="Select",
               command=lambda: self.controller.open_file_dialog(self.output_dir, file_type='dir')).grid(row=4, column=2)

        # Checkbutton(self, text="Use default arguments for all the other parameters?", variable=controller.use_default).pack(side=BOTTOM)

    def init_collim_list(self, collim_path):
        files_list = os.listdir(collim_path)
        self.collim_lists['EAR1'] = [f.split('.')[0] for f in files_list if f.lower().startswith('ear1')] + ["Other"]
        self.collim_lists['EAR2'] = [f.split('.')[0] for f in files_list if f.lower().startswith('ear2')] + ["Other"]

    def set_collim(self, ear):
        self.collim_option.grid_forget()
        currList = self.collim_lists[self.ear.get()]
        self.collimation = StringVar(self, currList[0])
        self.collim_option = OptionMenu(self.frame, self.collimation, *currList, command=self.set_other_file)
        self.collim_option.grid(row=2, column=1)
        self.set_other_file('new')

    def set_other_file(self, file):
        if file == "Other":
            self.other_collim_frame.grid(row=3, columnspan=3)
        else:
            self.other_collim_frame.grid_forget()

    def get_ear_cmd(self):
        return self.controller.configs_dict[self.ear.get() + '_const']

    def get_collimation_cmd(self):
        collim = self.collimation.get()
        if collim == "Other":
            cmd = self.user_collimation_file.get()
        else:
            cmd = '-i ' + self.controller.paths['collimation_files_path'] + collim + '.inp'
        return cmd

    def get_output_cmd(self):
        return '-o ' + self.output_dir.get() + '/${{i}}.out'

    def get_cmd(self):
        return self.get_ear_cmd() + ' ' + self.get_collimation_cmd() + ' ' + self.get_output_cmd()

    def get_summary(self, master, row, widths):
        Label(master, text="EAR", relief=SUNKEN, width=widths[0], height=2).grid(row=row, column=0)
        Label(master, bg='white', text=self.ear.get(), relief=SUNKEN, width=widths[1], height=2).grid(row=row, column=1)
        Label(master, bg='white', text=self.get_ear_cmd(), relief=SUNKEN, width=widths[2], height=2).grid(row=row, column=2)

        Label(master, text="Collimation", relief=SUNKEN, width=widths[0], height=2).grid(row=row+1, column=0)
        Label(master, bg='white', text=self.collimation.get(), relief=SUNKEN, width=widths[1], height=2).grid(row=row + 1, column=1)
        Label(master, bg='white', text=self.get_collimation_cmd(), relief=SUNKEN, width=widths[2], height=2).grid(row=row+1, column=2)

        Label(master, text="Output", relief=SUNKEN, width=widths[0], height=2).grid(row=row+2, column=0)
        Label(master, bg='white', text=self.output_dir.get(), relief=SUNKEN, width=widths[1], height=2).grid(row=row+2, column=1)
        Label(master, bg='white', text=self.get_output_cmd(), relief=SUNKEN, width=widths[2], height=2).grid(row=row+2, column=2)

        return 3 # number of added rows

    def get_vars_list(self):
        if self.collimation.get == 'Other':
            self.vars_list.append('user_collimation_file')
        return self.vars_list

    def finalize(self):
        if not os.path.exists(self.output_dir.get()):
            self.controller.raise_error_message("Output directory does not exist.\nPlease specify an existing directory.")
            return False

        if self.collimation.get() == 'Other' and not os.path.exists(self.user_collimation_file.get()):
            self.controller.raise_error_message("Collimation file does not exist.\nPlease try again.")
            return False

        return True
