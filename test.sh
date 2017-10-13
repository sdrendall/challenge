#! /bin/bash

export PYTHONPATH="$(pwd):$PYTHONPATH"
cat motion.tsv | python bg_analysis/main.py glucose_predictor.model | tee test_output.txt
