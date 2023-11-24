#!/bin/bash

#for clas in cnnM resnetM; do
#    for max_eval in $(seq 1 10); do
#        sbatch job.sbatch $clas $max_eval
#    done;
#done;

for max_eval in $(seq 1 10); do
  for  i_fold in 00 01 02 03 04; do
    for clas in  fcnM cnnM resnetM mcdcnnM  inceptionM stresnetM encoderM  mlpM mlpLstmM cnnLstmM; do 
      sbatch training.sbatch $i_fold $clas $max_eval
    done
  done
done
