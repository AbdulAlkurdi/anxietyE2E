# This script was created because of probable memory leakage in version of tensorflow/keras used in this project
for clas in inceptionM ; do #cnnM mcdcnnM fcnM mlpM mlpLstmM cnnLstmM InceptionM resnetM encoderM stresnetM; do #cnnLstmM mlpLstmM mlpM encoderM  
  for dataset in wesad; do
    for i_fold in 04 03 02 01 00; do #max_eval in $(seq 7 10); do
      for max_eval in $(seq 7 10); do # i_fold in 04 03 02 03 04; do
        python tune_two-2.py "$0" "$dataset"_fold_05_"$i_fold" $clas "$max_eval"
      done
    done
  done
done
