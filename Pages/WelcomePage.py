from BasePage import *


class WelcomePage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Welcome", has_prev=False)

        # vars:
        currList = self.get_collim_list(controller.ear.get())
        self.collim = StringVar(self, currList[0])
        self.other_collim_file_path = StringVar(self)
        self.output_dir = StringVar(self)

        # gui:
        self.frame.pack()
        Label(self.frame, text="Welcome to the transport simulation configuration wizard!").grid(row=0, columnspan=2)
        Label(self.frame, text="Please select experiment area:").grid(row=1, column=0)
        OptionMenu(self.frame, controller.ear, "EAR1", "EAR2", command=controller.set_ear).grid(row=1, column=1)

        Label(self.frame, text="Please select collimation input file:").grid(row=2, column=0)
        self.collim_option = OptionMenu(self.frame, self.collim, *currList, command=self.set_other_file)
        self.collim_option.grid(row=2, column=1)

        self.other_collim_frame = Frame(self.frame)
        Label(self.other_collim_frame, text="Specify the path for the collimation file:").grid(row=0, column=0)
        Entry(self.other_collim_frame, textvariable=self.other_collim_file_path).grid(row=0, column=1)
        Button(self.other_collim_frame, text="Select",
               command=lambda: self.controller.open_file_dialog(self.other_collim_file_path, file_type='inp')).grid(row=0, column=2)

        Label(self.frame, text="Specify the output directory:").grid(row=4, column=0)
        Entry(self.frame, textvariable=self.output_dir).grid(row=4, column=1)
        Button(self.frame, text="Select",
               command=lambda: self.controller.open_file_dialog(self.output_dir, file_type='dir')).grid(row=4, column=2)

        Checkbutton(self, text="Use default arguments for all the other parameters?", variable=controller.use_default).pack(side=BOTTOM)

    def get_collim_list(self, ear):
        currList = default_values[ear]['collimation']
        return currList + ["Other"]

    def set_collim(self, ear):
        self.collim_option.grid_forget()
        currList = self.get_collim_list(ear)
        self.collim = StringVar(self, currList[0])
        self.collim_option = OptionMenu(self.frame, self.collim, *currList, command=self.set_other_file)
        self.collim_option.grid(row=2, column=1)
        self.set_other_file('new')

    def set_other_file(self, file):
        if file == "Other":
            self.other_collim_frame.grid(row=3, columnspan=3)
        else:
            self.other_collim_frame.grid_forget()

    def get_ear_cmd(self):
        return default_values[self.controller.ear.get()]['const']

    def get_collimation_cmd(self):
        collim = self.collim.get()
        if collim == "Other":
            cmd = self.other_collim_file_path.get()
        else:
            cmd = '-i ' + default_values['collimation_path'] + collim + '.inp'
        return cmd

    def get_output_cmd(self):
        return '-o ' + self.output_dir.get() + '/${{i}}.out'

    def get_cmd(self):
        return self.get_ear_cmd() + ' ' + self.get_collimation_cmd() + ' ' + self.get_output_cmd()

    def get_summary(self, master, row, widths):
        Label(master, text="EAR", relief=SUNKEN, width=widths[0], height=2).grid(row=row, column=0)
        Label(master, bg='white', text=self.controller.ear.get(), relief=SUNKEN, width=widths[1], height=2).grid(row=row, column=1)
        Label(master, bg='white', text=self.get_ear_cmd(), relief=SUNKEN, width=widths[2], height=2).grid(row=row, column=2)

        Label(master, text="Collimation", relief=SUNKEN, width=widths[0], height=2).grid(row=row+1, column=0)
        Label(master, bg='white', text=self.collim.get(), relief=SUNKEN, width=widths[1], height=2).grid(row=row+1, column=1)
        Label(master, bg='white', text=self.get_collimation_cmd(), relief=SUNKEN, width=widths[2], height=2).grid(row=row+1, column=2)

        Label(master, text="Output", relief=SUNKEN, width=widths[0], height=2).grid(row=row+2, column=0)
        Label(master, bg='white', text=self.output_dir.get(), relief=SUNKEN, width=widths[1], height=2).grid(row=row+2, column=1)
        Label(master, bg='white', text=self.get_output_cmd(), relief=SUNKEN, width=widths[2], height=2).grid(row=row+2, column=2)

        return 3 # number of added rows

    def finalize(self):
        if not os.path.exists(self.output_dir.get()):
            self.controller.raise_error_message("Output directory does not exist.\nPlease specify an existing directory.")
            return False

        if self.collim.get() == 'Other' and not os.path.exists(self.other_collim_file_path.get()):
            self.controller.raise_error_message("Collimation file does not exist.\nPlease try again.")
            return False

        return True
