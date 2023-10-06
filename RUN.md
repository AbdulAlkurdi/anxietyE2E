 #Running the First Program
this document goes over how to run a program after the environment has been set up.

## Enter to New Machine
Run the following command to enter into the correct machine

```
srun --account=bbyn-delta-gpu --partition=gpuA40x4-interactive   --nodes=1 --gpus-per-node=1 --tasks=1   --tasks-per-node=1 --cpus-per-task=1 --mem=20g   --pty bash
```

## Activate the Environment
Run the following command to activate the environment
```
conda activate TFwesad
```

## Navigate to Correct Directory
navigate to the following directory

```
cd /projects/bbyn/<your username>
```

if you do not have a directory called anxietyE2E, you will have to clone it from this directory.

### Cloning the repo
Follow the following [Instructions](https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) on how to generate a Personal Access Token.
Make sure to copy and save the token after you generate it.

now clong the repo
```
git clone https://github.com/AbdulAlkurdi/anxietyE2E.git
```

You will be asked to provide your github username and a password. For the password, you will need to use your personal access token

now navigate into the cloned directory

```
cd anxietyE2E
```

## Run the Program
Run the following command to run the program
```
python tune_one.py 1 wesad_fold_05_00 cnnM 1
```
