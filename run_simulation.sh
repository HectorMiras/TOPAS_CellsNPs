#!/bin/bash

CURRENTPATH=`pwd`
RUNDIR="${CURRENTPATH}/work/${1:-TestRunDir}"
mkdir -p $RUNDIR
python3 run_simulation.py
cp -r ./runFiles/* $RUNDIR
cp -r ./supportFiles $RUNDIR
cd $RUNDIR
dos2unix submit_script.sh
chmod +x submit_script.sh
./submit_script.sh

