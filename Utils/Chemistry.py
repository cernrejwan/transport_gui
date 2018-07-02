import pandas as pd
from FileReader import *
import os

paths = csv2dict('./Data/paths.csv')
symbols = pd.read_csv('./Data/elements/symbols.csv')
abundance = pd.read_csv('./Data/elements/abundance.csv')
abundance['fraction'] = abundance['fraction'] / 100

unit_mass = 1.66053904e-24
cm2barn = 1e24


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


support_materials = init_support_materials_menu('./Data/support_materials/')


def get_full_name(element_symbol, isotope_number):
    atom_num = symbols.query("Symbol == '{}'".format(element_symbol))['Atom_num'].values[0]
    sample = '{atom_num}-{symbol}-{isotope}'.format(atom_num=atom_num, symbol=element_symbol, isotope=isotope_number)
    return sample


def get_xs_file(element_symbol, isotope_number):
    return paths['xs_files_path'] + get_full_name(element_symbol.title(), isotope_number) + '_tot.xs'


def element_exists(element_symbol):
    return element_symbol.title() in list(symbols['Symbol'])


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
