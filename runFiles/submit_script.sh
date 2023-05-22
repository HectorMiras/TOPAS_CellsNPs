#!/bin/bash

INFILE1="SARRP_PHSP.txt" 
INFILE2="Cell_and_medium_NPs.txt" 
INFILE3="None" 
PYFILE="get_NP_positions.py"
DELFILE="SARRP_CellPHSP.phsp"

ITER=2 
ADDITION=0

USER=`whoami`
CURRENTPATH=`pwd`
COUNT=0

if [[ -z $ADDITION ]]; then
    COUNT=0
else
    COUNT=$ADDITION
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
#    cp $INFILE3 $DIR    
#    cp $PYFILE $DIR

    SEED=`bash -c 'echo $RANDOM'`
    echo i:Ts/Seed = $SEED >> $DIR/$INFILE1
    echo i:Ts/Seed = $SEED >> $DIR/$INFILE2
#	echo i:Ts/Seed = $SEED >> $DIR/$INFILE3
    

    cp -r ./supportFiles $DIR
	cd $DIR
	
#	python $PYFILE
	time ~/topas/bin/topas $INFILE1
	time ~/topas/bin/topas $INFILE2
#	time ~/topas/bin/topas $INFILE3
	rm $DELFILE

    
    COUNT=$((COUNT+1))
	
	cd $CURRENTPATH
done
