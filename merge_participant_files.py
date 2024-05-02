from scipy import io
import bioread
import neurokit2 as nk
import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt


df=pd.DataFrame()

path = "C:/Users/ozarslan/Desktop/python_files/datacopies"
os.chdir(path)
for files in os.listdir(path):
    if files.endswith('csv') and 'NS' in files:
            files1=pd.read_csv(files)
            df = pd.concat([df, pd.DataFrame(files1)], ignore_index=False)


df.to_csv('Merged_NS.csv', index=False)