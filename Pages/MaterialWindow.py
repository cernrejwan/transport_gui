from Tkinter import *
from Utils.ToolTip import ToolTip
from Utils.Chemistry import *
from tkFont import Font
from ElementWindow import Element


class MaterialWindow:
    def __init__(self, parent, controller, material_var):
        self.controller = controller
        self.parent = parent
        self.material_var = material_var
        self.type_var = StringVar(self.parent, "Number of atoms")
        self.elements_dict = dict()
        self.curr_row = 1

    def set_material(self, material):
        self.curr_row = 1
        self.elements_dict = dict()

        if material != 'Other':
            formula = default_values['cross_section']['materials'][material]['formula']
            self.type_var.set("Mass fraction")
            for element, fraction in formula:
                self.add_element(element, fraction)
        else:
            self.add_element()

    def add_element(self, symbol='', fraction=0.0):
        symbol_var = StringVar(self.controller, symbol)
        fraction_var = DoubleVar(self.controller, fraction)
        self.elements_dict[self.curr_row] = {'symbol': symbol_var, 'fraction': fraction_var, 'element': None}
        self.curr_row += 1

    def show_element(self, frame, row):
        Entry(frame, textvariable=self.elements_dict[row]['symbol'], width=8).grid(row=row, column=0)
        Entry(frame, textvariable=self.elements_dict[row]['fraction'], width=8).grid(row=row, column=1)
        Button(frame, text="Change", command=lambda: self.change_composition(row)).grid(row=row, column=2)

    def add_element_and_show(self, frame):
        row = self.curr_row
        self.add_element()
        self.show_element(frame, row)

    def change_composition(self, row):
        curr_element = self.elements_dict[row]
        element_symbol = curr_element['symbol'].get().title()
        if not element_exists(element_symbol):
            self.controller.raise_error_message('Element does not exist.\nPlease check spelling.')
            return

        if not curr_element['element'] or curr_element['element'].symbol != element_symbol:
            curr_element['element'] = Element(self.parent, self.controller, element_symbol)

        isotopes_window = Toplevel(self.controller)
        curr_element['element'].show(isotopes_window)

    def finalize(self):
        if not self.elements_dict[1]['symbol'].get():
            self.controller.raise_error_message('Please specify at least one element.')
            return False

        if self.type_var.get() == 'Mass fraction (%)':
            cumulative_sum = sum([element['fraction'].get() for element in self.elements_dict.values()])
            if cumulative_sum != 100:
                self.controller.raise_error_message('Fractions should sum up to 100%')
                return False
        else:   # num atoms
            if not self.elements_dict[1]['fraction'].get():
                self.controller.raise_error_message('Each element has to have at least 1 atom.')
                return False

        new_dict = {}
        for i, item in self.elements_dict.iteritems():
            if not item['element']:
                new_dict[i] = item
                new_dict[i]['element'] = Element(self.parent, self.controller, item['symbol'].get())
        self.elements_dict.update(new_dict)

        return True

    def get_total_mass(self):
        total_mass = 0
        for item in self.elements_dict.values():
            element_mass = item['element'].get_avg_mass_number()
            total_mass += item['fraction'].get() * element_mass   # same formula for num atoms or mass fraction
        return total_mass

    def get_formula(self):
        res = ''
        form = '{}{:0.0f} ' if self.type_var.get() == 'Number of atoms' else '{} ({:0.2f}%) '
        for item in self.elements_dict.values():
            symbol = item['symbol'].get().title()
            frac = item['fraction'].get()
            if self.type_var.get() != "Number of atoms":
                frac = frac * 100
            res += form.format(symbol, frac)
        return res

    def get_cmd(self, total_atob):
        cmd = ''
        for item in self.elements_dict.values():
            cmd += item['element'].get_cmd(total_atob)
        return cmd

    def get_data(self):
        data = "Material: {} ({})".format(self.get_formula(), self.material_var.get())
        data += '\nMolecular mass: {} * 1.66e-24 g'.format(self.get_total_mass())
        return data

    def show(self, window):
        frame = Frame(window)
        frame.pack()
        title_font = Font(family='Helvetica', size=15, weight="bold", slant="italic")
        Label(frame, text='Elements composition', font=title_font).pack(side="top", fill="x", pady=10)

        Label(frame, text="Provide the material's composition by:").pack()
        OptionMenu(frame, self.type_var, "Number of atoms", "Mass fraction",
                   command=self.set_fraction_input_method).pack()
        Label(frame, text="(hover over the headers for explanation)").pack()

        elements_frame = Frame(frame)
        symbol = Label(elements_frame, text="Element")
        symbol.grid(row=0, column=0)
        ToolTip(symbol, "The chemical symbol of the element\nfor example for carbon use C")
        self.num_atoms_label = Label(elements_frame, text="Num atoms")
        self.fraction_label = Label(elements_frame, text="Mass frac")
        ToolTip(self.fraction_label, "The fraction of mass (between 0 and 1)")
        self.num_atoms_label.grid(row=0, column=1)
        composition = Label(elements_frame, text="Composition")
        composition.grid(row=0, column=2)
        ToolTip(composition,
                "Change the isotopic composition of the element\nIf not changed, the natural abundance is taken")

        elements_frame.pack()

        if len(self.elements_dict) == 0:
            self.add_element_and_show(elements_frame)
        else:
            for row in self.elements_dict.keys():
                self.show_element(elements_frame, row)

        Button(frame, text="Add element", command=lambda: self.add_element_and_show(elements_frame)).pack(side=BOTTOM)

    def set_fraction_input_method(self, type_var):
        if type_var == "Number of atoms":
            self.fraction_label.grid_forget()
            self.num_atoms_label.grid(row=0, column=1)
        else:
            self.num_atoms_label.grid_forget()
            self.fraction_label.grid(row=0, column=1)
