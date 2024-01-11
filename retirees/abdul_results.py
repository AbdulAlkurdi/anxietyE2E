'''OUTDATED'''

import os
import pandas as pd 
import sys

#path2 = '/mnt/d/Users/alkurdi/anxietyE2E/results_archive'
#path2 = "/mnt/d/Users/alkurdi/OneDrive - University of Illinois - Urbana/delta_old_results/e2e"
general_path = '/mnt/d/Users/alkurdi/OneDrive - University of Illinois - Urbana/delta_old_results'
path2 = "/mnt/d/Users/alkurdi/OneDrive - University of Illinois - Urbana/delta_old_results/e2e"


# walk paths


# walk paths
#df.columns(['model','dataset','accuracy','precision','recall','f1','auc','time', 'it', 'fold', 'tune' ])
complete_results = pd.DataFrame()
#complete_results.columns=['model','dataset','accuracy','precision','recall','f1','auc','time', 'it', 'fold', 'tune' ]
i=0
#n=10
identifier = path2.split('/')[-1]
big_identifier = path2.split('/')[-2]

def find_result_roots(general_path):
    i =0
    maps = []
    for root, dirs, files in os.walk(general_path):
        for dir in dirs:        
            
            if 'results' in dir:
                i+=1 
                maps.append([root,dir])
                #print(root)
                #print(dir)
     
            
                
                if i%50==0: print(i)
    return maps
output = find_result_roots(general_path)
#print(output)

for entry in output:
    print('root', entry[0])
    print('dir',entry[1])

    for root, dirs, files in os.walk( entry[0]):
        
        for file in files:
            if 'trials_objs' in root: break
            else: pass
            if 'metrics' in file:
                save_path = root + '/../../../../..'
                #print(root)
                rt_splt = root.split('/')
                metrics = pd.read_csv(root+'/'+file)
                #print(rt_splt)
                metrics['iter'] = int(rt_splt[-1][-2:])+1
                metrics['fold'] = int(root[-2:])+1
                metrics['tune'] = int(rt_splt[-3][-2:])+1
                metrics['model'] = rt_splt[-2]
                metrics['dataset'] = rt_splt[-4].split('_')[0]
                #print(rt_splt)
                #print(rt_splt[-5].split('_')[2])
                #print('snr', rt_splt[-5].split('_')[2])
            
                metrics['snr'] = rt_splt[-4].split('_')[2]
                #print('snr', metrics['snr'])
            #terminate loop
                complete_results = pd.concat([complete_results, metrics], ignore_index=True)
            #if i==n: break
            #else: None
        #print every 100
        if i%100==0:
            print(i)
            #if i==n: break
    identifier = '_'.join(save_path.split('/')[-12:-9])
    print(f'{root}/{identifier}_complete_results.csv')
    #complete_results.to_csv(f'{root}/{identifier}_complete_results.csv')
    
#print(save_path)
#print(os.listdir(save_path))
#print(i)
#identifier = '_'.join(save_path.split('/')[-12:-9])
#print('identifier', identifier)

#print(complete_results)
#if big_identifier ==  'anxietyE2E' :
#    complete_results.to_csv(f'{path2}/e2e_copy{identifier}_complete_results.csv')
#else:
#    



