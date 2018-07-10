from BasePage import *


txt = """Welcome to the transport simulation configuration wizard!
Use it to set up parameters for a simulation and launch it,
or to check the status of older runs.
What would you like to do?"""


class WelcomePage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Welcome!", has_prev=False)
        self.config_file = StringVar(self)
        self.radio = IntVar(self, 1)

        # gui
        Label(self.frame, text=txt, justify=LEFT).grid(sticky="w", row=0, columnspan=2)
        Radiobutton(self.frame, variable=self.radio, value=1, text="Set up simulation parameters manually",
                    command=self.grid_load_button).grid(sticky="w", row=1, column=0)

        Radiobutton(self.frame, variable=self.radio, value=2, text="Load older run parameters",
                    command=self.grid_load_button).grid(sticky="w", row=2, column=0)

        # Radiobutton(self.frame, variable=self.radio, value=3, text="Check the status of a simulation",
        #             command=self.grid_load_button).grid(sticky="w", row=3, column=0)

        self.loader_button = Button(self.frame, text="Load",
                                    command=lambda: self.controller.open_file_dialog(self.config_file, file_type='csv'))

    def grid_load_button(self):
        if self.radio.get() > 1:
            self.loader_button.grid(sticky="w", row=self.radio.get(), column=1)
        else:
            self.loader_button.grid_forget()

    def finalize(self):
        if self.radio.get() > 1 and not self.config_file.get():
            self.controller.raise_error_message("Please provide a submit directory.")
            return False
        return True

    def get_config_file(self):
        if self.radio.get() == 1:
            return None
        return self.config_file.get()

    def is_watch(self):
        return self.radio.get() == 3
