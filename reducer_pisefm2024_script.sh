#!/bin/bash


SIMULATIONTPATH=$1
CONFIGFILE=$2
cp $CONFIGFILE $SIMULATIONTPATH
cd $SIMULATIONTPATH
SIMULATIONTPATH=$(pwd)
CONFIGFILE=$(pwd)/simconfig.json

PYPATH="/home/radiofisica/hector/mytopassimulations/MyTOPASPythonScripts"
cd "$PYPATH"
source venv/bin/activate
python3 reduce_CellsNPs_files.py "$SIMULATIONTPATH" "$CONFIGFILE"
deactivate

