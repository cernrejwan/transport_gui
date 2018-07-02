def csv2dict(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    result = [line.strip().split(',') for line in lines]
    return {item[0]: ','.join(item[1:]) for item in result}


def dict2csv(data_dict, filename):
    data_list = [str(key) + ',' + str(value) for key, value in data_dict.iteritems()]
    data_str = '\n'.join(data_list)
    with open(filename, 'w') as f:
        f.write(data_str)
