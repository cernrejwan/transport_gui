from BasePage import *
from Utils.Chemistry import *
from AtobWidget import AtobWidget


class SamplePage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Sample")

        # vars:
        self.vars_list = ['sample_element', 'sample_isotope', 'sample_xs_file']

        self.sample_element = StringVar(self, kwargs.get('sample_element', ''))
        self.sample_isotope = IntVar(self, kwargs.get('sample_isotope', ''))
        self.sample_xs_file = StringVar(self, kwargs.get('sample_xs_file', ''))

        # gui:
        self.use.set(0)
        self.atob_widget = AtobWidget(self.frame, self.controller, self.sample_isotope)

        Checkbutton(self, text="Use sample", variable=self.use, command=self.show).pack(side=TOP)

        Label(self.frame, text="Please specify the sample's properties").grid(row=0, columnspan=3)
        Label(self.frame, text="Element:").grid(row=1, column=0)
        Entry(self.frame, textvariable=self.sample_element).grid(row=1, column=1)

        Label(self.frame, text="Isotope (atomic mass):").grid(row=2, column=0)
        Entry(self.frame, textvariable=self.sample_isotope).grid(row=2, column=1)

        Label(self.frame, text="Sample cross section file:").grid(row=3, column=0)
        Entry(self.frame, textvariable=self.sample_xs_file).grid(row=3, column=1)
        Button(self.frame, text="Select",
               command=lambda: self.controller.open_file_dialog(self.sample_xs_file, file_type='xs')).grid(row=3, column=2)

        self.atob_widget.grid(row=4, columnspan=3)

    def finalize(self):
        if not self.use.get():
            return True

        symbol = self.sample_element.get().title()
        if not element_exists(symbol):
            self.controller.raise_error_message('Element does not exist.\nPlease check spelling.')
            return False

        if not isotope_exists(symbol, self.sample_isotope.get()):
            self.controller.raise_error_message('Isotope does not match to element.')
            return False

        if not os.path.exists(self.sample_xs_file.get()):
            self.controller.raise_error_message('Cross section file does not exist.\nPlease try again.')
            return False

        finalized = self.atob_widget.finalize()
        return finalized

    def get_data(self):
        data = '''Sample: {sample}
        XS file: {path}'''.format(sample=get_full_name(self.sample_element.get().title(), self.sample_isotope.get()),
                                  path=self.sample_xs_file.get())
        data += '\n' + self.atob_widget.get_data()
        return data

    def get_cmd(self):
        xs = self.sample_xs_file.get()
        xstotal = get_xs_file(self.sample_element.get(), self.sample_isotope.get())
        atob = self.atob_widget.get_atob()
        return '--xs {xs} --atob {atob} --xstotal {xstotal}'.format(xs=xs, atob=atob, xstotal=xstotal)
