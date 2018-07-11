from BasePage import *
from Pages.SupportLayerPage import SupportLayerPage
from Utils.OrderedDict import OrderedDict


class SupportPage(BasePage):
    def __init__(self, parent, controller, **kwargs):
        BasePage.__init__(self, parent, controller, "Support", show_title=False)

        # vars
        self.kwargs = dict([(key, value) for key, value in kwargs.iteritems() if key.startswith("support")])
        self.num_layers = 0
        self.layers = OrderedDict()

        # gui
        self.navigation_header = Frame(self)
        self.navigation_header.pack(side=TOP)

        self.plus = Button(self.navigation_header, text='+', command=self.add_layer)
        self.plus.grid(row=0, column=self.num_layers)
        self.buttons = OrderedDict()

        self.container = Frame(self)
        self.container.pack()
        Label(self.container, text="Click the + buttons to add support layers").grid(row=0, column=0)

        num_layers = int(kwargs.get('support_layers', 0))
        for i in range(num_layers):
            self.add_layer()

    def add_page(self, cls, page_name, **kwargs):
        page = cls(parent=self.container, controller=self.controller, master=self, **kwargs)
        self.layers.add(page_name, page)
        page.grid(row=1, column=0, sticky="nsew")

    def add_layer(self):
        self.plus.grid_forget()
        page_name = "Support " + str(self.num_layers + 1)
        self.add_page(SupportLayerPage, page_name, index=self.num_layers + 1, **self.kwargs)
        new_button = Button(self.navigation_header, text=page_name, command=self.layers[page_name].tkraise)
        new_button.grid(row=0, column=self.num_layers)
        self.buttons.add(page_name, new_button)
        self.num_layers += 1
        self.plus.grid(row=0, column=self.num_layers)

    def remove_page(self, index):
        page_name = "Support " + str(index)
        self.layers[page_name].destroy()
        self.layers.remove(page_name)
        self.buttons[page_name].grid_forget()
        self.buttons.remove(page_name)

    def get_cmd(self):
        return ' '.join([layer.get_cmd() for layer in self.layers])

    def finalize(self):
        for layer in self.layers:
            if not layer.finalize():
                return False
        return True

    def get_data(self):
        data = ''
        for layer in self.layers:
            data += '\n' + layer.page_name + ':\n'
            data += layer.get_data() + '\n'
        return data

    def get_vars(self):
        result = dict()
        result['support_layers'] = self.num_layers
        for layer in self.layers:
            result.update(layer.get_vars())
        return result
