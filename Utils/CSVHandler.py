from collections import defaultdict


def read_csv(filename, header=False):
    with open(filename, 'r') as f:
        lines = f.readlines()
    result = [line.strip().split(',') for line in lines]
    return result[1:] if header else result


def csv2dict(filename):
    result = read_csv(filename)
    return {item[0]: ','.join(item[1:]) for item in result}


def dict2csv(data_dict, filename):
    data_list = [str(key) + ',' + str(value) for key, value in data_dict.iteritems()]
    data_str = '\n'.join(data_list)
    with open(filename, 'w') as f:
        f.write(data_str)


def read_symbols(filename):
    result = read_csv(filename, header=True)
    return {item[0]: {'Name': item[1], 'Atom_num': item[2]} for item in result}


def read_abundance(filename):
    result = read_csv(filename, header=True)
    res_dict = defaultdict(dict)
    for item in result:
        res_dict[item[0]][item[1]] = item[2]
    return res_dict
