#!/bin/bash


cd src

python3 process_for_figures.py --name RBC --type lm & python3 process_for_figures.py --name BP --type lm

echo "half finished"

python3 process_for_figures.py --name RBC --type new_lm & python3 process_for_figures.py --name BP --type new_lm

cd ../

echo "Process finished"
