#!/bin/bash

# ARG1: container name
# ARG2: local dir to download
# ARG3: 'Y' to download only merged results

CONTAINER=$1
ARG2=$2
cd $ARG2
DOWNLOADDIR=`pwd`
#DOWNLOADDIR=`pwd`/$CONTAINER
ONLYRESULTS=$3


BATCHPATH='/home/hector/AzureBatch'
cd $BATCHPATH
#source venv/bin/activate
python3 download_files_local.py "$CONTAINER" "$DOWNLOADDIR" "$ONLYRESULTS"
#deactivate

