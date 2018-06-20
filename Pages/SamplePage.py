from BasePage import *
from Utils.ElementsTools import *
from AtobWidget import AtobWidget


class SamplePage(BasePage):
    def __init__(self, parent, controller):
        BasePage.__init__(self, parent, controller, "Sample")

        # vars:
        self.element = StringVar(self)
        self.isotope = IntVar(self)
        self.sample_file = StringVar(self)

        # gui:
        self.use.set(0)
        self.atob_widget = AtobWidget(self.frame, self.controller, self.isotope)

        Checkbutton(self, text="Use sample", variable=self.use, command=self.show).pack(side=TOP)

        Label(self.frame, text="Please specify the sample's properties").grid(row=0, columnspan=3)
        Label(self.frame, text="Element:").grid(row=1, column=0)
        Entry(self.frame, textvariable=self.element).grid(row=1, column=1)

        Label(self.frame, text="Isotope (atomic mass):").grid(row=2, column=0)
        Entry(self.frame, textvariable=self.isotope).grid(row=2, column=1)

        Label(self.frame, text="Sample cross section file:").grid(row=3, column=0)
        Entry(self.frame, textvariable=self.sample_file).grid(row=3, column=1)
        Button(self.frame, text="Select",
               command=lambda: self.controller.open_file_dialog(self.sample_file, file_type='xs')).grid(row=3, column=2)

        self.atob_widget.grid(row=4, columnspan=3)

    def finalize(self):
        if not self.use.get():
            return True

        symbol = self.element.get().title()
        if not element_exists(symbol):
            self.controller.raise_error_message('Element does not exist.\nPlease check spelling.')
            return False

        if not isotope_exists(symbol, self.isotope.get()):
            self.controller.raise_error_message('Isotope does not match to element.')
            return False

        if not os.path.exists(self.sample_file.get()):
            self.controller.raise_error_message('Cross section file does not exist.\nPlease try again.')
            return False

        finalized = self.atob_widget.finalize()
        return finalized

    def get_data(self):
        data = '''Sample: {sample}
        XS file: {path}'''.format(sample=get_full_name(self.element.get().title(), self.isotope.get()),
                                  path=self.sample_file.get())
        data += '\n' + self.atob_widget.get_data()
        return data

    def get_cmd(self):
        xs = self.sample_file.get()
        xstotal = get_xs_file(self.element.get(), self.isotope.get())
        atob = self.atob_widget.get_atob()
        return '--xs {xs} --atob {atob} --xstotal {xstotal}'.format(xs=xs, atob=atob, xstotal=xstotal)
