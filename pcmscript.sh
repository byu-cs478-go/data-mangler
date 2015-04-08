#!/bin/bash

for x in $@; do
    python3 src/main.py $x results_3/$(basename $x).arff
done
