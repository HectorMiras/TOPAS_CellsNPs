#!/bin/bash

# User configuration
SIMULATIONTPATH="/home/radiofisica/hector/mytopassimulations/TOPAS_CellsNPs/work/NanoBrachy-CellColony-MDAMB231-med0-cell0"
DNASCORERFILE="/home/radiofisica/hector/mytopassimulations/TOPAS_CellsNPs/supportFiles/DNAScorerStepByStep.txt"

# Iterate through cell directories in natural numeric order
for cell_dir in $(ls -d "$SIMULATIONTPATH"/cell*/ 2>/dev/null | sort -V); do
  cell_name=$(basename "$cell_dir")
  echo -e "\nChecking $cell_name..."
  # Iterate through run directories in each cell, sorted numerically
  for run_dir in $(ls -d "$cell_dir"/run*/ 2>/dev/null | sort -V); do
    run_name=$(basename "$run_dir")
    support_dir="$run_dir/supportFiles"
    mkdir -p "$support_dir"
    cp "$DNASCORERFILE" "$support_dir/"
    echo "  Copied DNAScorerStepByStep.txt to $cell_name/$run_name/supportFiles/"
  done
done

echo -e "\nDone."
