from Tkinter import *
from tkFont import Font
from Utils.ToolTip import ToolTip


class IsotopesWindow:
    def __init__(self, parent, controller, element):
        self.parent = parent
        self.element = element
        self.controller = controller

        self.title_font = Font(family='Helvetica', size=15, weight="bold", slant="italic")
        Label(self.parent, text='Isotopic abundance for element:\n{} (atomic number: {})'.format(element.name, element.atomic_num),
              font=self.title_font).pack(side="top", fill="x", pady=10)

        if element.no_data:
            txt = "Unfortunately, natural abundance of this element is missing.\nPlease provide the isotopes and their fraction (%)."
        else:
            txt = "Here is the natural abundance for the selected element.\nFeel free to change the composition."

        Label(self.parent, text=txt).pack()

        self.isotopes_frame = Frame(self.parent)
        Label(self.isotopes_frame, text="Isotope").grid(row=0, column=0)
        fraction = Label(self.isotopes_frame, text="Fraction")
        fraction.grid(row=0, column=1)
        ToolTip(fraction, "The fraction of the isotope in percents, e.g. 99.9")

        i = 1
        for isotope, fraction_var in element.isotopes:
            Label(self.isotopes_frame, text=isotope, width=8).grid(row=i, column=0)
            Entry(self.isotopes_frame, textvariable=fraction_var, width=8).grid(row=i, column=1)
            i += 1

        self.isotopes_frame.pack()

        Button(self.parent, text="Save", command=self.finalize).pack(side=RIGHT)

    def finalize(self):
        if not self.element.is_valid():
            self.controller.raise_error_message('Fractions should sum up to 1')
        else:
            self.parent.destroy()
