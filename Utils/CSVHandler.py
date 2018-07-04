from collections import defaultdict


def read_csv(filename, header=False):
    with open(filename, 'r') as f:
        lines = f.readlines()
    result = [line.strip().split(',') for line in lines]
    return result[1:] if header else result


def csv2dict(filename):
    result = read_csv(filename)
    return dict([(item[0], ','.join(item[1:])) for item in result])


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


def read_histogram_menus(filename):
    result = read_csv(filename, header=True)
    res_dict = dict()
    for item in result:
        name = item[1]
        res_dict[name] = dict([('dim',item[0]),('cmd',item[2]),('unit_x',item[3]),('unit_y',item[4]),('yield',item[5])])
    return res_dict
