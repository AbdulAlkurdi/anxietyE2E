import os
import sys
if __name__ == '__main__':

	_, dataset_name, classifier, max_eval, num_iteration = sys.argv

	data_dir = "results"

	for dataset_fold in range(5):
		for tune_trial in range(int(max_eval)):
			for iteration in range(int(num_iteration)):
				
				path = f"{data_dir}/{dataset_name}_5fold_{dataset_fold:02d}/tune_{tune_trial:02d}/{classifier}/it_{iteration:02d}"
				print(path)
				if (os.path.exists(path)):
					print(f"Results for {classifier}, {dataset_name}, fold {dataset_fold}, tune {tune_trial}, iteration {iteration} already exists")
				else:
					print(f"Results for {classifier}, {dataset_name}, fold {dataset_fold}, tune {tune_trial}, iteration {iteration} missing")
