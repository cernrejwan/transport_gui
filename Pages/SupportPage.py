from BasePage import *
from MaterialWindow import MaterialWindow


class SupportPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Support " + str(kwargs.get('index')))
        self.index = kwargs['index']
        prefix = "support{}".format(self.index)
        self.kwargs = {key.split("_")[1]: value for key, value in kwargs.iteritems() if key.startswith(prefix)}

        # vars:
        self.vars_list = ['material', 'composition', 'atob']

        self.support_materials = self.get_support_materials(self.controller.paths['support_materials_path'])
        self.materials_list = self.support_materials.keys() + ['Other']
        self.material = StringVar(self, self.kwargs.get('material', self.materials_list[0]))
        self.molecular_mass = DoubleVar(self)
        self.atob = DoubleVar(self, self.kwargs.get('atob', 0.0))
        self.density = DoubleVar(self, self.kwargs.get('density', 0.0))
        self.material_window = MaterialWindow(self, self.controller, self.material, density_var=self.density, **self.kwargs)

        # gui:
        self.frame.pack()
        Label(self.frame, text="Material for the total cross section:").grid(row=1, column=0, columnspan=2)
        OptionMenu(self.frame, self.material, *self.materials_list,
                   command=self.set_material).grid(row=1, column=2)

        Label(self.frame, text="Atoms per barn:").grid(row=4, column=0)
        Entry(self.frame, textvariable=self.atob).grid(row=4, column=1)
        Button(self.frame, text="Calculate",
               command=lambda: self.controller.open_atob_window(self.material_window.get_material_name(),
                                                                self.molecular_mass.get(), self.atob,
                                                                density_var=self.density, **self.kwargs)).grid(row=4, column=2)

        # self.atob_widget = AtobCalculator(self.frame, self.controller, self.molecular_mass, **self_kwargs)
        # self.atob_widget.grid(row=5, columnspan=3)

        self.material_details = Frame(self.frame)
        self.set_material(self.material.get(), popup=False)

    @staticmethod
    def get_support_materials(support_materials_path):
        support_materials = dict()
        files_list = os.listdir(support_materials_path)
        for material in files_list:
            name = material.split('.')[0]
            values = pd.read_csv(os.path.join(support_materials_path, material), header=None, index_col=0,
                                 squeeze=True).to_dict()
            values['formula'] = eval(values['formula'])
            support_materials[name] = values
        return support_materials

    def set_material(self, material, popup=True):
        self.material_window.set_material(material, self.support_materials)
        if popup:
            self.open_material_window()
            return

        if material != "Other":
            self.density.set(self.support_materials[material]['density'])

        mass = self.material_window.get_total_mass()
        self.molecular_mass.set(mass)
        self.show_material_details(self.material_window.get_formula(), self.molecular_mass.get())

    def open_material_window(self):
        self.density.set(0.0)
        new_window = Toplevel(self.controller)
        self.material_window.show(new_window)
        Button(new_window, text="OK", command=lambda: self.close_elements_session(new_window)).pack(side=BOTTOM)

    def show_material_details(self, formula, molecular_mass):
        self.material_details.grid_forget()
        self.material_details = Frame(self.frame)
        self.material_details.grid(row=2, columnspan=3)
        Label(self.material_details, text='Material: ' + formula).grid(row=2, columnspan=3)
        Label(self.material_details, text='Molecular mass: {} * 1.66e-24 g'.format(molecular_mass)).grid(row=3, columnspan=3)
        if self.density.get() > 0:
            Label(self.material_details, text=u'Density: {} g / cm\xb3'.format(self.density.get())).grid(row=4,
                                                                                                         columnspan=3)

        if self.material.get() == 'Other':
            Button(self.material_details, text="Load", command=self.load_material).grid(row=5, column=0)
            Button(self.material_details, text="Change", command=self.open_material_window).grid(row=5, column=1)
            Button(self.material_details, text="Save", command=self.save_material).grid(row=5, column=2)

    def save_material(self):
        df = pd.Series(self.get_vars(use_prefix=False))
        self.controller.save_df(df)

    def load_material(self):
        pass

    def close_elements_session(self, parent):
        finalized = self.material_window.finalize()
        if not finalized:
            return

        self.molecular_mass.set(self.material_window.get_total_mass())
        parent.destroy()
        self.show_material_details(self.material_window.get_formula(), self.molecular_mass.get())

    def get_data(self):
        data = self.material_window.get_data()
        data += "\nAtoms per barn: " + str(self.atob.get())
        # data += "\n" + self.atob_widget.get_data()
        return data

    def get_cmd(self):
        total_atob = self.atob.get()
        return self.material_window.get_cmd(total_atob)

    def get_vars(self, use_prefix=True):
        material = self.material.get()
        prefix = 'support{}_'.format(self.index) if use_prefix else ''
        vars_dict = {prefix + "material": material}
        if material == 'Other':
            vars_dict[prefix + "formula".format(self.index)] = self.material_window.get()

        # atob_dict = self.atob_widget.get_vars()
        # vars_dict.update({prefix + key: value for key, value in atob_dict.iteritems()})
        return vars_dict

    # def finalize(self):
    #     atob_finalized = self.atob_widget.finalize()
    #     elements_finalized = self.material_window.finalize()
    #
    #     return atob_finalized
