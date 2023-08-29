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

if [ ! $DOSAMPLE ]; then
	cd ./supportFiles
	python $PYFILE1
	python $PYFILE2
	cd $CURRENTPATH
fi

while [[ $COUNT -lt $((ITER + ADDITION)) ]]
do
    #USER=`whoami`
    #CURRENTPATH=`pwd`
    DATEDAY=`date | awk '{print $3}'`
    DATEMONTH=`date | awk '{print $2}'`
    DATEYEAR=`date | awk '{print $6}'`
    DATEHOUR=`date | awk '{print $4}' | awk -F: '{print $1}'`
    DATEMIN=`date | awk '{print $4}' | awk -F: '{print $2}'`
    DATE=$DATEYEAR$DATEMONTH$DATEDAY
    UNAME=`uname`
    
    #DIR=$CURRENTPATH/$DATE/$INFILE/$COUNT
    #if [ -d $DIR ]
    #then
    #   echo Directory exists, removing and recreating $DIR
    #    rm -rf $DIR
    #fi

    DIR="${CURRENTPATH}/run${COUNT}"
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
#	cp -r sourcePHSPFiles $DIR
	
	if $DOSAMPLE; then
		cd "${DIR}/supportFiles"
		python3 $PYFILE1
		python3 $PYFILE2
	fi
	#read -p "Press any key to continue..."
	
	cd $DIR
	time /root/topas/bin/topas $INFILE1
	time /root/topas/bin/topas $INFILE2
	time /root/topas/bin/topas $INFILE3
	rm $DELFILE

    
    COUNT=$((COUNT+1))
	
	cd $CURRENTPATH
done
