#!/bin/bash

function create_lm_data {
    python3 lm_simulation.py --name BP
    echo "ended lm BP"
    python3 lm_simulation.py --name CRP
    echo "ended lm CRP"
    python3 lm_simulation.py --name glucose
    echo "ended lm glucose"
    python3 lm_simulation.py --name RBC
    echo "ended lm RBC"
}

function create_new_lm_data {
    python3 new_lm_simulation.py --name BP
    echo "ended new_lm BP"
    python3 new_lm_simulation.py --name CRP
    echo "ended new_lm CRP"
    python3 new_lm_simulation.py --name glucose
    echo "ended new_lm CRP"
    python3 new_lm_simulation.py --name RBC
    echo "ended new_lm RBC"
}

function simulate {
    echo "starting simulation ..."
    create_lm_data && create_new_lm_data
    echo "simulation finished!"
}

cd src
simulate 
cd ../