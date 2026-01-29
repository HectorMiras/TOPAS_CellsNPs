#!/bin/bash

SIMULATIONTPATH="/home/radiofisica/hector/mytopassimulations/TOPAS_CellsNPs/work/NanoBrachy-CellColony-MDAMB231-med0-cell1-clustered"
MAX_RETRIES=20  # Setting maximum retries constant

INFILE="/home/radiofisica/hector/mytopassimulations/TOPAS_CellsNPs/simulationFiles/Phase3_dnaDamage.txt"
CHECKFILE="DNADamage.phsp"
# INFILE="/home/radiofisica/hector/mytopassimulations/TOPAS_CellsNPs/simulationFiles/Phase3_dose_to_nucleus.txt"
# CHECKFILE="nucleus_dose_Ph3.csv"

DOCHECK=true  # Whether to check for CHECKFILE before running simulation
# Use basename to extract just the filename from the path
SIMFILE=$(basename "$INFILE")

SAMPLESEEDS=true

# Counter for statistics
total_cells=0
total_runs=0
total_missing=0
total_fixed=0
total_failed=0

# Log file (will be written at the end only, in SIMULATIONTPATH)
LOG_FILE="$SIMULATIONTPATH/run_phase3_summary_$(date +%Y%m%d_%H%M%S).log"

# Array to store failed runs
FAILED_RUNS=()

run_simulation() {
  # Copy INFILE to run_dir before running simulation
  cp "$INFILE" "$run_dir/"
  # Try to run the simulation up to MAX_RETRIES times
  success=false
  for ((retry=1; retry<=MAX_RETRIES; retry++)); do
    echo "  Attempt $retry of $MAX_RETRIES for $cell_name/$run_name"
    # Sample a new seed if enabled
    if [ "$SAMPLESEEDS" = true ]; then
      SEED=$RANDOM
      echo "  Using new random seed: $SEED"
      # Save original seed to restore later
      ORIGINAL_SEED=$(grep "i:Ts/Seed" "$run_dir/$SIMFILE" | awk '{print $NF}')
      # Modify the seed directly in the copied file
      sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" "$run_dir/$SIMFILE"
    fi
    # Run TOPAS in the run directory
    cd "$run_dir" || continue
    echo "  Running: topas $INFILE in $(pwd)"
    find . -maxdepth 1 -type f -name 'run_failed_simulations_*.log' -delete
    topas "$SIMFILE" >> "$LOG_FILE" 2>&1
    # Check if the simulation was successful (file exists AND has content)
    if [ -f "$CHECKFILE" ] && [ -s "$CHECKFILE" ]; then
      success=true
      ((total_fixed++))
      echo "  SUCCESS!!!: $CHECKFILE created in $cell_name/$run_name"
      break
    fi
    echo "  Simulation failed on attempt $retry"
    sleep 2
  done
  if [ "$success" = false ]; then
    ((total_failed++))
    FAILED_RUNS+=("$cell_name/$run_name")
  fi
  cd - > /dev/null || exit
}

echo "Starting simulation check at $(date)"
echo "Simulation path: $SIMULATIONTPATH"

# Check if simulation path exists
if [ ! -d "$SIMULATIONTPATH" ]; then
  echo "Error: Simulation path does not exist: $SIMULATIONTPATH"
  exit 1
fi

# Iterate through cell directories in natural numeric order
for cell_dir in $(ls -d "$SIMULATIONTPATH"/cell*/ 2>/dev/null | sort -V); do
  if [ -d "$cell_dir" ]; then
    cell_name=$(basename "$cell_dir")
    ((total_cells++))
    echo "Checking $cell_name..."
    
    # Iterate through run directories in each cell, sorted numerically
    for run_dir in $(ls -d "$cell_dir"/run*/ 2>/dev/null | sort -V); do
      if [ -d "$run_dir" ]; then
        run_name=$(basename "$run_dir")
        ((total_runs++))
        
        # Check if CHECKFILE exists in the run directory AND is not empty
        if [ "$DOCHECK" = true ]; then
          if [ ! -f "$run_dir/$CHECKFILE" ] || [ ! -s "$run_dir/$CHECKFILE" ]; then
            ((total_missing++))
            if [ ! -f "$run_dir/$CHECKFILE" ]; then
              echo "Missing $CHECKFILE in $cell_name/$run_name"
            else
              echo "Empty $CHECKFILE found in $cell_name/$run_name"
            fi
            run_simulation
          fi
        else
          run_simulation
        fi
      fi
    done
  fi
done

# Print summary and failed runs to log file in SIMULATIONTPATH
{
  echo "Summary:"
  echo "Total cells checked: $total_cells"
  echo "Total runs checked: $total_runs"
  echo "Total missing or empty $CHECKFILE files: $total_missing"
  echo "Total successfully fixed: $total_fixed"
  echo "Total failed after $MAX_RETRIES attempts: $total_failed"
  echo "Finished at $(date)"
  if (( total_failed > 0 )); then
    echo "\nFailed runs after $MAX_RETRIES attempts:"
    for failed in "${FAILED_RUNS[@]}"; do
      echo "$failed"
    done
  fi
} > "$LOG_FILE"

echo "Summary log file saved to: $LOG_FILE"
