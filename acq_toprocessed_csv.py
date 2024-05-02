from scipy import io
import bioread
import neurokit2 as nk
import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt

path = "C:/Users/ozarslan/Desktop/python_files/datacopies"
os.chdir(path)
for i in os.listdir(path):
    if  i.endswith('acq'):
        data = nk.read_acqknowledge(i, sampling_rate=200)
        df = pd.DataFrame(data[0])
        df = df.rename(columns={'PPG100C': 'PPG', 'TSD160A - Differential Pressure, 2.5 cm': 'RESP', 'Digital (STP Input 7)': 'MRI-SEQ'})
        data_clean, info = nk.bio_process(ppg=df["PPG"], 
                                    rsp=df["RESP"], 
                                    keep=df["MRI-SEQ"],  
                                    sampling_rate=200)
        data_clean.to_csv(f'{os.path.splitext(i)[0]}_processed.csv', index=False)
    elif i.endswith('csv'):
        data = pd.read_csv(i)
        a=data['blocks']
        data_clean, info = nk.bio_process(ppg=data["PPG"], 
                            rsp=data["RESP"], 
                            keep=data["MRI-SEQ"],  
                            sampling_rate=200)
        data_clean['blocks']=a
        data_clean.to_csv(f'{os.path.splitext(i)[0]}_processed.csv', index=False)
        
    
    
    #for further preprocessing options, define your functions my_cleaning and my_processing / change parameters:
    #def my_cleaning(ecg_signal, sampling_rate):
    #detrended = nk.signal_detrend(ecg_signal, order=1)
    #cleaned = nk.signal_filter(detrended, 
    #                           sampling_rate=sampling_rate, 
     #                          lowcut=2, 
     #                          highcut=9, 
      #                         method='butterworth')
        #return cleaned
        
        #def my_processing(ecg_signal):
    #ecg_cleaned = my_cleaning(ecg_signal, sampling_rate=1000)
    #instant_peaks, rpeaks, = nk.ecg_peaks(ecg_cleaned, sampling_rate=1000)
    #rate = nk.ecg_rate(rpeaks, sampling_rate=1000, desired_length=len(ecg_cleaned))
    #quality = nk.ecg_quality(ecg_cleaned, sampling_rate=1000)

    # Prepare output
    #signals = pd.DataFrame({"ECG_Raw": ecg_signal,
     #                       "ECG_Clean": ecg_cleaned,
      #                      "ECG_Rate": rate,
       #                     "ECG_Quality": quality})

    #signals = pd.concat([signals, instant_peaks], axis=1)

    # Create info dict
    #info = rpeaks
    #info["sampling_rate"] = 1000
    
    #return signals, info
    