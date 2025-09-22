#!/bin/bash

INFILE1="SARRP_PHSP.txt"
INFILE2="Cell_AGuIX.txt"
INFILE3="nucleus_nBIO.txt"
PYFILE1="sample_positions_in_medium.py"
PYFILE2="sample_positions_in_cell.py"
SPLITPYFILE="split_simulation_script.py"
DELFILE="I125Beam_PHSP.phsp"
DOSAMPLE=true 

ITER=1
ADDITION=0
SPLITNUM=1
MAX_RETRIES=5  # Maximum number of retries for failed simulations

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

#start with 1
COUNT=$((COUNT+1))
while [[ $COUNT -le $((ITER + ADDITION)) ]]
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
	echo "$DIR"
    mkdir -p "$DIR"
    
    cp $INFILE1 "$DIR"
    cp $INFILE2 "$DIR"
    cp $INFILE3 "$DIR"
    

    cp -r ./supportFiles $DIR
	cp -r sourcePHSPFiles $DIR
	
	if [ "$DOSAMPLE" == true ]; then
		cd "${DIR}/supportFiles"
		echo 'Sample NPs in each run.'
		python3 $PYFILE1
		python3 $PYFILE2
	fi
	#read -p "Press any key to continue..."

	SPLITCOUNT=1
	SIMFILE1=$INFILE1
	SIMFILE2=$INFILE2
	SIMFILE3=$INFILE3
	while [[ SPLITCOUNT -le $SPLITNUM ]]
  do

    SEED=`bash -c 'echo $RANDOM'`
    sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" "$DIR"/$INFILE1
    sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" "$DIR"/$INFILE2
	sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" "$DIR"/$INFILE3

	  if [ $SPLITNUM -gt 1 ]; then
	    cd "${DIR}/supportFiles"
		  echo 'Sample NPs in each run.'
	    SIMFILE1=$(python3 $SPLITPYFILE $SPLITNUM $SPLITCOUNT "$DIR"/$INFILE1)
	    SIMFILE2=$(python3 $SPLITPYFILE $SPLITNUM $SPLITCOUNT "$DIR"/$INFILE2)
	    SIMFILE3=$(python3 $SPLITPYFILE $SPLITNUM $SPLITCOUNT "$DIR"/$INFILE3)
	  fi
	  cd "${DIR}"

	  time topas $SIMFILE1
	  time topas $SIMFILE2
	  
	  # Add error handling for $SIMFILE3 which sometimes crashes
	  retry_count=0
	  success=false
	  
	  while [ $retry_count -lt $MAX_RETRIES ] && [ "$success" != "true" ]; do
	    echo "Running topas $SIMFILE3 (attempt $((retry_count+1))/$MAX_RETRIES)"
	    time topas $SIMFILE3
	    
	    if [ $? -eq 0 ]; then
	      success=true
	      echo "Simulation $SIMFILE3 completed successfully"
	    else
	      retry_count=$((retry_count+1))
	      echo "Simulation $SIMFILE3 failed (core dumped). Retrying with new seed..."
	      
	      if [ $retry_count -lt $MAX_RETRIES ]; then
	        # Generate new random seed
	        SEED=`bash -c 'echo $RANDOM'`
	        echo "Using new seed: $SEED"
	        sed -i "s/i:Ts\/Seed = .*/i:Ts\/Seed = $SEED/" "$DIR"/$INFILE3
	      else
	        echo "Maximum retries reached. Moving on..."
	      fi
	    fi
	  done
	  
	  rm $DELFILE

	  SPLITCOUNT=$((SPLITCOUNT+1))
  done
    
    COUNT=$((COUNT+1))
	
	cd $CURRENTPATH
done
