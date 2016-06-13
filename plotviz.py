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

def makeplot(title,filename,xlabel,xdata,ylabel,ydata,catlabel,catdata):
	ax = sns.violinplot(x=xdata, y=ydata, hue=catdata, data=df, palette="Set1", scale="count",inner="quartile", bw=.1)
	ax.set_title("")
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	plt.savefig("/home/barbara/Dropbox/oncopeltus/susan-lisa/%s.png" %filename)
	plt.close()

## Fill up the plot
title = ""
filename = ""

## X axis ##
xlabel = "Fixation frequency (in minutes)"
xdata =  "slot_duration"

## Y axis ##
ylabel = "p-value" 
ydata = "pvalue" #pvalue

## Categories ##
catlabel = ""
catdata = "simultaneous_fixation"

makeplot()
