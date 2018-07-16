from CSVHandler import *

symbols = read_symbols(paths['symbols_path'])
abundance = read_abundance(paths['abundance_path'])

unit_mass = 1.66053904e-24
cm2barn = 1e24


def get_full_name(element_symbol, isotope_number):
    atom_num = symbols[element_symbol]['Atom_num']
    sample = '{atom_num}-{symbol}-{isotope}'.format(atom_num=atom_num, symbol=element_symbol, isotope=isotope_number)
    return sample


def get_xs_file(element_symbol, isotope_number):
    return paths['xs_files_path'] + get_full_name(element_symbol.title(), isotope_number) + '_tot.xs'


def element_exists(element_symbol):
    return element_symbol.title() in list(symbols.keys())


def isotope_exists(element_symbol, isotope_number):
    isotopes = abundance[element_symbol.title()].keys()
    return isotope_number in list(isotopes)


def calc_atob_by_density(mass_number, density, thickness):
    sigma = density * thickness
    atob = calc_atob_by_sigma(mass_number, sigma)
    return atob, sigma


def calc_atob_by_sigma(mass_number, sigma):
    atob = sigma / (mass_number * unit_mass) / cm2barn
    return atob
