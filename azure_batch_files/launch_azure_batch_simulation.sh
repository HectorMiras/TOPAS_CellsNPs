#!/bin/bash

SIMULATIONTPATH=`pwd`
BATCHPATH='/home/hector/AzureBatch'
cd $BATCHPATH
python3 batch_simulation_runner.py $SIMULATIONTPATH/simconfig.json

