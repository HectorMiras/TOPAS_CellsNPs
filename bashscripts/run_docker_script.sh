#!/bin/bash

# This script ignores the njobs value in the configfile and will create only one run directory in the container
# Other simulation runs will be executed in the other containers, managed by the batch script
# Arg 1 is the node number that is passed by main script

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
COUNT=$1


if [ ! $DOSAMPLE ]; then
	cd ./supportFiles
	python $PYFILE1
	python $PYFILE2
	cd $CURRENTPATH
fi

#DIR="${CURRENTPATH}/run${COUNT}"
DIR="${CURRENTPATH}/run"
echo $COUNT
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
	
if $DOSAMPLE; then
    cd "${DIR}/supportFiles"
    python3 $PYFILE1
    python3 $PYFILE2
fi

#read -p "Press any key to continue..."
	
cd $DIR
time /topas/bin/topas $INFILE1
time /topas/bin/topas $INFILE2
time /topas/bin/topas $INFILE3
rm $DELFILE


cd $CURRENTPATH
