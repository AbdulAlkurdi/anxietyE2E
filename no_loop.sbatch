#!/bin/bash -l

#SBATCH --mem=16g
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1  
#SBATCH --partition=gpuA40x4
#SBATCH --account=bbyn-delta-gpu
#SBATCH --job-name=wesad
#SBATCH --time=48:00:00      # hh:mm:ss for the job
#SBATCH --constraint="scratch"
#SBATCH --gpus-per-node=1
#SBATCH -o ./job_logs/job_%x_%j.out
#SBATCH --mail-user=louislidelta@gmail.com
#SBATCH --mail-type="END" 
 
module list
conda activate TFwesad

echo "job is starting on `hostname`"
cd /projects/bbyn/lli4/anxietyE2E

dataset="wesad"
clas=$1
max_eval=$2

echo "dataset=$dataset"
echo "clas=$clas"
echo "max_eval=$max_eval"
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"

for i_fold in 00; do

  echo " "
  echo " ******************************"	
  echo " ******* i_fold=$i_fold *******"
  echo " ******************************"
  echo " "
  date
  srun python tune_one.py $CUDA_VISIBLE_DEVICES "$dataset"_fold_05_"$i_fold" $clas "$max_eval"
done

echo "Done"
date

