import os, csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

sns.set_style("ticks")
sns.set_context("poster")
#sns.despine(trim=True)

df = pd.read_csv("collect_data.csv")
data=df.loc[(df["slot_duration"]!=120) & (df["simultaneous_fixation"]==False) & (df["genetics_bool"] == True) & (df["clutch_m"] == 10)]
#data2 = data.loc[data["pvalue"] < 0.05]

data_adjust = df.loc[(df["smallest_n"]>30) & (df["n_embryos"]>200)]

#print "15 min AND YES genetics:", len(data)
#print "Of those, pval <0.05:", len(data2)
#print "Percentage:", len(data2)/float(len(data))*100

colors = np.where(data.smallest_n > 10, 'r', 'g')
plt.scatter(data.n_embryos, data.pvalue, c=colors)
plt.show()

#plt.figure()
#df['pvalue'].hist()
#plt.show()
#plt.figure()


discrete_cats = ["genetics_bool","slot_duration","simultaneous_fixation","clutch_m","clutch_sd","noise_sd"]
output_cats = ["chisquare","pvalue","n_embryos","smallest_n","total_clutches"]

labels = {"genetics_bool":"Clutch genetics","slot_duration":"Fixation frequency","simultaneous_fixation":"Simultaneous fixation","clutch_m":"Mean clutch size","clutch_sd":"Clutch size standard deviation","noise_sd":"Noise standard deviation","chisquare":"Chi square","pvalue":"p-value","n_embryos":"total numer of embryos","smallest_n":"n embryos per age category","total_clutches":"total number of clutches"}

orders = {"genetics_bool":[True,False],"slot_duration":[15,30,60,120],"simultaneous_fixation":[True,False],"clutch_m":[4,10,20],"clutch_sd":[1,6,15],"noise_sd":[5,20]}


def makeplot(title,filename,xlabel,xdata,xorder,ylabel,ydata,catlabel,catdata):
	ax = sns.violinplot(x=xdata, y=ydata, hue=catdata, data=data_adjust, palette="Set1", scale="count",inner="quartile", order=xorder, bw=.1)
	ax.set_title("")
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	plt.savefig("/home/barbara/Dropbox/oncopeltus/susan-lisa/adjusteddata-%s.png" %filename)
	plt.clf()
	plt.close()


##Discrete categories in the dataset
#"genetics_bool"
#"slot_duration"
#"simultaneous_fixation"
#"clutch_m"
#"clutch_sd"
#"noise_sd"

## Output/continuous categories in the dataset
#"chisquare"
#"pvalue"
#"n_embryos"
#"smallest_n"
#"total_clutches"

for cc in output_cats:
	for dc1 in discrete_cats:
		for dc2 in discrete_cats:
			if dc1 == dc2:
				continue
			## Fill up the plot
			title = "%s by %s per %s" %(labels[cc],labels[dc1],labels[dc2])
			filename = "%s-%s-%s" %(cc,dc1,dc2)
	
			## X axis ##
			xlabel = labels[dc1]
			xdata =  dc1
			xorder = orders[dc1]

			## Y axis ##
			ylabel = labels[cc] 
			ydata = cc

			## Categories ##
			catlabel = labels[dc2]
			catdata = dc2

			#makeplot(title,filename,xlabel,xdata,xorder,ylabel,ydata,catlabel,catdata)



