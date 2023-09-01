#!/bin/bash

source ./venv/bin/activate

CURRENTPATH=`pwd`
CONFIGFILE="${1:-SimulationConfigFile.txt}"

python3 pythonscripts/run_simulation.py $CURRENTPATH $CONFIGFILE

RUNDIR=$(grep "runDirectoryName" SimulationConfigFile.txt | awk -F'= ' '{print $2}' | cut -d'#' -f1 | tr -d ' ')
RUNDIR="${CURRENTPATH}/work/$RUNDIR"
echo $RUNDIR

cd $RUNDIR

#dos2unix submit_script.sh
chmod +x submit_script.sh
./submit_script.sh

deactivate
