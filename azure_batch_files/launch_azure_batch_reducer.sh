#!/bin/bash

SIMULATIONTPATH=`pwd`
BATCHPATH='/home/hector/AzureBatch'
cd $BATCHPATH
python3 batch_data_reducer.py $SIMULATIONTPATH/simconfig.json

