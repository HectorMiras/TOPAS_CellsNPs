import numpy as np
import sys
import os
import math

class Cell_class:

    def __init__(self, shape="Cylindrical"):
        # all spatial values in um.
        self.rCell = 5
        self.rNucl = 4.8
        self.height = 10
        self.membraneThickness = 0.01
        self.shape = shape  # "Cylindrical" or "Spherical"

    def read_file_parameters(self, cell_parameter_file):
        parameters = {}
        with open(cell_parameter_file, 'r') as file:
            for line in file:
                if line.startswith('d:Ge/') and not line.startswith('#'):
                    # remove newline character and any leading/trailing whitespace
                    line = line.strip()

                    # split the line into parameter name and value
                    parameter, value = line.split('=')
                    parameter = parameter.strip()
                    if "#" in value:
                        value, comment = value.split('#')
                    value = value.strip()

                    # separate the value and its unit
                    value, unit = value.split(' ')

                    # if the value ends with a digit, convert it to a float
                    if value[-1].isdigit():
                        value = float(value)

                    parameters[parameter] = {'value': value, 'unit': unit}
                    if "RCell" in parameter:
                        self.rCell = value
                    if "HLCell" in parameter:
                        self.height = 2 * value
                    if "RNucleus" in parameter:
                        self.rNucl = value
                    if "CellMembrane" in parameter:
                        self.membraneThickness = 0.001 * value

                    # if shape is Spherical, assign height = rCell
                    if self.shape == "Spherical":
                        self.height = self.rCell


    def volume_cell(self):
        if self.shape == "Spherical":
            # Volume of a sphere: (4/3)πr³.
            return (4/3) * math.pi * np.power(self.rCell, 3)
        else:
            # Assume cylindrical shape: base area * height.
            return math.pi * np.power(self.rCell, 2) * self.height

    def volume_nucleus(self):
        # Volume of a sphere: (4/3)πr³.
        return (4/3) * math.pi * np.power(self.rNucl, 3)

    def volume_cytoplasm(self):
        return self.volume_cell() - self.volume_nucleus()