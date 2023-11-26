#!/bin/bash -l

#SBATCH --mem=16g
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=gpuA100x4
#SBATCH --account=bbnp-delta-gpu
#SBATCH --job-name=encoder_wesad_reduced
#SBATCH --time=06:00:00      # hh:mm:ss for the job
#SBATCH --constraint="scratch"
#SBATCH --gpus-per-node=1
#SBATCH -o ./job_logs/job_"$SLURM_JOB_ID"_%x_%j.out
#SBATCH --mail-user=alkurdi2@illinois.edu
#SBATCH --mail-type="END"

module list
conda activate TFwesad

echo "job is starting on `hostname`"
cd /projects/bbnp/anxietyE2E

dataset="wesad"



echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"


for clas in encoderM; do
  for dataset in wesad; do
    for max_eval in $(seq 1 10); do
      for i_fold in 00 01 02 03 04; do
        srun python tune_one.py "$1" "$dataset"_fold_05_"$i_fold" $clas "$max_eval"
      done
    done
  done
done

echo "Done"
date

