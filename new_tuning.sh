#!/bin/bash

for clas in cnnM resnetM; do

    for max_eval in $(seq 1 10); do

        sbatch job.sbatch $clas $max_eval
    done;
done;
