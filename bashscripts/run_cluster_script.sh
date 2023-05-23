#!/bin/bash

module purge
module load topas/3.9.0_nomcauto
module load libGLU/9.0.0-foss-2018b
module load python
#module load geant4/10.7.3

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

USER=`whoami`
CURRENTPATH=`pwd`

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
    
    mkdir -p $DIR
    
    cp $INFILE1 $DIR
    cp $INFILE2 $DIR
    cp $INFILE3 $DIR    


    SEED=`bash -c 'echo $RANDOM'`
    sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" $DIR/$INFILE1
    sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" $DIR/$INFILE2
	sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" $DIR/$INFILE3

    
    SCRIPT=$DIR/$INFILE1-$COUNT".csh"

    cp -r ./supportFiles $DIR
	cp -r sourcePHSPFiles $DIR
    
    cat - << EOF > $SCRIPT
#!/bin/bash
#BSUB -J $INFILE1-$COUNT
#BSUB -q normal
#BSUB -r
#BSUB -C 0
#BSUB -n 1
#BSUB -R "rusage[mem=2500]"
#BSUB -Q "140"
#BSUB -u nobody

if $DOSAMPLE; then
cd "${DIR}/supportFiles"
python $PYFILE1
python $PYFILE2
fi

cd $DIR
time ~/topas/bin/topas $INFILE1
time ~/topas/bin/topas $INFILE2
time ~/topas/bin/topas $INFILE3
rm $DELFILE

EOF
    
    chmod +x $SCRIPT
    bsub -e $DIR/log.err -o $DIR/log.out < $SCRIPT
    
    COUNT=$((COUNT+1))
done
