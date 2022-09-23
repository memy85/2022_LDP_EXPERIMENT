#!/bin/bash

cd src 

python3 classify.py --name RBC --type lm --epsilon 0.1
python3 classify.py --name RBC --type lm --epsilon 0.2
python3 classify.py --name RBC --type lm --epsilon 0.4
python3 classify.py --name RBC --type lm --epsilon 0.8
python3 classify.py --name RBC --type lm --epsilon 1.6
python3 classify.py --name RBC --type lm --epsilon 3.2
python3 classify.py --name RBC --type lm --epsilon 6.4

python3 classify.py --name RBC --type new_lm --epsilon 0.1
python3 classify.py --name RBC --type new_lm --epsilon 0.2
python3 classify.py --name RBC --type new_lm --epsilon 0.4
python3 classify.py --name RBC --type new_lm --epsilon 0.8
python3 classify.py --name RBC --type new_lm --epsilon 1.6
python3 classify.py --name RBC --type new_lm --epsilon 3.2
python3 classify.py --name RBC --type new_lm --epsilon 6.4

echo "ended RBC"

python3 classify.py --name BP --type lm --epsilon 0.1
python3 classify.py --name BP --type lm --epsilon 0.2
python3 classify.py --name BP --type lm --epsilon 0.4
python3 classify.py --name BP --type lm --epsilon 0.8
python3 classify.py --name BP --type lm --epsilon 1.6
python3 classify.py --name BP --type lm --epsilon 3.2
python3 classify.py --name BP --type lm --epsilon 6.4

python3 classify.py --name BP --type new_lm --epsilon 0.1
python3 classify.py --name BP --type new_lm --epsilon 0.2
python3 classify.py --name BP --type new_lm --epsilon 0.4
python3 classify.py --name BP --type new_lm --epsilon 0.8
python3 classify.py --name BP --type new_lm --epsilon 1.6
python3 classify.py --name BP --type new_lm --epsilon 3.2
python3 classify.py --name BP --type new_lm --epsilon 6.4

echo "ended all"
cd ../