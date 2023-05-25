#!/bin/bash

CURRENTPATH=`pwd`
CONFIGFILE="${1:-SimulationConfigFile.txt}"

python3 pythonscripts/merge_topas_results.py $CURRENTPATH $CONFIGFILE


