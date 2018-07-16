from collections import defaultdict
import os


def read_csv(filename, header=False):
    with open(filename, 'r') as f:
        lines = f.readlines()
    result = [line.strip().split(',') for line in lines]
    return result[1:] if header else result


def csv2dict(filename):
    result = read_csv(filename)
    return dict([(item[0], ','.join(item[1:])) for item in result])


def read_paths():
    loc_dir = os.path.dirname(os.path.realpath(__file__))
    par_dir = os.path.abspath(os.path.join(loc_dir, os.pardir))
    paths_file = 'Data/paths.csv'
    paths = csv2dict(os.path.join(par_dir, paths_file))
    abs_paths = dict()
    for key, value in paths.iteritems():
        if value.startswith('./'):
            abs_paths[key] = os.path.join(par_dir, value[2:])
    paths.update(abs_paths)
    return paths


paths = read_paths()


def dict2csv(data_dict, filename):
    data_list = [str(key) + ',' + str(value) for key, value in data_dict.iteritems()]
    data_str = '\n'.join(data_list)
    with open(filename, 'w') as f:
        f.write(data_str)


def read_symbols(filename):
    result = read_csv(filename, header=True)
    return dict([(item[0], dict([('Name', item[1]), ('Atom_num', item[2])])) for item in result])


def read_abundance(filename):
    result = read_csv(filename, header=True)
    res_dict = defaultdict(dict)
    for item in result:
        fraction = item[2] if item[2] else 0
        res_dict[item[0]][int(item[1])] = float(fraction) / 100
    return res_dict


def read_histogram_menus():
    result = read_csv(paths['histogram_menus_path'], header=True)
    res_dict = dict()
    for item in result:
        name_x, name_y = item[1], item[2]
        name = name_y + ' vs ' + name_x if name_y else name_x
        res_dict[name] = {'dim': item[0], 'name_x': item[1], 'name_y': item[2], 'cmd': item[3]}
    return res_dict


def read_histogram_types():
    result = read_csv(paths['histogram_types_path'], header=True)
    res_dict = dict()
    for item in result:
        name = item[0]
        res_dict[name] = {'unit': item[1], 'min': item[2], 'max': item[3], 'bins': item[4]}
    return res_dict

