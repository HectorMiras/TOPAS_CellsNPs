#!/bin/bash

# Input simulation file
input_file="Cell_PHSP.txt"

# Number of cores
num_cores=$(nproc)

# Loop over the 10 runs
for run_number in {1..5}; do
    # Create the run folder and copy all *.txt files
    run_folder="run${run_number}"
    #mkdir -p "${run_folder}"
    #cp ./*.txt "${run_folder}/"
	cp "${input_file}" "${run_folder}/${input_file}"

    # Update the random seed value
    sed -i "s/i:Ts\/Seed = [0-9]*/i:Ts\/Seed = ${run_number}/" "${run_folder}/${input_file}"

    # Change to the run folder, execute the simulation, and return to the parent folder
    (
        cd "${run_folder}"
        # Replace 'topas' with the actual TOPAS command if different
        core_number=$(( (run_number - 1) % num_cores ))
        taskset -c ${core_number} topas "${input_file}"
    ) &
done

# Wait for all simulations to complete
wait
