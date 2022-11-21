#!/bin/bash

### functions 
### 1. simulation functions

function create_lm_data {
    python3 src/1_simulation/lm_simulation.py
}

function create_new_lm_data {
    python3 src/1_simulation/new_lm_simulation.py 
}

function simulate {
    echo "starting simulation ..."
    create_lm_data
    echo "finished lm simulation"
    create_new_lm_data
    echo "simulation finished!"
}

### 2. evaluation


"$@"