import os
from pathlib import Path
import sys
import numpy as np
#from topas2numpy import BinnedResult
#import pandas as pd
from files_and_directory_manager import get_outputfile_paths

# Merge EnergyDeposit or DoseToMedium files from different runs
combined_sum = 0
combined_count_in_bin = 0
combined_second_moment = 0
combined_histories_with_scorer_active = 0

folder_path = "./work"
filename = 'EnergyDepositToNucleus_1mgml_0AGuIX'

output_file_paths = get_outputfile_paths(folder_path, filename, 'csv')
print(len(output_file_paths))
cont = 0
var = 0.0
for file_path in output_file_paths:
    # subfolder_name = f'run{run_number}'

    # Read EnergyDepositToNucleus.csv file
    # file_path = Path(f'{folder_path}/{subfolder_name}/{filename}').absolute()

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Extract the data from the last line
    if len(lines) > 0:
        data_line = lines[-1]
        data_values = [float(value) for value in data_line.split(', ')]

        sum_energy, mean_energy, count_in_bin, second_moment, variance, std_dev, histories_with_scorer_active = data_values

        # Combine the output values
        combined_sum += sum_energy
        combined_count_in_bin += count_in_bin
        combined_second_moment += second_moment
        combined_histories_with_scorer_active += histories_with_scorer_active
        var = var +  sum_energy*sum_energy
        cont = cont + 1
# Calculate the combined mean, variance, and standard deviation
combined_mean = combined_sum / combined_histories_with_scorer_active
combined_variance = combined_second_moment / combined_histories_with_scorer_active - combined_mean ** 2
combined_std_dev = np.sqrt(combined_variance)
var = np.sqrt(var/cont - combined_sum*combined_sum/(cont*cont))

# Write the combined results to a new output file
with open(f"{folder_path}/results/combined_{filename}.csv", "w") as f:
    for line in lines[:-1]:
        f.write(line)

    f.write(
        f"{combined_sum}, {combined_mean}, {combined_count_in_bin}, {combined_second_moment}, {combined_variance}, {combined_std_dev}, {combined_histories_with_scorer_active}\n")

unc_2sigma = combined_std_dev / np.sqrt(combined_histories_with_scorer_active)
print(f'Number of results merged: {cont} out of {len(output_file_paths)}')
print(f'Energy (MeV/hist): {combined_mean} +/- {unc_2sigma}')
print(f'Sum energy = {combined_sum/cont} +/- {var}')
