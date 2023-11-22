import configparser

from arpreprocessing.wesad import Wesad
from utils.loggerwrapper import GLOBAL_LOGGER
import warnings
warnings.filterwarnings("ignore")
if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")
    dataset = Wesad(GLOBAL_LOGGER, config['Paths']['wesad_dir']).get_dataset()
    dataset.save(config['Paths']['mts_out_dir'])

 