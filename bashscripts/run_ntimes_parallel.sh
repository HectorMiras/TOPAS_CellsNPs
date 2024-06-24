#!/bin/bash

INFILE1="SARRP_PHSP.txt"
INFILE2="Cell_AGuIX.txt"
INFILE3="nucleus_nBIO.txt"
PYFILE1="sample_positions_in_medium.py"
PYFILE2="sample_positions_in_cell.py"
DELFILE="SARRP_PHSP.phsp"
DOSAMPLE=true 

ITER=1
ADDITION=0

USER=`whoami`
CURRENTPATH=`pwd`
COUNT=0

if [[ -z $ADDITION ]]; then
    COUNT=0
else
    COUNT=$ADDITION
fi

if [ "$DOSAMPLE" == false ]; then
    cd ./supportFiles
    echo 'Sample NPs only once'
    python $PYFILE1
    python $PYFILE2
    cd $CURRENTPATH
fi

# Number of available threads
available_threads=$(($(nproc) - 1))
# Print the available_threads
echo "Available threads: $available_threads"

# Function to execute simulation for one run
run_simulation() {
    local count=$1
    local currentpath=$2
    local dosample=$3

    DIR="${currentpath}/run${count}"
    echo $count
    echo $DIR
    mkdir -p $DIR

    cp $INFILE1 $DIR
    cp $INFILE2 $DIR
    cp $INFILE3 $DIR    

    SEED=`bash -c 'echo $RANDOM'`
    sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" $DIR/$INFILE1
    sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" $DIR/$INFILE2
    sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" $DIR/$INFILE3

    cp -r ./supportFiles $DIR
    cp -r sourcePHSPFiles $DIR

    if [ "$dosample" == true ]; then
        cd "${DIR}/supportFiles"
        echo 'Sample NPs in each run.'
        python3 $PYFILE1
        python3 $PYFILE2
        cd $DIR
    fi

    cd $DIR
    time ~/topas/bin/topas $INFILE1
    time ~/topas/bin/topas $INFILE2
    time ~/topas/bin/topas $INFILE3
    #rm $DELFILE

    cd $currentpath
}

while [[ $COUNT -lt $((ITER + ADDITION)) ]]
do
    # Run the simulation in the background
    run_simulation $COUNT $CURRENTPATH $DOSAMPLE &

    # Check the number of background jobs and wait if necessary
    while [ $(jobs -r | wc -l) -ge "$available_threads" ]; do
        sleep 30
    done

    COUNT=$((COUNT+1))
done

# Wait for all background jobs to finish
wait

echo "All simulations have completed."

