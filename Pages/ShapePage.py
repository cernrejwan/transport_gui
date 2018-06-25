from BasePage import *


class ShapePage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Target shape")

        # vars:
        self.shape = StringVar(self, "Circular")

        self.radius_min = DoubleVar(self, kwargs['radius_min'])
        self.radius_max = DoubleVar(self, kwargs['radius_max'])
        self.radius_step = DoubleVar(self, kwargs['radius_step'])

        self.rect_x1 = DoubleVar(self, kwargs['rect_x1'])
        self.rect_x2 = DoubleVar(self, kwargs['rect_x2'])
        self.rect_y1 = DoubleVar(self, kwargs['rect_y1'])
        self.rect_y2 = DoubleVar(self, kwargs['rect_y2'])

        # gui:
        self.frame.pack()
        Label(self.frame, text="Please select target shape:").pack()
        OptionMenu(self, self.shape, "Circular", "Rectangular", command=self.set_shape).pack()

        self.circ_frame = Frame(self)
        Label(self.circ_frame, text="Set radius [cm]").pack()
        radius_range = Frame(self.circ_frame)
        radius_range.pack()
        Label(radius_range, text="min:").pack(side=LEFT)
        Entry(radius_range, textvariable=self.radius_min).pack(side=LEFT)
        Label(radius_range, text="max:").pack(side=LEFT)
        Entry(radius_range, textvariable=self.radius_max).pack(side=LEFT)
        Label(self.circ_frame, text="step size for resampling").pack()
        Entry(self.circ_frame, textvariable=self.radius_step).pack()

        self.rect_frame = Frame(self)
        Label(self.rect_frame, text="x1").grid(row=0, column=0)
        Entry(self.rect_frame, textvariable=self.rect_x1).grid(row=0, column=1)
        Label(self.rect_frame, text="y1").grid(row=0, column=2)
        Entry(self.rect_frame, textvariable=self.rect_y1).grid(row=0, column=3)
        Label(self.rect_frame, text="x2").grid(row=1, column=0)
        Entry(self.rect_frame, textvariable=self.rect_x2).grid(row=1, column=1)
        Label(self.rect_frame, text="y2").grid(row=1, column=2)
        Entry(self.rect_frame, textvariable=self.rect_y2).grid(row=1, column=3)

        self.circ_frame.pack()

    def set_shape(self, shape):
        if shape == "Circular":
            self.rect_frame.pack_forget()
            self.circ_frame.pack()
        else:
            self.circ_frame.pack_forget()
            self.rect_frame.pack()

    def get_cmd(self):
        if self.shape.get() == "Circular":
            cmd = '-r ' + str(self.radius_min.get())
            cmd += ' -R ' + str(self.radius_min.get())
            cmd += ' -s ' + str(self.radius_step.get())
        else:
            cmd = '--x1 ' + str(self.rect_x1.get())
            cmd += ' --y1 ' + str(self.rect_y1.get())
            cmd += ' --x2 ' + str(self.rect_x2.get())
            cmd += ' --y2 ' + str(self.rect_y2.get())

        return cmd

    def get_data(self):
        data = 'Shape = ' + self.shape.get() + '\n'

        if self.shape.get() == 'Circular':
            data += 'Radius = {min} - {max} [cm]\nstep = {step} [cm]'.format(
                min=self.radius_min.get(), max=self.radius_max.get(), step=self.radius_step.get()
            )
        else:
            data += '(x1,y1) = ({x1},{y1})\n(x2,y2) = ({x2},{y2})'.format(
                x1=self.rect_x1.get(), x2=self.rect_x2.get(), y1=self.rect_y1.get(), y2=self.rect_y2.get()
            )

        return data

    def get_vars_list(self):
        if self.shape.get() == "Circular":
            self.vars_list = ['shape', 'radius_min', 'radius_max', 'radius_step']
        else:
            self.vars_list = ['shape', 'rect_x1', 'rect_x2', 'rect_y1', 'rect_y2']
        return self.vars_list

    def finalize(self):
        if self.shape.get() == 'Circular':
            if self.radius_min.get() < 0 or self.radius_max.get() <= 0:
                self.controller.raise_error_message("Radius must be greater than 0")
                return False
            if self.radius_min.get() > self.radius_max.get():
                self.controller.raise_error_message("R_max must be greater than R_min")
                return False
        return True