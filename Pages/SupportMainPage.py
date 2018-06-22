from BasePage import *


class SupportMainPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Support")

        # vars
        self.support_layers = IntVar(self, 1)
        self.support_pages_exist = 0

        # gui
        self.use.set(0)
        Checkbutton(self, text="Use support layer(s)", variable=self.use, command=self.show).pack(side=TOP)
        Label(self.frame, text="Number of support layers:").grid(row=1, column=0)
        Entry(self.frame, textvariable=self.support_layers).grid(row=1, column=1)

    def finalize(self):
        if not self.use.get():
            return True

        num_layers = int(self.support_layers.get())

        if num_layers < 1 or num_layers > 100:
            self.controller.raise_error_message("Number of support layers must be between 1 and 100.")
            return False

        if num_layers == self.support_pages_exist:
            return True

        self.controller.remove_page("SupportPage", count=self.support_pages_exist)
        self.controller.add_page("SupportPage", count=num_layers)
        self.support_pages_exist = num_layers
        return True
