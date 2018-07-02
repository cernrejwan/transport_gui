from Tkinter import *
from Utils.ElementsHandler import *
from tkFont import Font
from Utils.ToolTip import ToolTip


class Element:
    def __init__(self, master, controller, element_symbol, isotopes=None):
        self.symbol = element_symbol.title()
        self.controller = controller

        info = symbols[self.symbol]
        self.name = info['Name']
        self.atomic_num = info['Atom_num']

        self.natural_abundance = abundance[self.symbol]

        if isotopes and isotopes != 'Natural':
            curr_abundance = dict()
            isotopes = eval(isotopes)
            for iso_num, fraction in isotopes:
                curr_abundance[iso_num] = fraction
        else:
            curr_abundance = self.natural_abundance

        self.isotopes = [(iso_num, DoubleVar(master, fraction)) for iso_num, fraction in curr_abundance.iteritems()]

    def is_valid(self):
        cumulative_sum = sum([float(frac.get()) for _, frac in self.isotopes])
        return (cumulative_sum == 1)

    def is_natural_abundance(self):
        for iso, frac in self.isotopes:
            if frac.get() != self.natural_abundance[iso]:
                return False
        return True

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
