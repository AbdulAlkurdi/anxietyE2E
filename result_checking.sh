# This script was created because of probable memory leakage in version of tensorflow/keras used in this project
for clas in stresnetM fcnM stresnetM resnetM mcdcnnM cnnM inceptionM encoderM mlpM mlpLstmM cnnLstmM ; do
  for dataset in WESAD; do
    python result_checking.py "$dataset" $clas "10" "05" > result_check.log
  done
done
