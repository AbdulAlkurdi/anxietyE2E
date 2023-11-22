import os
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import classification_report
import warnings
from multiprocessing import Pool
import concurrent.futures

from time import time
from tqdm import tqdm
import logging
logging.basicConfig(filename='logs/analyze_all_case_results.log',filemode='w', level=logging.INFO)

all_results_repos = {'name': 'Path'}
all_results_repos['anxietyE2E/results_archive'] = '/mnt/d/Users/alkurdi/anxietyE2E/results_archive'
all_results_repos['anxietyE2E/results'] = '/mnt/d/Users/alkurdi/anxietyE2E/results'
all_results_repos['anxietyE2E/results_reduced'] = '/mnt/d/Users/alkurdi/anxietyE2E/results_reduced'
all_results_repos['wsl2 may2023'] = '/mnt/d/Users/alkurdi/from_wsl2_created_may_23/wsl2_e2e/results'
all_results_repos['delta old e2e_snr_0.5'] = '/mnt/d/Users/alkurdi/delta_old_results/e2e/e2e/results_snr_0.5'
all_results_repos['delta old e2e_copy_snr_0.1'] = '/mnt/d/Users/alkurdi/delta_old_results/e2e/e2e_copy/results_snr_0.1'
all_results_repos['delta old e2e_copy_snr_0.2'] = '/mnt/d/Users/alkurdi/delta_old_results/e2e/e2e_copy/results_snr_0.2'
all_results_repos['delta old e2e_copy_snr_0.5'] = '/mnt/d/Users/alkurdi/delta_old_results/e2e/e2e_copy/results_snr_0.5'
all_results_repos['delta old e2e_copy2_snr_0.01'] = '/mnt/d/Users/alkurdi/delta_old_results/e2e/e2e_copy2/results_snr_0.01'
all_results_repos['delta old e2e_copy2_snr_0.1'] = '/mnt/d/Users/alkurdi/delta_old_results/e2e/e2e_copy2/results_snr_0.1'
all_results_repos['delta old e2e_copy2_snr_0.2'] = '/mnt/d/Users/alkurdi/delta_old_results/e2e/e2e_copy2/results_snr_0.2'
all_results_repos['delta old e2e_copy2_snr_0.5'] = '/mnt/d/Users/alkurdi/delta_old_results/e2e/e2e_copy2/results_snr_0.5'
all_results_repos['delta old e2e_snr_0.2_snr_0.2'] = '/mnt/d/Users/alkurdi/delta_old_results/e2e/e2e_snr_0.2/results_snr_0.2'
all_results_repos['delta old e2e_snr_0.2_snr_0.5'] = '/mnt/d/Users/alkurdi/delta_old_results/e2e/e2e_snr_0.2/results_snr_0.5'
all_results_repos['bbyn katerina snr_0.5'] = '/mnt/d/Users/alkurdi/delta_old_results/e2e_bbyn/katerina/results_snr_0.5'
all_results_repos['bbyn katerina snr_0.5_save'] = '/mnt/d/Users/alkurdi/delta_old_results/e2e_bbyn/katerina/results_snr_0.5_save'


warnings.filterwarnings("ignore")
done_list = {}
master_ledger = {'name':['df_best_model', 'df_metrics', 'history', 'predictions', 'result', 'aggregated_classification_reports', 'done']}
if os.path.isfile('/mnt/d/Users/alkurdi/master_ledger.pkl'):
    with open('/mnt/d/Users/alkurdi/master_ledger.pkl', 'rb') as handle:
        master_ledger = pickle.load(handle)
