from BasePage import *
from AtobWidget import AtobWidget
from MaterialWindow import MaterialWindow
from Utils.OptionMenus import support_materials
from ttk import Separator


class SupportPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Support " + str(kwargs.get('index')))
        self.index = kwargs['index']

        # vars:
        self.vars_list = ['material', 'composition']

        self.materials_list = support_materials.keys() + ['Other']
        self.material = StringVar(self, kwargs.get('material', self.materials_list[0]))
        self.molecular_mass = DoubleVar(self)
        self.material_composition = MaterialWindow(self, self.controller, self.material)

        prefix = "support{}".format(self.index)
        atob_kwargs = {key.split("_")[1]: value for key, value in kwargs.iteritems() if key.startswith(prefix)}

        # gui:
        self.frame.pack()
        Label(self.frame, text="Material for the total cross section:").grid(row=1, column=0, columnspan=2)
        OptionMenu(self.frame, self.material, *self.materials_list,
                   command=self.set_material).grid(row=1, column=2)

        self.atob_widget = AtobWidget(self.frame, self.controller, self.molecular_mass, **atob_kwargs)
        self.atob_widget.grid(row=5, columnspan=3)

        self.material_details = Frame(self.frame)
        self.set_material(self.material.get())

    def set_material(self, material):
        self.material_composition.set_material(material)
        if material != "Other":
            self.atob_widget.density.set(support_materials[material]['density'])
            self.molecular_mass.set(self.material_composition.get_total_mass())
            self.show_material_details(self.material_composition.get_formula(), self.molecular_mass.get(), allow_change=False)
        else:
            self.open_material_window()

    def open_material_window(self):
        self.atob_widget.density.set(0.0)
        new_window = Toplevel(self.controller)
        self.material_composition.show(new_window)
        Button(new_window, text="OK", command=lambda: self.close_elements_session(new_window)).pack(side=BOTTOM)

    def show_material_details(self, formula, molecular_mass, allow_change):
        self.material_details.grid_forget()
        self.material_details = Frame(self.frame)
        self.material_details.grid(row=2, columnspan=3)
        Label(self.material_details, text='Material: ' + formula).grid(row=2, columnspan=2)
        if allow_change:
            Button(self.material_details, text="Change", command=self.open_material_window).grid(row=2, column=2)
        Label(self.material_details, text='Molecular mass: {} * 1.66e-24 g'.format(molecular_mass)).grid(row=3, columnspan=2)
        Separator(self.material_details, orient="horizontal").grid(row=4, columnspan=3)

    def close_elements_session(self, parent):
        finalized = self.material_composition.finalize()
        if not finalized:
            return

        self.molecular_mass.set(self.material_composition.get_total_mass())
        parent.destroy()
        self.show_material_details(self.material_composition.get_formula(), self.molecular_mass.get(), allow_change=True)

    def get_data(self):
        data = self.material_composition.get_data()
        data += "\n" + self.atob_widget.get_data()
        return data

    def get_cmd(self):
        total_atob = self.atob_widget.get_atob()
        return self.material_composition.get_cmd(total_atob)

    def get_vars(self):
        material = self.material.get()
        vars_dict = {"support{}_material".format(self.index): material}
        if material == 'Other':
            vars_dict["support{}_composition".format(self.index)] = self.material_composition.get()

        atob_dict = self.atob_widget.get_vars()
        vars_dict.update({"support{}_".format(self.index) + key: value for key, value in atob_dict.iteritems()})
        return vars_dict

    def finalize(self):
        atob_finalized = self.atob_widget.finalize()
        # elements_finalized = self.elements_window.finalize()

        return atob_finalized
