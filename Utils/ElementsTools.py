import pandas as pd
from Tkinter import DoubleVar
from Default import *

symbols = pd.read_csv('./elements/symbols.csv')
abundance = pd.read_csv('./elements/abundance.csv')
abundance['fraction'] = abundance['fraction'] / 100

unit_mass = 1.66053904e-24
cm2barn = 1e24


class Element:
    def __init__(self, master, element_symbol):
        self.symbol = element_symbol.title()

        info = symbols[symbols['Symbol'] == self.symbol]
        self.name = info['Name'].values[0]
        self.atomic_num = info['Atom_num'].values[0]

        iso_abundance = abundance[abundance['symbol'] == self.symbol]

        self.no_data = (iso_abundance['fraction'].count() == 0)
        iso_abundance = iso_abundance.fillna(0)
        self.isotopes = [(iso['iso_num'], DoubleVar(master, iso['fraction'])) for _, iso in iso_abundance.iterrows()]

    def is_valid(self):
        cumulative_sum = sum([float(frac.get()) for _, frac in self.isotopes])
        return (cumulative_sum == 1)

    def get_avg_mass_number(self):
        weighted_sum = sum([frac.get() * iso_num for iso_num, frac in self.isotopes])
        return weighted_sum

    def get_cmd(self, total_atob):
        total_mass = self.get_avg_mass_number()
        cmd = ''
        for iso_num, frac in self.isotopes:
            atob = total_atob * frac.get() * iso_num / total_mass
            xs_file = get_xs_file(self.symbol, iso_num)
            cmd += '--Sxs {xs_file} --Satob {atob} '.format(xs_file=xs_file, atob=atob)
        return cmd


def get_full_name(element_symbol, isotope_number):
    atom_num = symbols.query("Symbol == '{}'".format(element_symbol))['Atom_num'].values[0]
    sample = '{atom_num}-{symbol}-{isotope}'.format(atom_num=atom_num, symbol=element_symbol, isotope=isotope_number)
    return sample


def get_xs_file(element_symbol, isotope_number):
    return default_values['cross_section']['path'] + get_full_name(element_symbol.title(), isotope_number) + '_tot.xs'


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
    atob = sigma / (mass_number * unit_mass) * cm2barn
    return atob