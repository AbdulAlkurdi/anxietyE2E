import os
import pandas as pd
import pickle
from time import time
subject_ids = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17]
o = time()
root = r'archives/WESAD'
for i in subject_ids:#subject_ids:
    subject_list = pd.read_pickle(str(root+r"/S"+str(i)+r"/S"+str(i)+r'.pkl'))
    subject_list['label'][subject_list['label'] == 3] = 1
    
    dest = root + r"/S"+str(i)+r"/S"+str(i)+r"binary.pkl"
    with open(dest, 'wb') as file:
            pickle.dump(subject_list, file)
print('time to process all participats is: ',round(time()-o,2),'s')
print('that is ',round(time()-o,2)/15,'per participat for 15 total sir thas')