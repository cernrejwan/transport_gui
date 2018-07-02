import pandas as pd
from CSVHandler import *

paths = csv2dict('./Data/paths.csv')
symbols = read_symbols('./Data/elements/symbols.csv')
abundance = pd.read_csv('./Data/elements/abundance.csv')
abundance['fraction'] = abundance['fraction'] / 100

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
    isotopes = abundance.loc[abundance['symbol'] == element_symbol.title(), 'iso_num']
    return isotope_number in list(isotopes)


def calc_atob_by_density(mass_number, density, thickness):
    sigma = density * thickness
    atob = calc_atob_by_sigma(mass_number, sigma)
    return atob, sigma


def calc_atob_by_sigma(mass_number, sigma):
    atob = sigma / (mass_number * unit_mass) / cm2barn
    return atob
