#!/bin/bash


python3 src/2_evaluation/classify.py --name RBC --type lm --epsilon 0.1
python3 src/2_evaluation/classify.py --name RBC --type lm --epsilon 0.2
python3 src/2_evaluation/classify.py --name RBC --type lm --epsilon 0.4
python3 src/2_evaluation/classify.py --name RBC --type lm --epsilon 0.8
python3 src/2_evaluation/classify.py --name RBC --type lm --epsilon 1.6
python3 src/2_evaluation/classify.py --name RBC --type lm --epsilon 3.2
python3 src/2_evaluation/classify.py --name RBC --type lm --epsilon 6.4

python3 src/2_evaluation/classify.py --name RBC --type new_lm --epsilon 0.1
python3 src/2_evaluation/classify.py --name RBC --type new_lm --epsilon 0.2
python3 src/2_evaluation/classify.py --name RBC --type new_lm --epsilon 0.4
python3 src/2_evaluation/classify.py --name RBC --type new_lm --epsilon 0.8
python3 src/2_evaluation/classify.py --name RBC --type new_lm --epsilon 1.6
python3 src/2_evaluation/classify.py --name RBC --type new_lm --epsilon 3.2
python3 src/2_evaluation/classify.py --name RBC --type new_lm --epsilon 6.4

echo "ended RBC"

python3 src/2_evaluation/classify.py --name glucose --type lm --epsilon 0.1
python3 src/2_evaluation/classify.py --name glucose --type lm --epsilon 0.2
python3 src/2_evaluation/classify.py --name glucose --type lm --epsilon 0.4
python3 src/2_evaluation/classify.py --name glucose --type lm --epsilon 0.8
python3 src/2_evaluation/classify.py --name glucose --type lm --epsilon 1.6
python3 src/2_evaluation/classify.py --name glucose --type lm --epsilon 3.2
python3 src/2_evaluation/classify.py --name glucose --type lm --epsilon 6.4

python3 src/2_evaluation/classify.py --name glucose --type new_lm --epsilon 0.1
python3 src/2_evaluation/classify.py --name glucose --type new_lm --epsilon 0.2
python3 src/2_evaluation/classify.py --name glucose --type new_lm --epsilon 0.4
python3 src/2_evaluation/classify.py --name glucose --type new_lm --epsilon 0.8
python3 src/2_evaluation/classify.py --name glucose --type new_lm --epsilon 1.6
python3 src/2_evaluation/classify.py --name glucose --type new_lm --epsilon 3.2
python3 src/2_evaluation/classify.py --name glucose --type new_lm --epsilon 6.4

echo "ended glucose"

python3 src/2_evaluation/classify.py --name BP --type lm --epsilon 0.1
python3 src/2_evaluation/classify.py --name BP --type lm --epsilon 0.2
python3 src/2_evaluation/classify.py --name BP --type lm --epsilon 0.4
python3 src/2_evaluation/classify.py --name BP --type lm --epsilon 0.8
python3 src/2_evaluation/classify.py --name BP --type lm --epsilon 1.6
python3 src/2_evaluation/classify.py --name BP --type lm --epsilon 3.2
python3 src/2_evaluation/classify.py --name BP --type lm --epsilon 6.4

python3 src/2_evaluation/classify.py --name BP --type new_lm --epsilon 0.1
python3 src/2_evaluation/classify.py --name BP --type new_lm --epsilon 0.2
python3 src/2_evaluation/classify.py --name BP --type new_lm --epsilon 0.4
python3 src/2_evaluation/classify.py --name BP --type new_lm --epsilon 0.8
python3 src/2_evaluation/classify.py --name BP --type new_lm --epsilon 1.6
python3 src/2_evaluation/classify.py --name BP --type new_lm --epsilon 3.2
python3 src/2_evaluation/classify.py --name BP --type new_lm --epsilon 6.4

echo "ended BP"

python3 src/2_evaluation/classify.py --name CRP --type lm --epsilon 0.1
python3 src/2_evaluation/classify.py --name CRP --type lm --epsilon 0.2
python3 src/2_evaluation/classify.py --name CRP --type lm --epsilon 0.4
python3 src/2_evaluation/classify.py --name CRP --type lm --epsilon 0.8
python3 src/2_evaluation/classify.py --name CRP --type lm --epsilon 1.6
python3 src/2_evaluation/classify.py --name CRP --type lm --epsilon 3.2
python3 src/2_evaluation/classify.py --name CRP --type lm --epsilon 6.4

python3 src/2_evaluation/classify.py --name CRP --type new_lm --epsilon 0.1
python3 src/2_evaluation/classify.py --name CRP --type new_lm --epsilon 0.2
python3 src/2_evaluation/classify.py --name CRP --type new_lm --epsilon 0.4
python3 src/2_evaluation/classify.py --name CRP --type new_lm --epsilon 0.8
python3 src/2_evaluation/classify.py --name CRP --type new_lm --epsilon 1.6
python3 src/2_evaluation/classify.py --name CRP --type new_lm --epsilon 3.2
python3 src/2_evaluation/classify.py --name CRP --type new_lm --epsilon 6.4

echo "ended CRP"

echo "ended all"