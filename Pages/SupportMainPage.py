from BasePage import *
from SupportPage import SupportPage


class SupportMainPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Support")

        # vars
        self.support_layers = StringVar(self, 1)
        self.support_pages = list()

        # gui
        self.use.set(0)
        Checkbutton(self, text="Use support layer(s)", variable=self.use, command=self.show).pack(side=TOP)
        Label(self.frame, text="Number of support layers:").grid(row=1, column=0)
        Entry(self.frame, textvariable=self.support_layers).grid(row=1, column=1)

    def finalize(self):
        if not self.use.get():
            return True

        try:
            num_layers = int(self.support_layers.get())
        except:
            self.controller.raise_error_message("Number of support layers must be an integer.")
            return False

        if num_layers < 1 or num_layers > 100:
            self.controller.raise_error_message("Number of support layers must be between 1 and 100.")
            return False

        if num_layers == len(self.support_pages):
            return True

        if len(self.support_pages) > 0:
            for page in self.support_pages:
                self.controller.remove_page(page)
            self.support_pages = list()

        for i in range(num_layers):
            page = SupportPage(self.parent, self.controller, i+1)
            self.controller.add_page(page)
            self.support_pages.append(page)

        return True
