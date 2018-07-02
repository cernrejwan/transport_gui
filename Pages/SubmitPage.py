from BasePage import *


class SubmitPage(BasePage):
    def __init__(self, parent, controller, iters, **kwargs):
        BasePage.__init__(self, parent, controller, "Submission", has_prev=False)
        Label(self.frame, text=str(iters) + " jobs submitted successfully to HTCondor!", justify=LEFT).pack()

    def get_next_button(self):
        return 'Exit', self.controller.destroy
