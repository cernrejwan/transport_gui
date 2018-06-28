from BasePage import *
from Pages.SupportPage import SupportPage


class SupportMainPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Support")

        # vars
        self.vars_list = ['support_layers']
        self.support_layers = IntVar(self, kwargs.get('support_layers', 1))
        self.support_pages_exist = 0

        if 'support_layers' not in kwargs:
            self.use.set(0)

        self.kwargs = {key: value for key, value in kwargs.iteritems() if key.startswith("support")}

        # gui
        Checkbutton(self, text="Use support layer(s)", variable=self.use, command=self.show).pack(side=TOP)
        self.show()
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

        if self.support_pages_exist > num_layers:
            for i in range(self.support_pages_exist, num_layers, -1):
                self.controller.remove_page("SupportPage" + str(i))
        else:
            for i in range(self.support_pages_exist + 1, num_layers + 1):
                self.controller.add_page(SupportPage, "SupportPage" + str(i), index=i, **self.kwargs)
        self.support_pages_exist = num_layers
        return True
