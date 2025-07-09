#!/bin/bash

SIMULATIONTPATH="/home/radiofisica/hector/mytopassimulations/TOPAS_CellsNPs/work/CellColony-med5-cell5"
MAX_RETRIES=20  # Setting maximum retries constant

INFILE="Phase3_dnaDamage.txt"
CHECKFILE="DNADamage.phsp"
# Use basename to extract just the filename from the path
SIMFILE=$(basename "$INFILE")

SAMPLESEEDS=true

# Counter for statistics
total_cells=0
total_runs=0
total_missing=0
total_fixed=0
total_failed=0

# Log file
LOG_FILE="run_failed_simulations_$(date +%Y%m%d_%H%M%S).log"

echo "Starting simulation check at $(date)" | tee -a "$LOG_FILE"
echo "Simulation path: $SIMULATIONTPATH" | tee -a "$LOG_FILE"

# Check if simulation path exists
if [ ! -d "$SIMULATIONTPATH" ]; then
  echo "Error: Simulation path does not exist: $SIMULATIONTPATH" | tee -a "$LOG_FILE"
  exit 1
fi

# Iterate through cell directories
for cell_dir in "$SIMULATIONTPATH"/cell*/; do
  if [ -d "$cell_dir" ]; then
    cell_name=$(basename "$cell_dir")
    ((total_cells++))
    echo "Checking $cell_name..." | tee -a "$LOG_FILE"
    
    # Iterate through run directories in each cell
    for run_dir in "$cell_dir"/run*/; do
      if [ -d "$run_dir" ]; then
        run_name=$(basename "$run_dir")
        ((total_runs++))
        
        # Check if CHECKFILE exists in the run directory AND is not empty
        if [ ! -f "$run_dir/$CHECKFILE" ] || [ ! -s "$run_dir/$CHECKFILE" ]; then
          # If file doesn't exist or is empty (zero size)
          ((total_missing++))
          if [ ! -f "$run_dir/$CHECKFILE" ]; then
            echo "Missing $CHECKFILE in $cell_name/$run_name" | tee -a "$LOG_FILE"
          else
            echo "Empty $CHECKFILE found in $cell_name/$run_name" | tee -a "$LOG_FILE"
          fi
          
          # Try to run the simulation up to MAX_RETRIES times
          success=false
          for ((retry=1; retry<=MAX_RETRIES; retry++)); do
            echo "  Attempt $retry of $MAX_RETRIES for $cell_name/$run_name" | tee -a "$LOG_FILE"
            
            # Sample a new seed if enabled
            if [ "$SAMPLESEEDS" = true ]; then
              SEED=$RANDOM
              echo "  Using new random seed: $SEED" | tee -a "$LOG_FILE"
              
              # Save original seed to restore later
              ORIGINAL_SEED=$(grep "i:Ts/Seed" "$run_dir/$INFILE" | awk '{print $NF}')
              
              # Modify the seed directly in the original file
              sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" "$run_dir/$INFILE"
            fi
            
            # Run TOPAS in the run directory
            cd "$run_dir" || continue
            echo "  Running: topas $INFILE in $(pwd)" | tee -a "$LOG_FILE"
            topas "$INFILE" >> "$LOG_FILE" 2>&1
            
            # Check if the simulation was successful (file exists AND has content)
            if [ -f "$CHECKFILE" ] && [ -s "$CHECKFILE" ]; then
              success=true
              ((total_fixed++))
              echo "  SUCCESS!!!: $CHECKFILE created in $cell_name/$run_name" | tee -a "$LOG_FILE"
              
              
              break
            fi
            
            echo "  Simulation failed on attempt $retry" | tee -a "$LOG_FILE"
            
            # Wait a moment before retrying
            sleep 2
          done
          
          
          if [ "$success" = false ]; then
            ((total_failed++))
            echo "  Failed to create valid $CHECKFILE after $MAX_RETRIES attempts in $cell_name/$run_name" | tee -a "$LOG_FILE"
          fi
          
          # Go back to the original directory
          cd - > /dev/null || exit
        fi
      fi
    done
  fi
done

# Print summary
echo -e "\nSummary:" | tee -a "$LOG_FILE"
echo "Total cells checked: $total_cells" | tee -a "$LOG_FILE"
echo "Total runs checked: $total_runs" | tee -a "$LOG_FILE"
echo "Total missing or empty $CHECKFILE files: $total_missing" | tee -a "$LOG_FILE"
echo "Total successfully fixed: $total_fixed" | tee -a "$LOG_FILE"
echo "Total failed after $MAX_RETRIES attempts: $total_failed" | tee -a "$LOG_FILE"
echo "Finished at $(date)" | tee -a "$LOG_FILE"

echo "Log file saved to: $LOG_FILE"
