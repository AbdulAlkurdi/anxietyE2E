# Profiling Instructions
Below are the instructions for how to profile the code and generate an output image. These instructions will go over how to profile the jobs in the job.sbatch file,
but it can also be extrapolated for all batch jobs.

## Intrsuctions for job.sbatch
instructions to the job.sbatch file
### Obtain the Batch file
First navigate into the directory that you want the .sbatch file to be in

run the following command to copy the job into your desired directory 

``cp /projects/bbyn/katerina/anxietyE2E/job.sbatch . ``

### Create a new file
create a copy of the job.sbatch file with the following command

``cp job.sbatch new_job.sbatch ``

### Edit the code
Open new_job.sbatch in an editor (vim, nano, etc.)

delete the following line

``srun python tune_one.py $CUDA_VISIBLE_DEVICES "$dataset"_fold_05_"$i_fold" $clas "$max_eval"``

replace it with the following line

``srun python -m cProfile -o output.pstats tune_one.py $CUDA_VISIBLE_DEVICES "$dataset"_fold_05_"$i_fold" $clas "$max_eval"``

### Create a New Environment
at this point, you must create and enter into a new environment to run the ensuing commands. Run the following commands to do so

``conda create --name profile python=3.9
conda activate profile
pip install gprof2dot
pip install graphviz ``

### Run the Batch Job
You need to run the batch job to create the output.pstats file needed to generate the image. Run the following command to do so

`` sbatch --job-name=cnnM_1 job.sbatch cnnM 1``

note, you can choose the classifier, names, and max eval of your choice. This method is the one that runs the fastest. the general template is below

`` sbatch --job-name=<name> job.sbatch <classifier> <max eval>``

the list of possible classifiers is as follows

``CLASSIFIERS = ("mcdcnnM", "cnnM", "mlpM", "fcnM", "encoderM", "resnetM", "inceptionM", "stresnetM", "mlpLstmM", "cnnLstmM") ``

### Create the image
run the following command to create the image, output.png

``gprof2dot --colour-nodes-by-selftime -f pstats output.pstats |     dot -Tpng -o output.png``

**Note**: You will need programs gprof2dot and dot, which are available on Mahuika and Maui. Use ``conda install gprof2dot``. Package graphviz is already installed in the TFwesad environment.

### Copy image to local machine
In order to view the image, you will need to copy it to your local machine with the following command. Run this on your LOCAL MACHINE.

``scp <username>@login.delta.ncsa.illinois.edu:<your current filepath>/output.png <directory you want to copy to>``

## General Instructions 
Below are the general instructions on how to profile any batch job.

## Create a Batch job
Create a .sbatch file that calls the program that you want to run. 

make sure to include the following line

``srun python -m cProfile -o output.pstats <other needed parameters>``

the other parameters needed to run the program will vary by case. Some important parameters will include dataset name, max number of evaluations, classifer name, and visible devices.

### Create a New Environment
at this point, you must create and enter into a new environment to run the ensuing commands. Run the following commands to do so

``conda create --name profile python=3.9
conda activate profile
pip install gprof2dot
pip install graphviz ``

### Run the Batch Job
You need to run the batch job to create the output.pstats file needed to generate the image. Run the following command to do so.

`` sbatch --job-name=<name> <batch file name> <classifier> <max eval>``

the list of possible classifiers is as follows

``CLASSIFIERS = ("mcdcnnM", "cnnM", "mlpM", "fcnM", "encoderM", "resnetM", "inceptionM", "stresnetM", "mlpLstmM", "cnnLstmM") ``

### Create the image
run the following command to create the image, output.png

``gprof2dot --colour-nodes-by-selftime -f pstats output.pstats |     dot -Tpng -o output.png``

### Copy image to local machine
In order to view the image, you will need to copy it to your local machine with the following command. Run this on your LOCAL MACHINE.

``scp <username>@login.delta.ncsa.illinois.edu:<your current filepath>/output.png <directory you want to copy to>``





