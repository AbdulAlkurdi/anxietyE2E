# This script was created because of probable memory leakage in version of tensorflow/keras used in this project
for clas in fcnM; do
  for dataset in wesad; do
    for max_eval in $(seq 5 8); do
      for i_fold in 00; do
        echo "0" "$dataset"_fold_05_"$i_fold" $clas "$max_eval" 
      
      done
    done
  done
done
