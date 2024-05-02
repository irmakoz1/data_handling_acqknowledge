#ADD the blocks to each csv file

from scipy import io
import bioread
import neurokit2 as nk
import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt

#def add_blocks_physio(filepath):
filepath='C:/Users/ozarslan/Desktop/python_files/datacopies'
os.chdir(filepath)

#filename1='C:/Users/ozarslan/Desktop/python_files/datacopies/Curiosity003NS-run02_processed.csv'

for filename1 in os.listdir(filepath):
   if filename1.endswith('acq'): 
    data_neuro =nk.read_acqknowledge(filename1, sampling_rate=200)
    df = pd.DataFrame(data_neuro[0])
    df = df.rename(columns={'PPG100C': 'PPG', 'TSD160A - Differential Pressure, 2.5 cm': 'RESP', 'Digital (STP Input 7)': 'MRI-SEQ'})
    df['blocks']=0 
    if 'run01' in filename1:
            cd=df.copy()
            cd['MRI-SEQ'] = cd['MRI-SEQ'].apply(np.int64)
            a=np.where(cd['MRI-SEQ']==5)       
            array=a[0][0]
            cd['blocks'][array:,] ='run01'
            cd.to_csv(f'{os.path.splitext(filename1)[0]}_blocks.csv', index=False)
    elif 'run02' in filename1:
            cd=df.copy()
            cd['MRI-SEQ'] = cd['MRI-SEQ'].apply(np.int64)
            a=np.where(cd['MRI-SEQ']>4)           
            array=a[0][0]
            cd['blocks'][array:,] ='run02'
            cd.to_csv(f'{os.path.splitext(filename1)[0]}_blocks.csv', index=False)  
    elif 'run03' in filename1:
            cd=df.copy()
            cd['MRI-SEQ'] = cd['MRI-SEQ'].apply(np.int64)
            a=np.where(cd['MRI-SEQ']==5)           
            array=a[0][0]
            cd['blocks'][array:,] ='run03'
            cd.to_csv(f'{os.path.splitext(filename1)[0]}_blocks.csv', index=False)
    elif 'run04' in filename1:
            cd=df.copy()
            cd['MRI-SEQ'] = cd['MRI-SEQ'].apply(np.int64)
            a=np.where(cd['MRI-SEQ']==5)           
            array=a[0][0]
            cd['blocks'][array:,] ='run04'
            cd.to_csv(f'{os.path.splitext(filename1)[0]}_blocks.csv', index=False)
    elif 'rest' in filename1:
            cd=df.copy()
            cd['MRI-SEQ'] =cd['MRI-SEQ'].apply(np.int64)
            a=np.where(cd['MRI-SEQ']==5)           
            array=a[0][0]
            cd['blocks'][array:,] ='rest'
            cd.to_csv(f'{os.path.splitext(filename1)[0]}_blocks.csv', index=False)
    elif 'mem' in filename1:
            cd=df.copy()
            cd['MRI-SEQ'] = cd['MRI-SEQ'].apply(np.int64)
            a=np.where(cd['MRI-SEQ']==5)           
            array=a[0][0]
            cd['blocks'][array:,] ='mem'
            cd.to_csv(f'{os.path.splitext(filename1)[0]}_blocks.csv', index=False)

    else:
            print('must be csv')
        
    
# identify the coordinate for all matching values
    
    

#add_blocks_physio('C:/Users/ozarslan/Desktop/python_files/datacopies/Curiosity002OP-mem_processed.csv')