else:
        
    for name, Path in all_results_repos.items():
        if name != 'name':        
            fold_gen = (i for i in os.listdir(Path) if 'WESAD' in i)
            for fold in fold_gen:
                tune_gen = (i for i in os.listdir(Path+'/'+fold) if 'tune' in i)
                for tune in tune_gen:
                    model_gen = (i for i in os.listdir(Path+'/'+fold+'/'+str(tune)))
                    for model in model_gen:
                        it_gen = ( i for i in os.listdir(Path+'/'+fold+'/'+str(tune)+'/'+model) if 'it' in i)
                        for it in it_gen:
                            try: 
                                in_path = Path+'/'+fold+'/'+str(tune)+'/'+model+'/'+str(it)
                                df_best_model = pd.read_csv(in_path+'/df_best_model.csv')
                                df_metrics = pd.read_csv(in_path+'/df_metrics.csv')
                                history = pd.read_csv(in_path+'/history.csv')
                                aggregated_classification_reports = {}
                                metrics = ["precision", "recall", "f1-score", "support"]
                                with open(in_path+'/predictions.txt') as f:
                                    y_true = [int(x) for x in f.readline().split()]
                                    if len(aggregated_classification_reports) == 0:
                                        for clas in set(y_true):
                                            aggregated_classification_reports[clas] = {"f1-score": [], "precision": [], "recall": [],
                                                                                        "support": []}
                                    y_pred = [int(x) for x in f.readline().split()]
                                    report = classification_report(y_true, y_pred, output_dict=True)
                                    for clas in aggregated_classification_reports:
                                        for metric in metrics:
                                            aggregated_classification_reports[clas][metric].append(report[str(clas)][metric])
                                result = []
                                for clas in aggregated_classification_reports:
                                    row = ['WESAD', clas]
                                    for metric in metrics:
                                        metric_values = aggregated_classification_reports[clas][metric]
                                        row.append(np.mean(metric_values))
                                        row.append(np.std(metric_values))
                                    result.append(row[:-1])  # Remove support std
                                is_done = os.path.isdir(in_path+'/DONE')
                                #
                                if is_done:
                                    done_list[in_path] = is_done
                                master_ledger[name+'_'+fold+'_'+tune+'_'+model+'_'+it] = [df_best_model, df_metrics, history, result, aggregated_classification_reports, is_done]
                            except Exception as e:
                                master_ledger[name+'_'+fold+'_'+tune+'_'+model+'_'+it] = [None, None, None, None, None, None]
                                #print('during '+name+'_'+fold+'_'+tune+'_'+model+'_'+it+' an error occured: ')
                                #print(e)
                                continue                    

    with open('/mnt/d/Users/alkurdi/master_ledger.pkl', 'wb') as handle:
        pickle.dump(master_ledger, handle, protocol=pickle.HIGHEST_PROTOCOL)


#create a multiprocess function to run the following code in parallel

def process_each_ledger(key):
    try:
        ledger_df = pd.DataFrame()
        if key != 'name':  
            case_df = pd.DataFrame()
            if master_ledger[key][-2] is None:
                pass
            else: 
                case_df['f1 binary']= master_ledger[key][-2][1]['f1-score']
                pass
            for ind in master_ledger[key]:
                pass
            #logging.info(key.split('_'))
            #logging.info('it'+key.split('_')[-1] + '|' + 'model'+key.split('_')[-2] + '|' + 'tune'+key.split('_')[-3] + '|' + 'fold'+key.split('_')[-4] + '|' + 'name'+key.split('_')[-5] + '|' + 'repo'+key.split('_')[-6])
            case_df['is_done'] = master_ledger[key][-1]
            case_df['it'] = key.split('_')[-1]
            case_df['model'] = key.split('_')[-3]
            case_df['tune'] = key.split('_')[-4]
            case_df['fold'] = key.split('_')[-6]
            #logging.info('it'+key.split('_')[-1] + '|' + 'model'+key.split('_')[-3] + '|' + 'tune'+key.split('_')[-4] + '|' + 'fold'+key.split('_')[-5])
            
            case_df['name'] = key
            ledger_df = pd.concat([ledger_df, master_ledger[key][0], master_ledger[key][1], case_df], axis = 1)
    except Exception as e:
        logging.info(e)
        pass
    return ledger_df








start_time = time()
ledger_results = []
with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_each_ledger, i) for i in master_ledger.keys()]
        done, not_done = concurrent.futures.wait(futures, return_when='ALL_COMPLETED')
        logging.debug(f'done assigning futures, now waiting for them to finish')
        for future in done:
            ledger_results.append(future.result())
        
imax =len(master_ledger)

logging.info(f'finished {imax} iterations in {round(time()-start_time,2)} seconds')
logging.info(f'an average of {(time()-start_time)/imax} seconds per iteration')


master_ledger_df = pd.concat(ledger_results)
with open('/mnt/d/Users/alkurdi/master_ledger_df.pkl', 'wb') as f:
            pickle.dump(master_ledger_df, f)
            

