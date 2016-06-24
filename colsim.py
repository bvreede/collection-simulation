from random import randint # used to generate random integer in specified interval
from random import random # used to generate a random number between 0 and 1
from random import choice #to choose a random item from a list
import numpy as np
import pandas as pd
from collections import Counter
from scipy.stats import chisquare
from scipy.stats import pearsonr
import os,sys

## Simulation description and definition of time parameters:
# The simulation starts with 12 hours of egg laying:
start_el = 0 #start time of egg lay in hours
start_el = start_el*60 #start time of egg lay in minutes
end_el = 12 #end time of egg lay in hours
end_el = end_el*60 #end time of egg lay in minutes

# Clutches are collected every 2 hours, and on average 4 clutches are laid per hour:
slot_duration = choice([15,30,60,120]) #120 #duration of time slots for fixation in minutes
clutchesPerHour= 6 # typical number of clutches laid in an hour

# Abdominal segmentation starts at 40HAEL (hours after egg lay), and a new segment is formed every 1.5 hours
start_abdominal = 42 #start time of abdominal segmentation in hours
start_abdominal = start_abdominal * 60 #start time of abdominal segmentation in minutes
global T_segmentation; T_segmentation=90 # the period of segmentation, in minutes

# All embryos are fixed at the end of the simulation, at 56 hours
end_sim = 56 #end time of simulation in hours; oldest embryos in the sample
end_sim = end_sim * 60  #end time of simulation in minutes

# This means the youngest embryos in the sample are 44 hours old
start_sim = end_sim - end_el #youngest embryos in the sample (! in minutes!)

# The simulation runs on iterations of 2 minutes
timestep = 2 #duration of simulation time steps in minutes
duration = int((end_sim - start_sim)/timestep) #length of simulation in time steps

# State whether fixation is done simultaneously, or if the clutch will be fixed at different timepoints
fixsim=choice([True, False])

##generate a list of random clutch sizes, normally distributed but larger than 0
clutch_m = 10 #mean of normal distribution clutch sizes
clutch_sd = 6 #standard dev of normal distribution clutch sizes
ranClutchSize = [int(t) for t in np.random.normal(clutch_m,clutch_sd,500) if t>0]

##generate a list of noise parameters for new clutches
noise_sd = 20 #standard deviation for noise in time units, which is 2 minutes.
noise = [int(n) for n in np.random.normal(0,noise_sd,500)]

##generate a list of genetic 'noise' parameters, which will be specific per clutch
genetics_bool = choice([True,False])
if genetics_bool == True:
	genetic_sd = choice([5,10]) #standard deviation from segmentation rate, in minutes
	genetics = [int(n) for n in np.random.normal(0,genetic_sd,100)]
else:
	genetics = [0]
	genetic_sd = 0


## parameters defining the sample
# The sample list is a list of collected embryos.
# Each embryo is represented by the embryo's ID, age (time slot), segment number at fix
global sampleList; sampleList=[]
global embryoID; embryoID = 1
total_clutches = 0 #counts the total number of clutches generated in the simulation

## fixation categories
nCats = end_el/slot_duration #total number of categories
fixCats = [(start_sim+n*slot_duration)/60. for n in range(nCats)] #all possible age categories at fixation

def slot(time):
	'''
	define the time slot for an embryo,
	given its age in minutes (NOT INCLUDING NOISE!)
	'''
	slot_start = float(int((end_sim - time)/slot_duration)*(slot_duration/60.))
	return slot_start
	
def slotoptions(time,clutchSize):
	'''
	return a list of slots for fixation, and the related fixation times (that will function as 'end_sim' equivalents)
	only required when fixation is not simultaneous.
	'''
	slots,fixation_times = [],[]
	for n in range(clutchSize):
		chosen_slot = choice(fixCats) #choose fixation slot randomly
		current_slot = int(time/slot_duration)*(slot_duration/60.)
		# calculate what time fixation needs to occur for the embryo to have the required age at fixation:
		fixtime = (chosen_slot+current_slot)*60 + slot_duration 
		# add slot and required fixtime to lists
		slots.append(chosen_slot)
		fixation_times.append(fixtime)
	return slots,fixation_times

def segments_from_age(age,sr):
	'''
	returns segment number, calculated from the age.
	note, this is the age INCLUDING noise, not the age bracket of the embryo!
	the segmentation rate that is used is the genetically determined one.
	'''
	#calculate number of abdominal segments
	abd_segments = int((age - start_abdominal)/sr)
	if abd_segments > 9:
		abd_segments = 9
	if abd_segments < 0:
		abd_segments = 0
	return abd_segments

def lay_clutch(time):
	'''
	generates a clutch of embryos, and defines their eventual segment number
	'''
	global embryoID
	global sampleList
	clutchSize = choice(ranClutchSize) # choose a clutch size from the list
	#print clutchSize, "embryos in the making..."
	if fixsim == True:
		#timeslot for all embryos in this clutch
		timeslot = slot(time)
	else:
		timeslots,fixtimes = slotoptions(time,clutchSize)
	clutch_sr = T_segmentation + choice(genetics) #this clutch has a genetic faster/slower segmentation rate
	for i in range(clutchSize):
		#provide ID
		thisID = embryoID
		embryoID += 1
		#define age +/- noise for each embryo
		ageNoise = choice(noise)
		age = 0 + ageNoise
		#add time until fixation
		if fixsim == True:
			fixation = end_sim
		else:
			fixation = fixtimes.pop()
		age_at_end = age + (fixation - time)
		#calculate how many segments the embryo will have
		segments = segments_from_age(age_at_end,clutch_sr)
		#determine the timeslot in case the clutch is not fixed simultaneously
		if fixsim == False:
			timeslot = timeslots.pop()
		#save embryo ID + age to the list
		sampleList.append([thisID,timeslot,segments])
    
	 
