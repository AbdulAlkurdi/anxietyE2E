# Set up environment
```
conda env create -f environment_mod.yml -n TFwesad
conda activate TFwesad
```
 

Check the version of python (the output should be Python 3.8.13)
```
python --version
```
 

Install additional packages:

```
pip install git+https://www.github.com/keras-team/keras-contrib.git
pip install nvidia-pyindex
pip install nvidia-tensorflow
pip install git+https://github.com/xflr6/graphviz.git0.13.2
```
