#!/bin/bash

for x in $@; do
    python3 src/main.py $x results_2/$(basename $x).arff
done
