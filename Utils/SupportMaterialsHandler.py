from CSVHandler import *


def get_support_material(file_path):
    name = os.path.basename(file_path).split('.')[0]
    values = csv2dict(file_path)
    values['formula'] = eval(eval(values['formula']))
    return name, values


def init_support_materials_menu(support_materials_path):
    support_materials_dict = dict()
    files_list = os.listdir(support_materials_path)
    for material in files_list:
        file_path = os.path.join(support_materials_path, material)
        name, values = get_support_material(file_path)
        support_materials_dict[name] = values
    return support_materials_dict


support_materials = init_support_materials_menu(paths['support_materials_path'])
