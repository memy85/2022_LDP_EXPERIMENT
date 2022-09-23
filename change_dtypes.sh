#!/bin/bash

cd src

python3 change_data_types.py --name BP --type new_lm &
python3 change_data_types.py --name RBC --type lm & python3 change_data_types.py --name RBC --type new_lm

cd ../

echo "finished all process"
