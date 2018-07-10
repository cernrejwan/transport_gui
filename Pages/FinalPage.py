from BasePage import *


class FinalPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Almost done...")

        Label(self.frame, text="Summary is presented in a new window.").pack(anchor='w')
        Label(self.frame, text="Please verify the correctness of the input, and change if necessary.").pack(anchor='w')
        Label(self.frame, text="When done, click the submit button to launch the simulation.").pack(anchor='w')

    def get_next_button(self):
        return "Submit", self.controller.submit
