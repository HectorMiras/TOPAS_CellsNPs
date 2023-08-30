#!/bin/bash

CURRENTPATH=`pwd`
NODE_ID=$1
RUNDIR="${CURRENTPATH}/work/${2:-RunDir}"
CONFIGFILE="SimulationConfigFile.txt"
mkdir -p $RUNDIR

python3 pythonscripts/run_simulation.py $CURRENTPATH

cp $CONFIGFILE $RUNDIR
cp -r ./runFiles/* $RUNDIR

cd $RUNDIR

chmod +x submit_script.sh $NODE_ID
./submit_script.sh

