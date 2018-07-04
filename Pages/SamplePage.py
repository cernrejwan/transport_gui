from BasePage import *
from Utils.ElementsHandler import *


class SamplePage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Sample")
        self.kwargs = dict([('_'.join(key.split("_")[1:]), value)
                            for key, value in kwargs.iteritems() if key.startswith("sample")])

        # vars:
        self.vars_list = ['sample_element', 'sample_isotope', 'sample_xs_file', 'sample_atob']

        self.sample_element = StringVar(self, self.kwargs.get('element', ''))
        self.sample_isotope = IntVar(self, self.kwargs.get('isotope', 0))
        self.sample_xs_file = StringVar(self, self.kwargs.get('xs_file', ''))
        self.sample_atob = DoubleVar(self, self.kwargs.get('atob', 0.0))

        # gui:
        Label(self.frame, text="Please specify the sample's properties").grid(row=0, columnspan=3)
        Label(self.frame, text="Element:").grid(row=1, column=0)
        Entry(self.frame, textvariable=self.sample_element).grid(row=1, column=1)

        Label(self.frame, text="Isotope (atomic mass):").grid(row=2, column=0)
        Entry(self.frame, textvariable=self.sample_isotope).grid(row=2, column=1)

        Label(self.frame, text="Sample cross section file:").grid(row=3, column=0)
        Entry(self.frame, textvariable=self.sample_xs_file).grid(row=3, column=1)
        Button(self.frame, text="Select",
               command=lambda: self.controller.open_file_dialog(self.sample_xs_file, file_type='xs')).grid(row=3, column=2)

        Label(self.frame, text="Atoms per barn:").grid(row=4, column=0)
        Entry(self.frame, textvariable=self.sample_atob).grid(row=4, column=1)
        Button(self.frame, text="Calculate",
               command=lambda: self.controller.open_atob_window(self.get_material_name(), self.sample_isotope.get(),
                                                                self.sample_atob, **self.kwargs)).grid(row=4, column=2)

    def get_material_name(self):
        if not isotope_exists(self.sample_element.get(), self.sample_isotope.get()):
            return '\nERROR: Material not found\nor isotope does not match to the element.'
        return get_full_name(self.sample_element.get().title(), self.sample_isotope.get())

    def finalize(self):
        if not self.show_page.get():
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

        if self.sample_atob.get() <= 0:
            self.controller.raise_error_message('Atoms per barn must be greater than zero.')
            return False

        return True

    def get_data(self):
        if not self.show_page.get():
            return ''

        data = "Sample: {sample}"
        data += '\nXS file: {path}'''.format(sample=self.get_material_name(), path=self.sample_xs_file.get())
        data += '\nAtoms per barn: ' + str(self.sample_atob.get())
        return data

    def get_cmd(self):
        if not self.show_page.get():
            return ''

        eff = self.controller.paths['efficiency_file']
        xs = self.sample_xs_file.get()
        xstotal = get_xs_file(self.sample_element.get(), self.sample_isotope.get())
        atob = self.sample_atob.get()
        return '--xs {xs} --atob {atob} --xstotal {xstotal} --eff {eff}'.format(xs=xs, atob=atob, xstotal=xstotal, eff=eff)
