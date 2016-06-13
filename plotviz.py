import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


df = pd.read_csv("collect_data.csv")

colors = np.where(df.simultaneous_fixation == True, 'r', 'g')
plt.scatter(df.slot_duration, df.pvalue, c=colors)
plt.show()

#plt.figure()
#df['pvalue'].hist()
#plt.show()