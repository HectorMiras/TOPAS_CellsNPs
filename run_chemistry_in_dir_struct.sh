#!/bin/bash

SIMULATIONTPATH=$1
MAX_RETRIES=5  # Setting maximum retries constant

#INFILE="./simulationFiles/Phase2_Cell_chemistry.txt"
INFILE="./simulationFiles/Phase2_Cell_ChemMolecules.txt"
OUTFILENAME="NumberOfMoleculesAtTime.phsp"
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

# Current working directory
CURRENTDIR=$(pwd)

# Find all run# directories at any level within SIMULATIONTPATH
run_dirs=$(find "$SIMULATIONTPATH" -type d -name "run*" | sort)

# Check if any run directories were found
if [ -z "$run_dirs" ]; then
    echo "No run directories found in $SIMULATIONTPATH or its subdirectories"
    exit 1
fi

echo "Found $(echo "$run_dirs" | wc -l) run directories to process"

# Process function for handling run directories
process_run_dir() {
    local DIR=$1
    echo "Processing directory: $DIR"
    
    # Copy the simulation file to the run directory
    echo "Copying $INFILE to $DIR/"
    cp "$INFILE" "$DIR/"
    
    # Change to the run directory
    cd "$DIR"
    
    # Replace Ge position lines from local Phase2_Cell.txt
    if [ -f Phase2_Cell.txt ]; then
        GE_MEDIUM_LINE=$(grep '^s:Ge/MediumNPPositionsFile' Phase2_Cell.txt)
        GE_CELL_LINE=$(grep '^s:Ge/CellNPPositionsFile' Phase2_Cell.txt)

        if [ -n "$GE_MEDIUM_LINE" ] && [ -n "$GE_CELL_LINE" ]; then
            sed -i "s|^s:Ge/MediumNPPositionsFile.*|$GE_MEDIUM_LINE|" "$SIMFILE"
            sed -i "s|^s:Ge/CellNPPositionsFile.*|$GE_CELL_LINE|" "$SIMFILE"
            echo "Replaced Ge position lines in $SIMFILE"
        else
            echo "Warning: One or both replacement lines not found in Phase2_Cell.txt"
        fi
    else
        echo "Warning: Phase2_Cell.txt not found in $DIR"
    fi

    if [ "$SAMPLESEEDS" == true ]; then
        SEED=`bash -c 'echo $RANDOM'`
        sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" "$SIMFILE"
    fi

    # Retry simulation loop
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
            echo "Simulation $SIMFILE failed. Retrying with new seed..."
              
            if [ $retry_count -lt $MAX_RETRIES ]; then
                SEED=`bash -c 'echo $RANDOM'`
                echo "Using new seed: $SEED"
                sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" "$SIMFILE"
            else
                echo "Maximum retries reached. Moving on..."
            fi
        fi
    done

    cd "$CURRENTDIR"
    echo "Completed processing directory: $DIR"
    echo "----------------------------------------"
}


# Process all run directories found at any level
for DIR in $run_dirs; do
    if [ ! -s "$DIR/$OUTFILENAME" ]; then
        process_run_dir "$DIR"
    else
        echo "Skipping $DIR: $OUTFILENAME already exists and is not empty."
    fi
done

echo "All run directories processed"
