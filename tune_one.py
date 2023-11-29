import sys
import os
from experiment.hyperparametertuning import HyperparameterTuning
from experiment.wesadexperiment import WesadExperimentNFold
from utils.loggerwrapper import GLOBAL_LOGGER
from utils.utils import set_available_gpus
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import warnings
warnings.filterwarnings("ignore")

# flag to enable automatic mixed precision 
# os.environ['TF_ENABLE_AUTO_MIXED_PRECISION'] = '1'



def get_dataset(name):
    if name.startswith("wesad_fold_"):
        return WesadExperimentNFold(GLOBAL_LOGGER, int(name[-5:-3]), int(name[-2:]))
    raise Exception(f"No such dataset/experiment as {name}")


if __name__ == '__main__':
    try:
        _, gpu_id, dataset_name, clas, max_eval = sys.argv

        set_available_gpus(gpu_id)
        dataset = get_dataset(dataset_name)

        HyperparameterTuning(dataset, [gpu_id]).tune_one(clas, int(max_eval))

    except Exception as e:
        GLOBAL_LOGGER.exception(e)
        raise e
