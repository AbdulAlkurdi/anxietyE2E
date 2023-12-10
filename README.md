## Description

### Preprocessing

Each subject and each signal is pre-processed using: 
* 3-97% winsorization, which removes extreme values from the signal data;
* Butterworth low-pass filter with 10 Hz cut-off, removes components above the threshold frequency of 10 Hz;
* downsampling, which  reduces the dimensionality of the inputs; it consequently decreases the number of learning parameters in the DL models;
* min-max normalization. 

### Used architectures
* Implementation of FCN, Resnet, Encoder, MCDCNN, Time-CNN, and MLP was based on code provided at https://github.com/hfawaz/dl-4-tsc,
* Implementation of Inception was based on code provided at https://github.com/hfawaz/InceptionTime,
* Implementation of MLP-LSTM was based on the above MLP implementation
* Implementation of CNN-LSTM was based on the description provided by [Kanjo at al.](https://doi.org/10.1016/j.inffus.2018.09.001),
* Implementation of Stresnet code was used from the previous work by [Gjoreski at al.](https://doi.org/10.1109/ACCESS.2020.2986810).

All architectures, except for MCDCNN, were adjusted for multi-source data - separate inputs for each signal. 

## How to run?

### Environment preparation

Prepare Anaconda / virtual environment with Python. Please read `setup.md`

### Data preparation

1. Create `archive` folder and put there WESAD, AMIGOS, ASCERTAIN and DECAF datasets in separate folders.
2. Create file `config.ini` with the following content:
    ```
    [Paths]
    root_dir = ... # directory path of project
    mts_out_dir = ..  # output directory for preprocessed datasets
    wesad_dir = archives/WESAD
    decaf_dir = archives/DECAF
    ascertain_dir = archives/ASCERTAIN
    amigos_dir = archives/Amigos
    ```
3. Run `ar_datasets_preprocessing.py`. Datasets should be successfully preprocessed.

### Tuning and results collection

In order to train models you need to run `.\tuning.sh X` where X is the id of GPU on which you want to run training.
If you want to gather all results, run `results.py`.

### 

to submit jobs HPC cluster, ssh login, then run a `*.sbatch`. For example, to run `no_loop`:

```
sbatch no_loop.sbatch
```

