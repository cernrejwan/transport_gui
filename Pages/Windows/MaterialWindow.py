from Tkinter import *
from tkFont import Font
from ElementWindow import Element
from Utils.ElementsHandler import *
from Utils.SupportMaterialsHandler import support_materials
from Utils.ToolTip import ToolTip


class MaterialWindow:
    def __init__(self, parent, controller, material_name, density_var, **kwargs):
        self.controller = controller
        self.parent = parent
        self.material = material_name
        self.type_var = StringVar(self.parent, "Number of atoms")
        self.elements_dict = dict()
        self.curr_row = 1
        self.formula = kwargs.get('formula', [])
        if type(self.formula) == str:
            self.formula = eval(self.formula)
            if type(self.formula) == str:
                self.formula = eval(self.formula)
        self.density = density_var
        self.set_material(self.material)

    def set_material(self, material):
        self.material = material
        self.curr_row = 1
        self.elements_dict = dict()
        self.type_var.set("Number of atoms")

        if material in support_materials:
            self.init_material_by_formula(support_materials[material]['formula'])
        elif self.formula:
            self.init_material_by_formula(self.formula)
        else:
            self.add_element()

    def init_material_by_formula(self, formula):
        total_fraction = 0
        for element, fraction, isotopes in formula:
            self.add_element(element, fraction, isotopes)
            total_fraction += fraction

        if total_fraction == 1:
            self.type_var.set("Mass fraction")

    def add_element(self, symbol='', fraction=0.0, isotopes=None):
        symbol_var = StringVar(self.controller, symbol)
        fraction_var = DoubleVar(self.controller, fraction)
        element = Element(self.parent, self.controller, symbol, isotopes) if symbol else None
        self.elements_dict[self.curr_row] = dict([('symbol', symbol_var), ('fraction', fraction_var), ('isotopes', element)])
        self.curr_row += 1

    def show_element(self, frame, row):
        Entry(frame, textvariable=self.elements_dict[row]['symbol'], width=8).grid(row=row, column=0)
        Entry(frame, textvariable=self.elements_dict[row]['fraction'], width=8).grid(row=row, column=1)
        Button(frame, text="Iso abund.", command=lambda: self.change_composition(row)).grid(row=row, column=2)

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

        if not curr_element['isotopes'] or curr_element['isotopes'].symbol != element_symbol:
            curr_element['isotopes'] = Element(self.parent, self.controller, element_symbol)

        isotopes_window = Toplevel(self.controller)
        curr_element['isotopes'].show(isotopes_window)
        self.elements_dict[row] = curr_element

    def finalize(self):
        if not self.elements_dict[1]['symbol'].get():
            self.controller.raise_error_message('Please specify at least one element.')
            return False

        if self.type_var.get() == 'Mass fraction':
            cumulative_sum = sum([element['fraction'].get() for element in self.elements_dict.values()])
            if abs(cumulative_sum - 1) > 1e-9:
                self.controller.raise_error_message('Fractions should sum up to 1.')
                return False
        else:   # num atoms
            if not self.elements_dict[1]['fraction'].get():
                self.controller.raise_error_message('Each element has to have at least 1 atom.')
                return False

        new_dict = dict()
        for i, item in self.elements_dict.iteritems():
            if item['symbol'].get() and not item['isotopes']:
                new_dict[i] = item
                new_dict[i]['isotopes'] = Element(self.parent, self.controller, item['symbol'].get())
        self.elements_dict.update(new_dict)

        return True

    def get_total_mass(self):
        total_mass = 0
        for item in self.elements_dict.values():
            element_mass = item['isotopes'].get_avg_mass_number() if item['isotopes'] else 0
            total_mass += item['fraction'].get() * element_mass   # same formula for num atoms or mass fraction
        return total_mass

    def get_formula(self):
        res = ''
        form = '{0}{1:0.0f} ' if self.type_var.get() == 'Number of atoms' else '{0} ({1:0.2f}%) '
        for item in self.elements_dict.values():
            symbol = item['symbol'].get().title()
            frac = item['fraction'].get()
            if not frac:
                continue

            if self.type_var.get() != "Number of atoms":
                frac = frac * 100
            res += form.format(symbol, frac)
        return res

    def get_cmd(self, total_atob):
        cmd = ''
        for item in self.elements_dict.values():
            cmd += item['isotopes'].get_cmd(total_atob)
        return cmd

    def get_material_name(self):
        return self.get_formula() if self.material == 'Other' else self.material

    def get_data(self):
        data = "Material: " + self.get_material_name()
        data += '\nMolecular mass: {0}'.format(round(self.get_total_mass(), 1))
        return data

    def show(self, window):
        frame = Frame(window)
        frame.pack()
        title_font = Font(family='Helvetica', size=15, weight="bold", slant="italic")
        Label(frame, text='Material composition', font=title_font).pack(side="top", fill="x", pady=10)

        Label(frame, text="Provide the material's composition by:").pack()
        OptionMenu(frame, self.type_var, "Number of atoms", "Mass fraction",
                   command=self.set_fraction_input_method).pack()
        Label(frame, text="(hover over the headers for explanation)").pack()

        elements_frame = Frame(frame)
        symbol = Label(elements_frame, text="Element (e.g. Au)")
        symbol.grid(row=0, column=0)
        ToolTip(symbol, "The chemical symbol of the element\nfor example for carbon use C")
        self.num_atoms_label = Label(elements_frame, text="Num atoms")
        self.fraction_label = Label(elements_frame, text="Mass frac")
        ToolTip(self.fraction_label, "The fraction of mass (between 0 and 1)")
        self.num_atoms_label.grid(row=0, column=1)

        elements_frame.pack()

        if len(self.elements_dict) == 0:
            self.add_element_and_show(elements_frame)
        else:
            for row in self.elements_dict.keys():
                self.show_element(elements_frame, row)

        Button(frame, text="Add element", command=lambda: self.add_element_and_show(elements_frame)).pack()

        density_frame = Frame(frame)
        Label(density_frame, text="Density (optional):").grid(row=0, column=0)
        Entry(density_frame, textvariable=self.density).grid(row=0, column=1)
        Label(density_frame, text=u"[g/cm\xb3]").grid(row=0, column=2)
        density_frame.pack()

    def set_fraction_input_method(self, type_var):
        if type_var == "Number of atoms":
            self.fraction_label.grid_forget()
            self.num_atoms_label.grid(row=0, column=1)
        else:
            self.num_atoms_label.grid_forget()
            self.fraction_label.grid(row=0, column=1)

    def get(self):
        result = list()
        for item in self.elements_dict.values():
            symbol = item['symbol'].get().title()
            frac = item['fraction'].get()
            if item['isotopes'].is_natural():
                composition = 'Natural'
            else:
                composition = item['isotopes'].get()
            result.append((symbol, frac, composition))
        return '"' + str(result) + '"'
