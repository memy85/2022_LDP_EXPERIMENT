#!/bin/bash

function check_figure1 {
    project_path=$(python3 src/utils.py --read_config True)
    echo "This is the project directory : $project_path"
}

function figure1 {
    python3 src/2_evaluation/figure1.py
}

function figure2 {
    # echo "preprocessing .. "
    # bash 2_preprocess4fig2.sh

    echo "testing classification .."
    bash test_classification.sh

    echo "making table 1 .."
    python3 src/2_evaluation/table1.py

    echo "making figure 2 .."
    python3 src/2_evaluation/figure2.py
}


"$@"