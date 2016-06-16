import pandas as pd


discrete_cats = ["genetics_bool","slot_duration","simultaneous_fixation","clutch_m","clutch_sd","noise_sd"]
output_cats = ["chisquare","pvalue","n_embryos","smallest_n","total_clutches"]

labels = {"genetics_bool":"Clutch genetics","slot_duration":"Fixation frequency","simultaneous_fixation":"Simultaneous fixation","clutch_m":"Mean clutch size","clutch_sd":"Clutch size standard deviation","noise_sd":"Noise standard deviation","chisquare":"Chi square","pvalue":"p-value","n_embryos":"total number of embryos","smallest_n":"n embryos per age category","total_clutches":"total number of clutches"}

options = {"genetics_bool":[True,False],"slot_duration":[15,30,60,120],"simultaneous_fixation":[True,False],"clutch_m":[4,10,20],"clutch_sd":[1,6,15],"noise_sd":[5,20]}

ranges = {"n_embryos":[[0,300],[300,800],[800,""]], "smallest_n":[[0,10],[10,30],[30,60],[60,""]], "total_clutches":[[0,35],[35,50],[50,""]]}

#open input database: the results of multiple experiments
df = pd.read_csv("collect_data.csv")

#open output file
out = open("/home/barbara/Dropbox/testscenarios.csv","w")
#write the output headers
out.write("genetics_bool,slot_duration,simultaneous_fixation,clutch_m,clutch_sd,noise_sd,n_embryos,smallest_n,total_clutches,total_experiments,total_p<0.05,percentage_p<0.05,mean_pvalue\n")

#counter to check that all experiments are included
dfcheck1 = len(df)
global dfcheck2; dfcheck2 = 0

def process_range(dfin,item,rangeoption):
	'''
	returning a new dataframe from [dfin] where the values of [item] are within the 
	range indicated in [rangeoption].
	'''
	dfout_a = dfin.loc[dfin[item]>=rangeoption[0]]
	if rangeoption[1] == "":
		return dfout_a
	else:
		dfout_b = dfout_a.loc[dfin[item]<rangeoption[1]]
		return dfout_b


def data2csv(df_final,o_a,o_b,o_c,o_d,o_e,o_f,o_g,o_h,o_i):
	'''
	analyse the resulting database, and write the selection criteria
	as well as the data (percentage of pvalues below 0.05) to the output file
	'''
	global dfcheck2
	#print "Printing to file."
	for o_x in [o_a,o_b,o_c,o_d,o_e,o_f]:
		out.write("%s," %(str(o_x)))
	for o_y in [o_g,o_h,o_i]:
		out.write("%s-%s," %(str(o_y[0]),str(o_y[1])))
	experiments = len(df_final)
	df_p = df_final.loc[df_final["pvalue"]<0.05]
	p5 = len(df_p)
	try:
		fraction = str(round(float(p5)/experiments*100,2))
	except ZeroDivisionError:
		fraction = "--"
	meanp = str(df_final["pvalue"].mean())
	out.write("%s,%s,%s,%s\n" %(str(experiments),str(p5),fraction,meanp))
	dfcheck2 += experiments
	

#iterate through all options to generate a unique combination of parameter values
#at each step, reduce the database to only use this particular parameter value combination.
#the old database is deleted from memory.

print "Starting database;",len(df),"values."
for o_a in options["genetics_bool"]:
	df_a = df.loc[df["genetics_bool"]==o_a]
	#print "First step: genetics;",len(df_a),"values."
	for o_b in options["slot_duration"]:
		df_b = df_a.loc[df_a["slot_duration"]==o_b]
		#print "Second step: slots;",len(df_b),"values."
		for o_c in options["simultaneous_fixation"]:
			df_c = df_b.loc[df_b["simultaneous_fixation"]==o_c]
			#print "Third step: fixation;",len(df_c),"values."
			for o_d in options["clutch_m"]:
				df_d = df_c.loc[df_c["clutch_m"]==o_d]
				#print "Fourth step: clutch size;",len(df_d),"values."
				for o_e in options["clutch_sd"]:
					df_e = df_d.loc[df_d["clutch_sd"]==o_e]
					#print "Fifth step: clutch sd;",len(df_e),"values."
					if len(df_e) == 0:
						continue
					for o_f in options["noise_sd"]:
						df_f = df_e.loc[df_e["noise_sd"]==o_f]
						#print "Sixth step: noise;",len(df_f),"values."
						for o_g in ranges["n_embryos"]:
							df_g=process_range(df_f,"n_embryos",o_g)
							#print "Seventh step: n embryos;",len(df_g),"values."
							for o_h in ranges["smallest_n"]:
								df_h=process_range(df_g,"smallest_n",o_h)
								#print "Eigth step: smallest group;",len(df_h),"values."
								for o_i in ranges["total_clutches"]:
									df_i=process_range(df_h,"total_clutches",o_i)
									#print "Ninth step: total clutches;",len(df_h),"values."
									if len(df_i) == 0:
										continue
									data2csv(df_i,o_a,o_b,o_c,o_d,o_e,o_f,o_g,o_h,o_i)

print dfcheck1,dfcheck2

