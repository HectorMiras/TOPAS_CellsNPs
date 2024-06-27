#!/bin/bash

# This script ignores the njobs value in the configfile and will create only one run directory in the container
# Other simulation runs will be executed in the other containers, managed by the batch script
# Arg 1 is the node number that is passed by main script

INFILE1="SARRP_PHSP.txt"
INFILE2="Cell_AGuIX.txt"
INFILE3="nucleus_nBIO.txt"
PYFILE1="sample_positions_in_medium.py"
PYFILE2="sample_positions_in_cell.py"
SPLITPYFILE="split_simulation_script.py"
DELFILE="SARRP_PHSP.phsp"
DOSAMPLE=true 

ITER=1
ADDITION=0
SPLITNUM=1

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
    

cp -r ./supportFiles $DIR
	
if $DOSAMPLE; then
    cd "${DIR}/supportFiles"
    python3 $PYFILE1
    python3 $PYFILE2
    cd "${DIR}"
fi

#read -p "Press any key to continue..."

SPLITCOUNT=1
SIMFILE1=$INFILE1
SIMFILE2=$INFILE2
SIMFILE3=$INFILE3
while [[ SPLITCOUNT -le $SPLITNUM ]]
 do

   SEED=`bash -c 'echo $RANDOM'`
   sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" $DIR/$INFILE1
   sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" $DIR/$INFILE2
   sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" $DIR/$INFILE3

  if [ $SPLITNUM -gt 1 ]; then
    cd "${DIR}/supportFiles"
	  echo 'Sample NPs in each run.'
    SIMFILE1=$(python3 $SPLITPYFILE $SPLITNUM $SPLITCOUNT "$DIR"/$INFILE1)
    SIMFILE2=$(python3 $SPLITPYFILE $SPLITNUM $SPLITCOUNT "$DIR"/$INFILE2)
    SIMFILE3=$(python3 $SPLITPYFILE $SPLITNUM $SPLITCOUNT "$DIR"/$INFILE3)
  fi
  cd "${DIR}"
  time /topas/bin/topas $SIMFILE1
  time /topas/bin/topas $SIMFILE2
  time /topas/bin/topas $SIMFILE3
	rm $DELFILE

	  SPLITCOUNT=$((SPLITCOUNT+1))
  done


#cd $CURRENTPATH
