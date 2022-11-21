#!/bin/bash

LOAD_DATA=$1

if [ "$LOAD_DATA" = true ] ; then
    echo "load data is $LOAD_DATA"
    python3 src/0_prepare_data/load_data.py

fi 
python3 src/0_prepare_data/process_data.py
python3 src/0_prepare_data/change_data_types.py

