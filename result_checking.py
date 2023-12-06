import os
import sys
if __name__ == '__main__':
	i=0
	#_, dataset_name, classifier, max_eval, num_iteration = sys.argv
	max_eval = 10
	num_iteration = 5
	dataset_name = 'WESAD'
	data_dir = "../new_delta_results/results_n_5_snr_0.15"
	for classifier in ['fcnM', 'resnetM', 'mcdcnnM',
					    'cnnM', 'inceptionM', 'encoderM',
						'mlpM', 'mlpLstmM', 'cnnLstmM']: #, 'stresnetM'
		print(classifier)
		for dataset_fold in range(5):
			for tune_trial in range(int(max_eval)):
				for iteration in range(int(num_iteration)):
					path = f"{data_dir}/{dataset_name}_5fold_{dataset_fold:02d}/tune_{tune_trial:02d}/{classifier}/it_{iteration:02d}"
					if os.path.isdir(path+'/DONE'):
						#print(f"Results for {classifier}, {dataset_name}, fold {dataset_fold}, tune {tune_trial}, iteration {iteration} already exists")
						pass
					else:
						print(f"Results for {classifier}, {dataset_name}, fold {dataset_fold}, tune {tune_trial}, iteration {iteration} missing")
						i+=1
	print('missing cases: ',i)
