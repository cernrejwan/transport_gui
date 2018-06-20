class OrderedDict:
    def __init__(self):
        self.items_list = list()
        self.keys_dict = dict()

    def __getitem__(self, item):
        if type(item) == int:
            return self.items_list[item]
        else:
            index = self.keys_dict[item]
            return self.items_list[index]

    def add(self, item):
        index = len(self.items_list)
        self.items_list.append(item)
        self.keys_dict[item.__class__.__name__] = index

    def remove(self, key):
        index = self.keys_dict.pop(key)
        self.items_list.pop(index)

    def __len__(self):
        return len(self.items_list)

    def __iter__(self):
        return iter(self.items_list)

    def __contains__(self, item):
        return item in self.keys_dict