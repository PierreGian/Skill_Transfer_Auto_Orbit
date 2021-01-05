#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import pylab
import statsmodels as sm
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf
from scipy.signal import argrelextrema
from glob import glob

import sys
Argums = sys.argv
########################################
#Variable to update before starting running the script
Type = Argums[1] #'FFF', 'MMM'
########################################

#Special search file to get all the model names
from glob import glob
GameNb=15
#Specify Evt file here!
ToWrite_path = Type
Evt_file = Type+'_Preproc'
Final_Folder = 'Outputs'
######################

my_game_search = './'+Evt_file+'/*_1.evts'
paths = glob(my_game_search)
NbPaths = len(paths)
#print(paths)
Listnames = [paths[i].split('/')[-1].split('.')[0].split('-')[0] for i in range(NbPaths)]
name_comps = [nn.split('_') for nn in Listnames]
Listnames = []
for nn in name_comps:
    Str_ToAppend = nn[0]+'_'+nn[1]+'_'+nn[2]
    Listnames.append(Str_ToAppend)
SubjNb = len(Listnames)
#print(SubjNb)
ints = [int(Listnames[i].split('_')[-1]) for i in range(SubjNb)]
#Sorting by integer
orderInts = np.argsort(np.array(ints))
names = [Listnames[nn] for nn in orderInts]
#print(names)
#names contains all the names of all the model subjects


#Now deal with autocorrelation measures
Lefts = [[[] for gg in range(GameNb)] for i in range(SubjNb)]
Rights = [[[] for gg in range(GameNb)] for i in range(SubjNb)]
Fires = [[[] for gg in range(GameNb)] for i in range(SubjNb)]


#Looping through all the subjects
numlags = 125
for subj,name in enumerate(names):
    for el,gg in enumerate(range(GameNb)):
        path_cyc = './Discrete_Game_Cycles/'+Type+'/NoRotations/'+name
        my_game_search2 = path_cyc+'_Game'+str(gg+1)+'_NoRot*.dists'
        cur_paths = glob(my_game_search2)
        Listfiles = [cur_paths[i].split('/')[-1] for i in range(len(cur_paths))]
        #print(Listfiles)
        if(not(not Listfiles)): #if the returned list is not empty
            list_len = len(Listfiles)
            for cc in np.arange(1,list_len+1): #for each game cycle, append a vector
                SeqFile = path_cyc+"_Game"+str(gg+1)+'_NoRot'+str(cc)+'.dists'
                f_toOpen = open(SeqFile,"r") 
                lines = [line.rstrip().split(",") for line in f_toOpen]
                cur_Lefts = [int(ee) for ee in lines[0]]
                cur_Rights = [int(ee) for ee in lines[1]]
                cur_Fires = [int(ee) for ee in lines[2]]
                Lefts[subj][el].append(cur_Lefts)
                Rights[subj][el].append(cur_Rights)
                if(len(cur_Fires)>=numlags):
                    Fires[subj][el].append(cur_Fires)


#Computation of the ACF measures
All_ACFs = [[[] for gg in range(GameNb)] for i in range(SubjNb)] #Initialize autocorrelation function
numlags = 125
len_lag = numlags+1
ACF_avg = [[np.zeros(numlags) for gg in range(GameNb)] for i in range(SubjNb)]
all_pers = np.zeros((SubjNb,GameNb)) #Periodicities
all_amps = np.zeros((SubjNb,GameNb)) #Amplitudes
for subj in range(SubjNb):
    for nn in range(GameNb):
        cur_Fires = Fires[subj][nn]
        if(cur_Fires==[]):
            all_pers[subj][nn] = 0.0
            all_amps[subj][nn] = 0.0
            continue
        n_cyc = len(cur_Fires)
        Per_list = []
        Amp_list = []
        for cc in range(n_cyc):
            cur_IPIs = cur_Fires[cc]
            data_fr = pd.DataFrame(
                {
                    "event":np.arange(1,len(cur_IPIs)+1),
                    "IPIs":cur_IPIs,
                }
            )
            if(cur_IPIs==[]):
                continue
            series = data_fr['IPIs']
            lag_acf = acf(series, nlags=numlags)
            All_ACFs[subj][nn].append(lag_acf)
        ACF_avg[subj][nn]=np.mean(np.array(All_ACFs[subj][nn]),axis=0)
        per = 0
        amp = 0
        if(len(lag_acf)==len_lag):
            vec = ACF_avg[subj][nn]
            max_all = argrelextrema(vec, np.greater)[0]
            amp_max = np.array([vec[ee] for ee in max_all])
            for iii,mm in enumerate(amp_max):
                if(mm>0.01):
                    amp=mm
                    per=max_all[iii]*16
                    break
        all_pers[subj][nn] = per
        all_amps[subj][nn] = amp


#Now printing the Excel version of the table to help plot results
#1) Periodicity
SeqFile = './'+Final_Folder+'/'+'Periodicity_'+Type+'_Transfer.txt'
ff_toWrite = open(SeqFile,"w+")
ToWrite = "ModelNb\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
ff_toWrite.write(ToWrite)
for subj in range(SubjNb):
    ToWrite = names[subj]
    for nn in range(GameNb):
        cGame = str(nn+1)
        Per = str(all_pers[subj][nn])
        ToWrite=ToWrite+'\t'+Per
    ToWrite=ToWrite+"\n"
    ff_toWrite.write(ToWrite)
ff_toWrite.close()
#2) Amplitude
SeqFile = './'+Final_Folder+'/'+'Amplitude_'+Type+'_Transfer.txt'
ff_toWrite = open(SeqFile,"w+")
ToWrite = "Subject\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
ff_toWrite.write(ToWrite)
for subj in range(SubjNb):
    ToWrite = names[subj]
    for nn in range(GameNb):
        cGame = str(nn+1)
        Per = str(all_amps[subj][nn])
        ToWrite=ToWrite+'\t'+Per
    ToWrite=ToWrite+"\n"
    ff_toWrite.write(ToWrite)
ff_toWrite.close()


