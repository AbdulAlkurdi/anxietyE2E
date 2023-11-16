import os
import sys
from datetime import datetime
current_dateTime = datetime.now()
import logging
logging.basicConfig(filename=f'logs/{current_dateTime}.log', level=logging.INFO)
if __name__ == '__main__':

	#_, dataset_name, classifier, max_eval, num_iteration = sys.argv
	#_, classifier = sys.argv
	files = []
	max_eval = 10
	num_iteration = 10
	data_dir = "results"
	dataset_name = 'wesad'
	for classifier in  ['mcdcnnM', 'cnnM', 'stresnetM', 'mlpM', 'fcnM', 'encoderM', 'resnetM', 'inceptionM',
                             'mlpLstmM', 'cnnLstmM']:
		for dataset_fold in range(5):
			for tune_trial in range((max_eval)):
				for iteration in range((num_iteration)):
					path = f"{data_dir}/{dataset_name}_5fold_{dataset_fold:02d}/tune_{tune_trial:02d}/{classifier}/it_{iteration:02d}"
					if (os.path.exists(path)):
						logging.info(f"Results for {dataset_name}, {path} already exists")
					else:
						logging.info(f"Results for {dataset_name}, {path} missing")
