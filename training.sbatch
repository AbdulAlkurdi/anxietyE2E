#!/bin/bash -l

#SBATCH --mem=16g
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=6  
#SBATCH --partition=gpuA100x4
#SBATCH --account=bbnp-delta-gpu
#SBATCH --job-name=wesad_reduced
#SBATCH --time=06:00:00      # hh:mm:ss for the job
#SBATCH --constraint="scratch"
#SBATCH --gpus-per-node=1
#SBATCH -o ./job_logs/job_%x_%j_"$1"_"$2"_"$3".out
#SBATCH --mail-user=alkurdi2@illinois.edu
#SBATCH --mail-type="END" 
 
module list
conda activate TFwesad

echo "job is starting on `hostname`"
cd /projects/bbnp/anxietyE2E

dataset="wesad"

i_fold=$1
clas=$2
max_eval=$3

echo "dataset=$dataset"
echo "clas=$clas"
echo "max_eval=$max_eval"
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
echo " "
echo " ******************************"	
echo " ******* i_fold=$i_fold *******"
echo " ******************************"
echo " "
date
srun python tune_one.py $CUDA_VISIBLE_DEVICES "$dataset"_fold_05_"$i_fold" $clas "$max_eval"

echo "Done"
date

