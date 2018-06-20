from BasePage import *


class FinalPage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Almost done...")
        self.frame.pack()

        Label(self.frame, text="Summary is presented in a new window.\nPlease verify the correctness of the input.").pack()
        Label(self.frame, text="Press the prev button if you want to change anything.").pack()
        Label(self.frame, text="Press the next button for submitting the job.").pack()

