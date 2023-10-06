# Set up environment

## Obtain .yml file
if your environment does not contain the file environment_mod.yml, you will have to copy it from this github directory. To complete this step you will have to complete the following steps

1.Download the environment_mod.yml file from this directory
2.Copy the file from your local machine to your Delta machine using the following command

```
scp module_environment.yml<your username>@login.delta.ncsa.illinois.edu
:/u/<your username>

```

##Build the environment
Run the following commands to create and activate your environment
```
conda env create -f environment_mod.yml -n TFwesad
conda activate TFwesad
```
 
##Python Version Check
Check the version of python (the output should be Python 3.8.13)
```
python --version
```

If you do not have the correct version of Python, run the following commands
```
export PATH=/u/<your username>/.conda/envs/TFwesad/bin:$PATH
export PYTHONPATH=/u/<your username>/.conda/envs/TFwesad/lib/python3.8/site-packages
```

##Install additional packages:
Run the following commands to install neccesary packages
```
pip install git+https://www.github.com/keras-team/keras-contrib.git
pip install nvidia-pyindex
pip install nvidia-tensorflow[horovod]
pip install git+https://github.com/xflr6/graphviz.git@0.13.2
```

##Commands in one block
Below are the commands listed in one block for a quick setup. This assumes that you have not copied the .yml file and does not include the Python version check. Please fill out the <your username> section of the first command before running.

```
scp module_environment.yml<your username>@login.delta.ncsa.illinois.edu
:/u/<your username>
conda env create -f environment_mod.yml -n TFwesad
conda activate TFwesad
pip install git+https://www.github.com/keras-team/keras-contrib.git
pip install nvidia-pyindex
pip install nvidia-tensorflow[horovod]
pip install git+https://github.com/xflr6/graphviz.git@0.13.2
```
