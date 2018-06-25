from BasePage import *
import pickle


class WelcomePage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Welcome!", has_prev=False)
        self.config_file = StringVar(self)
        self.config_set = IntVar(0)

        # gui:
        self.frame.pack()
        txt = "Welcome to the transport simulation configuration wizard!\nUse this wizard to set up a simulation and see its results.\nWhat would you like to do?"
        Label(self.frame, text=txt, justify=LEFT).grid(sticky="w", row=0, columnspan=2)

        # Radiobutton(self, variable=self.controller.config_set, value=0, text="Use default configurations").pack(anchor="w")
        Radiobutton(self.frame, variable=self.config_set, value=0, text="Load configurations",
                    command=lambda: self.loader_button.grid(sticky="w", row=1, column=1)).grid(sticky="w", row=1, column=0)

        self.loader_button = Button(self.frame, text="Load",
                                    command=lambda: self.controller.open_file_dialog(self.config_file, file_type='pkl'))
        self.loader_button.grid(sticky="w", row=1, column=1)

        Radiobutton(self.frame, variable=self.config_set, value=1, text="Configure manually",
                    command=lambda: self.loader_button.grid_forget()).grid(sticky="w", row=2, column=0)

    def finalize(self):
        if self.config_set.get() == 0 and not self.config_file.get():
            self.controller.raise_error_message("Please provide a config file.")
            return False
        return True

    def get_config_file(self):
        if self.config_set.get() == 1:
            return None
        return self.config_file.get()
