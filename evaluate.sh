#!/bin/bash

function check_figure1 {
    project_path=$(python3 src/utils.py --read_config True)
    echo "This is the project directory : $project_path"
}

function figure1 {
    python3 src/2_evaluation/figure1.py
}

function figure2 {
    bash 2_preprocess4fig2.sh
    bash test_classification.sh
    python3 src/2_evaluation/table1.py
    python3 src/2_evaluation/figure2.py
}


"$@"