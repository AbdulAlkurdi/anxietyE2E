# This script was created because of probable memory leakage in version of tensorflow/keras used in this project
for clas in cnnM mcdcnnM fcnM mlpM mlpLstmM cnnLstmM InceptionM resnetM encoderM stresnetM; do #cnnLstmM mlpLstmM mlpM encoderM  
  for dataset in wesad; do
    for max_eval in $(seq 1 10); do
      for i_fold in 00 01 02 03 04; do
        python tune_two-2.py "$0" "$dataset"_fold_05_"$i_fold" $clas "$max_eval"
      done
    done
  done
done
