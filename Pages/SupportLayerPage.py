from BasePage import *
from Pages.Windows.MaterialWindow import MaterialWindow
from Utils.SupportMaterialsHandler import *


class SupportLayerPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Support " + str(kwargs.get('index')))
        self.index = kwargs['index']
        prefix = "support" +str(self.index)
        self.page_name = "SupportPage" +str(self.index)
        self.kwargs = dict([('_'.join(key.split("_")[1:]), value)
                            for key, value in kwargs.iteritems() if key.startswith(prefix)])

        # vars:
        self.vars_list = ['material', 'formula', 'atob', 'density']

        self.materials_list = support_materials.keys() + ['Other']
        self.material = StringVar(self, self.kwargs.get('material', self.materials_list[0]))
        self.atob = DoubleVar(self, self.kwargs.get('atob', 0.0))
        self.density = DoubleVar(self, self.kwargs.get('density', 0.0))
        if self.material.get() != "Other":
            self.density.set(support_materials[self.material.get()]['density'])

        self.material_window = MaterialWindow(self, self.controller, self.material.get(), density_var=self.density, **self.kwargs)

        # gui:
        Label(self.frame, text="Material for the total cross section:").grid(row=1, column=0, columnspan=2)
        OptionMenu(self.frame, self.material, *self.materials_list,
                   command=self.set_material).grid(row=1, column=2)

        Label(self.frame, text="Atoms per barn:").grid(row=4, column=0)
        Entry(self.frame, textvariable=self.atob).grid(row=4, column=1)
        Button(self.frame, text="Calculate",
               command=lambda: self.controller.open_atob_window(self.material_window.get_material_name(),
                                                                self.material_window.get_total_mass(), self.atob,
                                                                density_var=self.density, **self.kwargs)).grid(row=4, column=2)

        self.material_details = Frame(self.frame)
        self.show_material_details()

    def set_material(self, material):
        self.material_window.set_material(material)

        if material in support_materials:
            self.density.set(support_materials[material]['density'])

        self.show_material_details()

    def open_material_window(self):
        self.density.set(0.0)
        new_window = Toplevel(self.controller)
        self.material_window.show(new_window)
        Button(new_window, text="OK", command=lambda: self.close_elements_session(new_window)).pack(side=BOTTOM)

    def show_material_details(self):
        self.material_details.grid_forget()
        self.material_details = Frame(self.frame)
        self.material_details.grid(row=2, columnspan=3)

        formula = self.material_window.get_formula()

        if formula:
            Label(self.material_details, text='Material: ' + formula).grid(row=2, columnspan=3)
            txt = 'Molecular mass: {0} * 1.66e-24 g'.format(self.material_window.get_total_mass())
            Label(self.material_details, text=txt).grid(row=3, columnspan=3)
            if self.density.get() > 0:
                txt = u'Density: {0} g/cm\xb3'.format(self.density.get())
                Label(self.material_details, text=txt).grid(row=4, columnspan=3)

        if self.material.get() == 'Other':
            Button(self.material_details, text="New", command=self.open_material_window).grid(row=5, column=0)
            Button(self.material_details, text="Load", command=self.load_material).grid(row=5, column=1)
            Button(self.material_details, text="Save", command=self.save_material).grid(row=5, column=2)

    def save_material(self):
        data_dict = self.get_vars(use_prefix=False)
        self.controller.save_to_csv(data_dict)

    def load_material(self):
        file_path = StringVar(self)
        self.controller.open_file_dialog(file_path, 'csv')
        name, kwargs = get_support_material(file_path.get())
        self.density.set(kwargs.get('density', 0.0))
        self.material_window = MaterialWindow(self, self.controller, name, density_var=self.density, **kwargs)
        self.show_material_details()

    def close_elements_session(self, parent):
        finalized = self.material_window.finalize()
        if not finalized:
            return

        parent.destroy()
        self.show_material_details()

    def get_data(self):
        if not self.show_page.get():
            return ''

        data = self.material_window.get_data()
        data += "\nAtoms per barn: " + str(round(self.atob.get(),3))
        return data

    def get_cmd(self):
        if not self.show_page.get():
            return ''

        total_atob = self.atob.get()
        return self.material_window.get_cmd(total_atob)

    def get_vars(self, use_prefix=True):
        if not self.show_page.get():
            return dict()

        material = self.material.get()
        prefix = 'support{0}_'.format(self.index) if use_prefix else ''
        vars_dict = dict()
        vars_dict[prefix + "material"] = material
        if material == 'Other':
            vars_dict[prefix + "formula".format(self.index)] = self.material_window.get()
        vars_dict[prefix + 'atob'] = self.atob.get()
        vars_dict[prefix + 'density'] = self.density.get()
        return vars_dict

    def finalize(self):
        if self.atob.get() <= 0:
            self.controller.raise_error_message('Atoms per barn must be greater than zero.')
            return False
        return self.material_window.finalize()
