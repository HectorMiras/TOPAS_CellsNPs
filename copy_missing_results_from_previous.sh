#!/bin/bash

# User configuration
SIMULATIONTPATH="/home/radiofisica/hector/mytopassimulations/TOPAS_CellsNPs/work/NanoBrachy-CellColony-MDAMB231-med0-cell0"
CHECKFILE="DNADamage.phsp"

# Patterns to copy if needed
PATTERNS=("DNADamage*.*" "DoseNucleus*")

# Gather all run directories and those missing results
ALL_RUN_DIRS=()
MISSING_RUN_DIRS=()

for cell_dir in $(ls -d "$SIMULATIONTPATH"/cell*/ 2>/dev/null | sort -V); do
  for run_dir in $(ls -d "$cell_dir"/run*/ 2>/dev/null | sort -V); do
    ALL_RUN_DIRS+=("$run_dir")
    if [ ! -f "$run_dir/$CHECKFILE" ] || [ ! -s "$run_dir/$CHECKFILE" ]; then
      MISSING_RUN_DIRS+=("$run_dir")
    fi
  done
done

if [ ${#MISSING_RUN_DIRS[@]} -gt 0 ]; then
  echo "List of run directories without $CHECKFILE results:"
  for mdir in "${MISSING_RUN_DIRS[@]}"; do
    echo "  $mdir"
  done
fi

echo "${#MISSING_RUN_DIRS[@]} run directories without $CHECKFILE results out of ${#ALL_RUN_DIRS[@]}. Do you want to proceed with copy? (Y/N) "
read -r answer
if [[ ! "$answer" =~ ^[Yy]$ ]]; then
  echo "Aborted by user."
  exit 0
fi

# Iterate through cell directories in natural numeric order
for cell_dir in $(ls -d "$SIMULATIONTPATH"/cell*/ 2>/dev/null | sort -V); do
  cell_name=$(basename "$cell_dir")
  echo -e "\n\nChecking $cell_name..."

  # Iterate through run directories in each cell, sorted numerically
  run_dirs_sorted=( $(ls -d "$cell_dir"/run*/ 2>/dev/null | sort -V) )
  prev_run_dirs=()
  num_runs=${#run_dirs_sorted[@]}
  for ((idx=0; idx<num_runs; idx++)); do
    run_dir="${run_dirs_sorted[$idx]}"
    run_name=$(basename "$run_dir")
    echo -e "\nChecking $cell_name/$run_name..."

    # Check if CHECKFILE exists and is not empty
    if [ ! -f "$run_dir/$CHECKFILE" ] || [ ! -s "$run_dir/$CHECKFILE" ]; then
      echo "  $CHECKFILE missing or empty in $cell_name/$run_name."
      # Find the most recent previous run_dir with valid CHECKFILE
      found_prev_with_results=false
      search_indices=()
      if [ $idx -eq 0 ]; then
        # If this is the first run, previous is the last run (wrap around)
        for ((j=num_runs-1; j>=0; j--)); do
          if [ $j -ne 0 ]; then
            search_indices+=( $j )
          fi
        done
      else
        for ((j=idx-1; j>=0; j--)); do
          search_indices+=( $j )
        done
      fi
      for j in "${search_indices[@]}"; do
        prev_dir="${run_dirs_sorted[$j]}"
        if [ -f "$prev_dir/$CHECKFILE" ] && [ -s "$prev_dir/$CHECKFILE" ]; then
          found_prev_with_results=true
          echo "  Copying files from previous run with results: $(basename "$prev_dir")"
          for pattern in "${PATTERNS[@]}"; do
            for src_file in "$prev_dir"/$pattern; do
              if [ -f "$src_file" ]; then
                cp "$src_file" "$run_dir/"
                echo "    Copied $(basename "$src_file") to $cell_name/$run_name."
              fi
            done
          done
          break
        fi
      done
      if [ "$found_prev_with_results" = false ]; then
        echo "  No previous run with results to copy from."
      fi
    else
      echo "  $CHECKFILE exists and is not empty in $cell_name/$run_name."
    fi
    prev_run_dirs+=("$run_dir")
  done
done

echo -e "\nDone."
