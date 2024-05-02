
from scipy import io
import bioread
import neurokit2 as nk
import pandas as pd

import numpy as np
from matplotlib import pyplot as plt

dir(bioread)

#BIOREAD READ AND PLOT
data = bioread.read_file('Pilot-001.acq')
data
#data.channels



#plt.subplot(211)
#seq = data.channels[2]
#resp = data.channels[0]
#pr = data.channels[1]
#resp.tit= 'Respiration'
#pr.tit='Pulse'
#seq.tit='Sequence'


#plt.plot(seq.time_index, seq.data +2, label='{}, {} ({})'.format(seq.name, seq.units,seq.tit))
#plt.plot(resp.time_index, resp.data, label='{} ,{} ({})'.format(resp.name, resp.units,resp.tit))
#plt.plot(pr.time_index, pr.data , label='{} , {} ({})'.format(pr.name, pr.units,pr.tit))

#plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
#           ncol=1, mode="expand", borderaxespad=0.)
#plt.show()

#plotting the ackqnowledge data. (added the names respiration -pulse)


#print(data)
#pd.DataFrame(data.channels[seq])
#pd.DataFrame.info(data.channels)
#HERE I CONVERT FILE TO CSV
data_neuro =nk.read_acqknowledge('C:/Users/ozarslan/Desktop/python_files/datacopies/Curiosity003NS-mem.acq', sampling_rate=200)
#print(data_neuro)
#type(data_neuro)
nk.signal_plot(data_neuro, sampling_rate=200) # Visualize

#data_neuro[0]
df = pd.DataFrame(data_neuro[0])

#print(df)
#df.to_csv('physio_data_01.csv', index=False)  #now to save the data to a csv file for further analysis.

df.head()
#RENAME THE COLUMNS IN A MORE CLEAR WAY
df = df.rename(columns={'PPG100C': 'PPG', 'TSD160A - Differential Pressure, 2.5 cm': 'RESP', 'Digital (STP Input 7)': 'MRI-SEQ'})
df.head()
#categorize the channels in neurokit
data_clean, info = nk.bio_process(ppg=df["PPG"], 
                                  rsp=df["RESP"], 
                                  keep=df["MRI-SEQ"],  
                                  sampling_rate=200)

data_clean.head()
type(data_clean)
data_clean[["PPG_Rate", "RSP_Rate", "MRI-SEQ"]].plot(subplots=True)
plt.show()

# Find peaks adn HRV indices
peaks, info = nk.ppg_peaks(df["PPG"], sampling_rate=200, correct_artifacts=True)
hrv_indices = nk.hrv(peaks, sampling_rate=200, show=True)
hrv_indices.head()

signals, info = nk.bio_process(df, sampling_rate=200)
hrv_processed=nk.hrv(signals, sampling_rate=200)


#need to extract the block of sequences in separate files! (mri-seq ) but the data is not block of 5 its mixed with 0's.

#1-add row number and column for blocks

df['row_number'] = df.index if df.index.is_monotonic_increasing else range(len(df))
df

#2- find the shift from 0 to 5 and return row number in a new data frame. 
#3-find where there are repeated 0's for length (enough) then get the row numbers- or just the start row number of the repeated 0's.
#4- using these two operations to mark the beginning and end of the blocks. (beginning shift to start 0) and fill the blocks column
#5- extract block as separate data-frames.
#6-do the preprocessing?

#Here I make the differences column (-5,0,5)
type(df)
df['differences'] = 0
df['differences'] =df['MRI-SEQ'].diff()
df["differences"] = pd.to_numeric(df["differences"], downcast='integer')
counts = df['differences'].value_counts()
counts
df['differences'] = round(df['differences'].replace(np.nan, 0))
df['differences'] = df['differences'].astype(int)
#df.to_csv('df.csv', index=False)
a=np.where(df['MRI-SEQ']==5)
array=a[0][0]
a=list(a)
a[0]
del a[1]
df.loc[:, ['differences']]

#Here it is for storing 5's and -5's

a=[]
for values,row in df.loc[:, ['differences']].iterrows():
    if row['differences']> 0:
        
       a.append(row)
       
b=[]      
for values,row in df.loc[:, ['differences']].iterrows():
    if row['differences']< 0:
        
       b.append(row)
   
a.head()
    
df_diff = pd.concat([pd.DataFrame(a), pd.DataFrame(b)]) #one dataframe


#calculate where the repeated 0's start.
        
#KK = df['differences'].eq(5)
#KK
      
    
thresh = 280 #state the threshold of repetition

m = df['differences'].eq(0) #state the number you want to search
group = (~m).cumsum()

g = df[m].reset_index().groupby(group)
g.size()
rows_change= g['index'].first()[g.size()>thresh].to_numpy()#find the first row of the repeated number
np.set_printoptions(threshold=sys.maxsize)
rows_change

#column blocks:
a=df.where(df['MRI-SEQ']==5).first()
a=
df['blocks']=0

#adjust the blocks according to the array.
#ROW-CHANGES TO REPEATED 0'S (END OF THE BLOCKS): array([      0,  402272,  563961,  601507,  758225,  905596, 1050774]
#find the start using array a. first change after this rownumber. check differences.
#block1 = 323588-402272, block2: 456516-563961, block3: 650815-758225,block4: 797431-905596, block5:942420-1050774
#divide the data into blocks
block1= df[456516:563961].copy()
block1['blocks']=1
#block1 = block1.iloc[: , :-1] #drop last column
block2= df[650815:758225].copy()
block2['blocks']=2
block3= df[797431:905596].copy()
block3['blocks']=3
block4= df[942429:1050774].copy()
block4['blocks']=4


#merged dataframe with blocks:

frames = [block1, block2, block3,block4]

merged_blocks = pd.concat(frames)
#to drop a colmumn by name
merged_blocks = merged_blocks.drop('differences', axis=1)
#write data
merged_blocks.to_csv('merged_blocks.csv', index=False)