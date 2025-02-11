#!/bin/bash


SIMULATIONTPATH=$1
CONFIGFILE=$2
cp $CONFIGFILE $SIMULATIONTPATH
cd $SIMULATIONTPATH
SIMULATIONTPATH=$(pwd)
CONFIGFILE=$(pwd)/$CONFIGFILE

PYPATH="/home/hector/mytopassimulations/MGHsimulations/pythonscripts"
cd "$PYPATH"
source venv/bin/activate
python3 reduce_CellsNPs_files.py "$SIMULATIONTPATH" "$CONFIGFILE"
deactivate

