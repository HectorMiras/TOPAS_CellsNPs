import numpy as np
import sys
import os
import math

class NP_class:

    def __init__(self,):
        # all spatial values in nm.
        self.rNP = 3 # nm
        self.material = "water"
        self.density = 1.0  # g/cm3

    def read_file_parameters(self, np_parameter_file):
        parameters = {}
        with open(np_parameter_file, 'r') as file:
            for line in file:
                if ("Ge/" in line) or ("Ma/" in line):
                    # remove newline character and any leading/trailing whitespace
                    line = line.strip()
                    print(line)
                    # split the line into parameter name and value
                    parameter, value = line.split('=')
                    value = value.strip().split(' ')[0]
                    #parameter = parameter.strip()
                    #if "#" in value:
                    #    value, comment = value.split('#')
                    #value = value.strip()

                    # separate the value and its unit
                    #value, unit = value.split(' ')

                    # if the value ends with a digit, convert it to a float
                    if value[-1].isdigit():
                        value = float(value)

                    #parameters[parameter] = {'value': value, 'unit': unit}
                    if "RNP" in parameter:
                        self.rNP = value
                    if "NPMaterial" in parameter:
                        self.material = value
                    if "NPDensity" in parameter:
                        self.density = value
                        

    def volume_um3(self,):
        # get volume in um3
        return (4/3) * math.pi * np.power(0.001*self.rNP, 3)

    def mass_mg(self,):
        # um3 to cm3 and g to mg
        return np.power(1e-4,3) * self.volume_um3() * 1000 * self.density
    
    def number_from_conc_volume(self, conc, vol):
        # volume in um3
        # conc in mg/cm3
        # print(f'con: {conc}, vol: {vol}, mass: {self.mass_mg()}')
        return int(conc * vol * np.power(1e-4,3) / self.mass_mg())

    def get_relweights_and_dens_from_conc(self, conc):
        # return relative mass weights of water and nanoparticles from the concentration given in mg/cm3
        #print(f'density: {self.density}')
        f_mg_to_g = 0.001
        dw = 1.00 # density of water in mg/cm3
        w_water = dw / (dw + f_mg_to_g * conc)
        w_np = f_mg_to_g * conc / (dw + f_mg_to_g * conc)
        dens_tot = (dw + f_mg_to_g * conc) / (1 + f_mg_to_g * conc / self.density)
        return w_water, w_np, dens_tot
    
