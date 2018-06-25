from BasePage import *


class SimuParamsPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Simulation")

        # vars:
        self.particle = StringVar(self, "Neutrons")
        self.length = DoubleVar(self, default_values['EAR1']['-L'])
        self.angle = DoubleVar(self, default_values['EAR1']['-a'])
        self.time_offset = DoubleVar(self, default_values['--t0'])
        self.sigma = DoubleVar(self, default_values['-S'])

        # gui:
        self.frame.pack()
        Label(self.frame, text="Select particle type:").grid(row=0, column=0)
        OptionMenu(self.frame, self.particle, "Neutrons", "Photons").grid(row=0, column=1)

        Label(self.frame, text="Flight path length:").grid(row=1, column=0)
        Entry(self.frame, textvariable=self.length).grid(row=1, column=1)
        Label(self.frame, text="[m]").grid(row=1, column=2)

        Label(self.frame, text="Max angular opening for the transport:").grid(row=2, column=0)
        Entry(self.frame, textvariable=self.angle).grid(row=2, column=1)
        Label(self.frame, text="[degrees]").grid(row=2, column=2)

        Label(self.frame, text="RMS of the proton beam:").grid(row=3, column=0)
        OptionMenu(self.frame, self.sigma, '0', '7e-9', '14e-9').grid(row=3, column=1)
        Label(self.frame, text="[s]").grid(row=3, column=2)

        Label(self.frame, text="Time offset:").grid(row=4, column=0)
        Entry(self.frame, textvariable=self.time_offset).grid(row=4, column=1)
        Label(self.frame, text="[s]").grid(row=4, column=2)

    def get_cmd(self):
        if self.particle.get() == 'Neutrons':
            cmd = '-p 8'
        else:
            cmd = '-p 7'

        cmd += ' -L ' + str(self.length.get())
        cmd += ' -a ' + str(self.angle.get())
        cmd += ' -S ' + str(self.sigma.get())
        cmd += ' --t0 ' + str(self.time_offset.get())

        return cmd

    def get_data(self):
        data = "Particle = {p}\nLength = {L} [m]\nAngle = {a} [deg]\nBeam RMS = {S} [s]\nTime offset = {t} [s]".format(
                p=self.particle.get(), L=self.length.get(), a=self.angle.get(), S=self.sigma.get(), t=self.time_offset.get())
        return data

    def finalize(self):
        ear = self.controller.ear.get()
        max_angle = default_values[ear]['-a']
        if self.angle.get() > max_angle:
            self.controller.raise_error_message("Angle must be smaller than {} for {}.".format(max_angle, ear))
            return False
        return True