def calculate_clutch_probability(clutchesPerHour,timestep):
	'''
	calculate_clutch_probability calculates a rough probability
	of clutching in a given interval based on typical clutches per hour
	'''
	p_clutch=float(clutchesPerHour)*timestep/60
	return p_clutch
	
## Calculate rough probability of clutching per timestep
p_clutch=calculate_clutch_probability(clutchesPerHour,timestep)

#run the simulation by iterating through time steps
for i in range(duration):
	#generate a clutch with probability p
	if p_clutch>random(): # decides whether a clutch will be laid based on rough probability
		time_i = i*timestep #convert timestep back to minutes
		lay_clutch(time_i)
		total_clutches += 1
		#print 'clutch laid at time', i, "(%s hours)" %(str(i*timestep/60))

print 'Total number of embryos:', len(sampleList)
print 'Total number of clutches:', total_clutches
print "Simultaneous fixation:", fixsim
print "Genetics:", genetics_bool, genetic_sd
print "Sampling frequency: every", slot_duration, "minutes"

#process the data
df = pd.DataFrame(sampleList, columns=["embryoID","age","stage"])
corr = pearsonr(df["age"],df["stage"])
corr_pval = str(corr[1])
corr_rsquared = str(corr[0]*corr[0])
corr_pearson = str(corr[0])

unsampled_data = {} #dictionary with age:[stages], before sampling
min_sample = len(sampleList) #the smallest number of embryos per age category

#iterate through the dataframe to collect all stages per age category
#append stages to a list in the "unsampled_data" dictionary
for cat in fixCats:
	unsampled_data[cat] = []
	#iterate through the dataframe
	for index,row in df.iterrows():
		if row["age"] == cat:
			unsampled_data[cat].append(row["stage"])
	# check if this category has the smallest sample of embryos; if so, put the value in "min_sample"
	if len(unsampled_data[cat]) < min_sample:
		min_sample = len(unsampled_data[cat])

print 'Smallest number of embryos in age group:', min_sample
if min_sample < 2:
	sys.exit("Not enough embryos to work with. Experiment not saved.")


sampled_data = [] #data with only stages
for cat in fixCats:
	embryos = unsampled_data[cat]
	for i in range(min_sample):
		#pick an embryo from the list
		n = randint(0,len(embryos)-1)
		#remove it and add it to the sampled data
		embryo_i = embryos.pop(n)
		sampled_data.append(embryo_i)

#count the number of embryos in each stage
stagecounts = Counter(sampled_data)

print "Data sampled to be uniform in time:"
for i in range(1,10):
	print stagecounts[i], "embryos in stage", i


print "Testing whether this deviates from a linear segmentation process:"
#start analysing the data to determine if it deviates significantly from a linear segmentation process
forchisquare = [] #list of embryo counts to be used for chisquare test
for i in range(2,9):
	forchisquare.append(stagecounts[i])
chisqtest = chisquare(forchisquare)
if chisqtest[1] < 0.05:
	print "YES (p value %s), with pearson's R = %s (pvalue %s)" %(str(chisqtest[1]), corr_pearson, corr_pval)
else:
	print "NO (p value %s), with pearson's R = %s (pvalue %s)" %(str(chisqtest[1]), corr_pearson, corr_pval)
	

#print data to output file. If the outputfile already exists, just add data to it.
curdir = os.getcwd() 
outfile = "%s/collect_data.csv" %curdir
if os.path.exists(outfile):
	out = open(outfile, "a")
else: #the outputfile does not yet exist. Create it and write headers
	out = open(outfile, "w")
	out.write("genetics_bool,genetic_sd,slot_duration,start_abdominal,timestep,simultaneous_fixation,clutch_m,clutch_sd,noise_sd,n_embryos,smallest_n,total_clutches,chisquare,chi_pvalue,pearsonsR,Rsquared,pear_pvalue\n")
	
#revert start_abdominal back to hours to write it to the outputfile
start_abdominal = start_abdominal/60


#write data and varying parameters to the outputfile
out.write("%s,%s,%s,%s,%s,%s," %(str(genetics_bool),str(genetic_sd),str(slot_duration),str(start_abdominal),str(timestep),str(fixsim)))
out.write("%s,%s,%s," %(str(clutch_m),str(clutch_sd),str(noise_sd)))
out.write("%s,%s,%s,%s,%s,%s,%s,%s\n" %(str(len(sampleList)),str(min_sample),str(total_clutches),str(chisqtest[0]),str(chisqtest[1]),corr_pearson,corr_rsquared,corr_pval))
out.close()


#something is still wrong with the simultaneous fixations and categories: 90 minutes and True fixsim does not combine, because the categories
#created that way are not in the fixCats list!