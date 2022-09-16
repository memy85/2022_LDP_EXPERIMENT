#!/bin/bash

function create_lm_data {
    python3 lm_simulation.py --name BP
    python3 lm_simulation.py --name CRP
    python3 lm_simulation.py --name glucose
    python3 lm_simulation.py --name RBC
}

function create_new_lm_data {
    python3 new_lm_simulation.py --name BP
    python3 new_lm_simulation.py --name CRP
    python3 new_lm_simulation.py --name glucose
    python3 new_lm_simulation.py --name RBC
}

function simulate {
    create_lm_data && create_new_lm_data
    echo "simulation finished!"
}

cd src
simulate 
cd ../