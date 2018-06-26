from Tkinter import *
from Utils.Chemistry import *


class AtobWidget(Frame):
    def __init__(self, parent, controller, mass, show_atob=True, **kwargs):
        Frame.__init__(self, parent)
        self.mass = mass
        self.controller = controller

        # vars:
        self.vars_list = ['sigma', 'atob', 'density', 'thickness', 'radio']

        self.sigma = DoubleVar(self, kwargs.get('sigma', 0))
        self.atob = DoubleVar(self, kwargs.get('atob', 0))
        self.density = DoubleVar(self, kwargs.get('density', 0))
        self.thickness = DoubleVar(self, kwargs.get('thickness', 0))
        self.radio = IntVar(0)
        if 'density' not in kwargs or kwargs['density'] == 0:
            self.radio.set(1 if 'sigma' in kwargs else 2)

        # gui:
        txt = "Fill in one of the following options regarding your sample.\nThe number of atoms per barn will be calculated automatically"
        Label(self, text=txt).grid(row=0, column=0, columnspan=3)

        Radiobutton(self, variable=self.radio, value=0, text="Density:\nThickness:").grid(sticky="W", row=1, column=0, rowspan=2)
        self.density_entry = Entry(self, textvariable=self.density)
        self.density_entry.bind("<Button-1>", lambda x: self.set_radio(0))
        self.density_entry.grid(row=1, column=1)
        Label(self, text=u"[g/cm\xb3]").grid(sticky="W", row=1, column=2)

        self.thickness_entry = Entry(self, textvariable=self.thickness)
        self.thickness_entry.bind("<Button-1>", lambda x: self.set_radio(0))
        self.thickness_entry.grid(row=2, column=1)
        Label(self, text="[cm]").grid(sticky="W", row=2, column=2)

        Radiobutton(self, variable=self.radio, value=1, text="Areal density:").grid(sticky="W", row=3, column=0)
        self.sigma_entry = Entry(self, textvariable=self.sigma)
        self.sigma_entry.bind("<Button-1>", lambda x: self.set_radio(1))
        self.sigma_entry.grid(row=3, column=1)
        Label(self, text=u"[g/cm\xb2]").grid(sticky="W", row=3, column=2)

        if show_atob:
            Radiobutton(self, variable=self.radio, value=2, text="Atoms per barn:").grid(sticky="W", row=4, column=0)
            self.atob_entry = Entry(self, textvariable=self.atob)
            self.atob_entry.bind("<Button-1>", lambda x: self.set_radio(2))
            self.atob_entry.grid(row=4, column=1)
            Label(self, text="[1/barn]").grid(sticky="W", row=4, column=2)

            buttons_frame = Frame(self)
            buttons_frame.grid(row=5, columnspan=3)
            Button(buttons_frame, text="Reset", command=self.reset).grid(row=0, column=0)
            Button(buttons_frame, text="Calculate", command=self.calc_atob).grid(row=0, column=1)

    def set_radio(self, value):
        self.radio.set(value)
        self.density_entry.config({"background": "Grey"})
        self.thickness_entry.config({"background": "Grey"})
        self.sigma_entry.config({"background": "Grey"})
        self.atob_entry.config({"background": "Grey"})

        if value == 0:
            self.density_entry.config({"background": "White"})
            self.thickness_entry.config({"background": "White"})
        elif value == 1:
            self.sigma_entry.config({"background": "White"})
        else:
            self.atob_entry.config({"background": "White"})

    def calc_atob(self):
        mass = self.mass.get()
        if not mass:
            self.controller.raise_error_message("Please specify the material first.")
            return

        if self.radio.get() == 0:
            atob, sigma = calc_atob_by_density(mass, self.density.get(), self.thickness.get())
            self.sigma.set(sigma)
        else:
            atob = calc_atob_by_sigma(mass, self.sigma.get())

        self.atob.set(float('{:0.5e}'.format(atob)))

    def reset(self):
        self.density.set(0.0)
        self.thickness.set(0.0)
        self.sigma.set(0.0)
        self.atob.set(0.0)

    def get_data(self):
        data = ''
        if self.radio.get() == 0:
            data += u'Density = {density} [g/cm\xb3]\nThickness = {thickness} [mm]\n'.format(density=self.density.get(),
                                                                                             thickness=self.thickness.get())
        elif self.radio.get() == 1:
            data += u'Aerial density = {:0.3e} [g/cm\xb2]\n'.format(self.sigma.get())
        data += 'Atoms per barn = {:0.3e} [1/barn]'.format(self.atob.get())
        return data

    def get_atob(self):
        return self.atob.get()

    def get_vars(self):
        vars_dict = dict()
        vars_dict['density'] = 0
        if self.radio.get() == 0:
            vars_dict['density'] = self.density.get()
            vars_dict['thickness'] = self.thickness.get()
            vars_dict['sigma'] = self.sigma.get()
        elif self.radio.get() == 1:
            vars_dict['sigma'] = self.sigma.get()
        vars_dict['atob'] = self.atob.get()
        return vars_dict

    def finalize(self):
        self.calc_atob()
        if self.atob.get() <= 0:
            txt = "Atoms per barn should be greater than zero.\nSomething went wrong, please try again."
            self.controller.raise_error_message(txt)
            self.reset()
            return False
        return True
