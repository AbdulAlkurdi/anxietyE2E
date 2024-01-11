# This script was created because of probable memory leakage in version of tensorflow/keras used in this project
for clas in mcdcnnM cnnM mlpM mlpLstmM cnnLstmM fcnM inceptionM resnetM encoderM stresnetM; do
    for max_eval in $(seq 0 10); do
        for i_fold in 00 01 02 03 04; do
          python tune_one.py "0" wesad_fold_05_"$i_fold" $clas "$max_eval"
        done
    done
done