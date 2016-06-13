import os, csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

sns.set_style("ticks")
sns.set_context("poster")
#sns.despine(trim=True)

df = pd.read_csv("dataset_random.csv")

#colors = np.where(df.simultaneous_fixation == True, 'r', 'g')
#plt.scatter(df.slot_duration, df.pvalue, c=colors)
#plt.show()

#plt.figure()
#df['pvalue'].hist()
#plt.show()
#plt.figure()


ax = sns.violinplot(x="slot_duration", y="pvalue", hue="simultaneous_fixation", data=df, palette="Set1", order=[15,30,60,120], scale="count",inner="quartile", bw=.1)
ax.set_title('Random parameters')

ax.set_xlabel('fixation slots (minutes)')
ax.set_ylabel('p-value')
plt.show()
