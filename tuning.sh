# This script was created because of probable memory leakage in version of tensorflow/keras used in this project
for clas in  stresnetM resnetM mcdcnnM cnnM inceptionM; do  #encoderM fcnM mlpM mlpLstmM cnnLstmM; do 
  for dataset in wesad; do
    for max_eval in $(seq 1 10); do
      for i_fold in 00 01 02 03 04; do
        python tune_one.py "$0" "$dataset"_fold_05_"$i_fold" $clas "$max_eval"
      done
    done
  done
done
