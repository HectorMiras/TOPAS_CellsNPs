#!/bin/bash

module purge
module load topas/3.9.0_nomcauto
module load libGLU/9.0.0-foss-2018b
module load python
#module load geant4/10.7.3

INFILE1="SARRP_PHSP.txt"
INFILE2="Cell_AGuIX.txt"
INFILE3="getPositions_in_cell_symmetry.py"
DELFILE="SARRP_PHSP.phsp"

ITER=$1
if [[ $ITER -eq "" ]]
then
    ITER=1
fi
ADDITION=$2

if [[ -z $ADDITION ]]; then
    COUNT=0
else
    COUNT=$ADDITION
fi

USER=`whoami`
CURRENTPATH=`pwd`

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

    DIR="${CURRENTPATH}/work/run${COUNT}"
    
    mkdir -p $DIR
    
    cp $INFILE1 $DIR
    cp $INFILE2 $DIR
    cp $INFILE3 $DIR    


    SEED=`bash -c 'echo $RANDOM'`
    echo i:Ts/Seed = $SEED >> $DIR/$INFILE1
    echo i:Ts/Seed = $SEED >> $DIR/$INFILE2
    
    SCRIPT=$DIR/$INFILE1-$COUNT".csh"

    cp -r ./supportFiles $DIR
    
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
cd $DIR

python $INFILE3
time ~/topas/bin/topas $INFILE1
time ~/topas/bin/topas $INFILE2
rm $DELFILE

EOF
    
    chmod +x $SCRIPT
    bsub -e $DIR/log.err -o $DIR/log.out < $SCRIPT
    
    COUNT=$((COUNT+1))
done
