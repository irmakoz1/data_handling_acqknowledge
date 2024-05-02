import seaborn as sns
import pandas as pd
import os
from matplotlib import pyplot as plt


path = "C:/Users/ozarslan/Desktop/python_files/datacopies"
os.chdir(path)
data1=pd.read_csv('Merged_NS.csv')

block1 = data1.query("blocks == 'run01'")
block2 = data1.query("blocks == 'run02'")
block3 = data1.query("blocks == 'run03'")
block4 = data1.query("blocks == 'run04'")

data_ppg= data1.drop('PPG',axis=1)
block1=block1.drop('MRI-SEQ',axis=1)
block2=block2.drop('MRI-SEQ',axis=1)
block3=block3.drop('MRI-SEQ',axis=1)
block3=block3.drop('MRI-SEQ',axis=1)


sns.lineplot(data=block1)
sns.lineplot(data=block2)
sns.lineplot(data=block3)
sns.lineplot(data=block4)

data1['blocks'] = data1['blocks'].astype(str)
data1=data1.drop('MRI-SEQ',axis=1)
#doesnotwork
df_melted = data1.melt("blocks",value_vars='RESP',var_name="Resp&ppg",value_name="Volts")
#sns.relplot(data=data_ppg, y='RESP',hue='blocks', kind='line', height=6, aspect=3, marker='o')


data1.plot(x='blocks')




axes[1].grid('blocks')
axes[1].set_xlabel("blocks")
axes[0].set_ylabel("Volts")
axes[1].set_ylabel("Volts")

#this one works
for key, gp in data1.groupby('blocks'):
    gp.plot( y=['PPG', 'RESP'], title='physio raw NS',subplots=True)
    plt.title(key)






plt.show()