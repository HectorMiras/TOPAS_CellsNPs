#!/bin/bash

NCELLS=40
INFILE=SimulationConfigFile_PISEFM2024.txt
TEMP_CONFIG="temp_config.txt"
STARTCELL=1
ENDCELL=$((STARTCELL + NCELLS - 1))

if [ -z "$NCELLS" ]; then
  echo "Usage: $0 <number_of_cells>"
  exit 1
fi

echo "Running simulation for $NCELLS cells..."

for i in $(seq $STARTCELL $ENDCELL); do
  echo "Processing cell $i of $ENDCELL"
  
  # Create a temporary configuration file with modified runDirectoryName
  cp "$INFILE" "$TEMP_CONFIG"
  
  # Append /cel# to only the directory path, preserving any comments
  sed -i -E 's|(runDirectoryName = [^[:space:]#]+)|\1/cell'$i'|' "$TEMP_CONFIG"
  
  # Run the simulation with the temporary config file
  ./main_run_simulation.sh "$TEMP_CONFIG"
  
  echo "Completed simulation for cell $i"
done

# Clean up
rm -f "$TEMP_CONFIG"

echo "All simulations completed!"


