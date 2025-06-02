#!/bin/bash

SIMULATIONTPATH=$1
MAX_RETRIES=5  # Setting maximum retries constant

INFILE="./simulationFiles/Phase2_Cell_chemistry.txt"
# Use basename to extract just the filename from the path
SIMFILE=$(basename "$INFILE")

SAMPLESEEDS=true 

# Check if SIMULATIONTPATH is provided
if [ -z "$SIMULATIONTPATH" ]; then
    echo "Error: No simulation path provided"
    echo "Usage: $0 <simulation_path>"
    exit 1
fi

# Check if SIMULATIONTPATH exists
if [ ! -d "$SIMULATIONTPATH" ]; then
    echo "Error: Directory $SIMULATIONTPATH does not exist"
    exit 1
fi

# Check if source INFILE exists
if [ ! -f "$INFILE" ]; then
    echo "Error: Source simulation file $INFILE does not exist"
    exit 1
fi

# Find all run# directories
run_dirs=$(find "$SIMULATIONTPATH" -type d -name "run*" | sort)

# Check if any run directories were found
if [ -z "$run_dirs" ]; then
    echo "No run directories found in $SIMULATIONTPATH"
    exit 1
fi

# Current working directory
CURRENTDIR=$(pwd)

# Loop through each run directory
for DIR in $run_dirs; do
    echo "Processing directory: $DIR"
    
    # Copy the simulation file to the run directory
    echo "Copying $INFILE to $DIR/"
    cp "$INFILE" "$DIR/"
    
    # Change to the run directory
    cd "$DIR"
    
    if [ "$SAMPLESEEDS" == true ]; then
        SEED=`bash -c 'echo $RANDOM'`
        sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" "$DIR/$SIMFILE"
    fi
    
    # Add error handling for simulation which sometimes crashes
    retry_count=0
    success=false
          
    while [ $retry_count -lt $MAX_RETRIES ] && [ "$success" != "true" ]; do
        echo "Running topas $SIMFILE (attempt $((retry_count+1))/$MAX_RETRIES)"
        time topas $SIMFILE
            
        if [ $? -eq 0 ]; then
            success=true
            echo "Simulation $SIMFILE completed successfully"
        else
            retry_count=$((retry_count+1))
            echo "Simulation $SIMFILE failed (core dumped). Retrying with new seed..."
              
            if [ $retry_count -lt $MAX_RETRIES ]; then
                # Generate new random seed
                SEED=`bash -c 'echo $RANDOM'`
                echo "Using new seed: $SEED"
                sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" "$DIR/$SIMFILE"
            else
                echo "Maximum retries reached. Moving on..."
            fi
        fi
    done
    
    # Return to original directory
    cd "$CURRENTDIR"
    
    echo "Completed processing directory: $DIR"
    echo "----------------------------------------"
done

echo "All run directories processed"