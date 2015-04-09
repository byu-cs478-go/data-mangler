#!/bin/bash

for x in $@; do
    python3 src/main.py $x results/$(basename $x).arff
done
