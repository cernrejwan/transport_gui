from BasePage import *


class SimulationPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Simulation")

        # vars:
        self.vars_list = ['particle', 'time_offset', 'beam_RMS', 'length', 'angle']

        self.particle = StringVar(self, kwargs['particle'])
        self.time_offset = DoubleVar(self, kwargs['time_offset'])
        self.beam_RMS = DoubleVar(self, kwargs['beam_RMS'])
        self.gravity = IntVar(self, kwargs['gravity'])

        self.length = DoubleVar(self, kwargs.get('length', kwargs[self.controller.get_ear() + '_length']))
        self.angle = DoubleVar(self, kwargs.get('angle', kwargs[self.controller.get_ear() + '_max_angle']))

        # gui:
        Label(self.frame, text="Select particle type:").grid(row=0, column=0)
        OptionMenu(self.frame, self.particle, "Neutrons", "Photons").grid(row=0, column=1)

        Label(self.frame, text="Flight path length:").grid(row=1, column=0)
        Entry(self.frame, textvariable=self.length).grid(row=1, column=1)
        Label(self.frame, text="[m]").grid(row=1, column=2)

        Label(self.frame, text="Max angle for resampling:").grid(row=2, column=0)
        Entry(self.frame, textvariable=self.angle).grid(row=2, column=1)
        Label(self.frame, text="[degrees]").grid(row=2, column=2)

        Label(self.frame, text="RMS of the proton beam:").grid(row=3, column=0)
        OptionMenu(self.frame, self.beam_RMS, '0', '7e-9', '14e-9').grid(row=3, column=1)
        Label(self.frame, text="[s]").grid(row=3, column=2)

        Label(self.frame, text="Time offset:").grid(row=4, column=0)
        Entry(self.frame, textvariable=self.time_offset).grid(row=4, column=1)
        Label(self.frame, text="[s]").grid(row=4, column=2)

        Checkbutton(self.frame, text="Use gravity?", variable=self.gravity).grid(row=5, column=0)

    def get_cmd(self):
        if self.particle.get() == 'Neutrons':
            cmd = '-p 8'
        else:
            cmd = '-p 7'

        cmd += ' -L ' + str(self.length.get())
        cmd += ' -a ' + str(self.angle.get())
        cmd += ' -S ' + str(self.beam_RMS.get())
        cmd += ' --t0 ' + str(self.time_offset.get())
        if self.gravity.get():
            cmd += ' --gravity'

        return cmd

    def get_data(self):
        data = "Particle = {p}\nLength = {L} [m]\nAngle = {a} [deg]\nBeam RMS = {S} [s]\nTime offset = {t} [s]\nUse gravity? {g}".format(
            p=self.particle.get(), L=self.length.get(), a=self.angle.get(), S=self.beam_RMS.get(),
            t=self.time_offset.get(), g='Yes' if self.gravity.get() else 'No')
        return data

    def finalize(self):
        ear = self.controller.get_ear()
        max_angle = float(self.controller.configs_dict[ear + '_max_angle'])
        if self.angle.get() > max_angle:
            self.controller.raise_error_message("Angle must be smaller than {0} for {1}.".format(max_angle, ear))
            return False
        return True
