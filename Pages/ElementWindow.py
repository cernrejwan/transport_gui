from Tkinter import *
from Utils.Chemistry import *
from tkFont import Font
from Utils.ToolTip import ToolTip


class Element:
    def __init__(self, master, controller, element_symbol, isotopes=None):
        self.symbol = element_symbol.title()
        self.controller = controller

        info = symbols[symbols['Symbol'] == self.symbol]
        self.name = info['Name'].values[0]
        self.atomic_num = info['Atom_num'].values[0]

        iso_abundance = abundance[abundance['symbol'] == 'H'].set_index('iso_num')['fraction']

        self.no_data = (iso_abundance.count() == 0)
        iso_abundance = iso_abundance.fillna(0)

        if isotopes and isotopes != 'Natural':
            iso_abundance[:] = 0
            for iso_num, fraction in isotopes:
                iso_abundance[iso_num] = fraction

        self.isotopes = [(iso_num, DoubleVar(master, fraction)) for iso_num, fraction in iso_abundance.iteritems()]

    def is_valid(self):
        cumulative_sum = sum([float(frac.get()) for _, frac in self.isotopes])
        return (cumulative_sum == 1)

    def get_avg_mass_number(self):
        weighted_sum = sum([frac.get() * iso_num for iso_num, frac in self.isotopes])
        return weighted_sum

    def get_cmd(self, total_atob):
        total_mass = self.get_avg_mass_number()
        cmd = ''
        for iso_num, frac in self.isotopes:
            atob = total_atob * frac.get() * iso_num / total_mass
            if atob > 0:
                xs_file = get_xs_file(self.symbol, iso_num)
                cmd += '--Sxs {xs_file} --Satob {atob} '.format(xs_file=xs_file, atob=atob)
        return cmd

    def show(self, window):
        self.window = window
        title_font = Font(family='Helvetica', size=15, weight="bold", slant="italic")
        header_txt = 'Isotopic abundance for element:\n{} (atomic number: {})'.format(self.name, self.atomic_num)
        Label(window, text=header_txt, font=title_font).pack(side="top", fill="x", pady=10)

        if self.no_data:
            txt = "Unfortunately, natural abundance of this element is missing.\nPlease provide the isotopes and their fraction (%)."
        else:
            txt = "Here is the natural abundance for the selected element.\nFeel free to change the composition."
        Label(window, text=txt).pack()

        isotopes_frame = Frame(window)
        Label(isotopes_frame, text="Isotope").grid(row=0, column=0)
        fraction = Label(isotopes_frame, text="Fraction")
        fraction.grid(row=0, column=1)
        ToolTip(fraction, "The fraction of the isotope in percents, e.g. 99.9")

        i = 1
        for isotope, fraction_var in self.isotopes:
            Label(isotopes_frame, text=isotope, width=8).grid(row=i, column=0)
            Entry(isotopes_frame, textvariable=fraction_var, width=8).grid(row=i, column=1)
            i += 1

        isotopes_frame.pack()
        Button(window, text="Save", command=self.finalize).pack(side=RIGHT)

    def finalize(self):
        if not self.is_valid():
            self.controller.raise_error_message('Fractions should sum up to 1')
        else:
            self.window.destroy()

    def get(self):
        result = list()
        for iso_num, frac in self.isotopes:
            if frac.get() > 0:
                result.append((iso_num, frac.get()))
        return str(result)
