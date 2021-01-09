#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import pylab
import scipy.fftpack
import statsmodels as sm
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf
from scipy.signal import argrelextrema
import os

from glob import glob
GameNb=15
N = 80
Data_file = 'Data'
Preproc_file = 'Preproc'
Output_file = 'Outputs'
Name_Output = 'ALL_Humans_avg'
######################

Allnames=[j for j in range(N)]
Allconds=[('','') for j in range(N)]
SeqFile = '../Scripts/Transfer_Scores_Humans.txt'
f_toOpen = open(SeqFile,"r") 
lines = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines[0]
idx=0
for ii in np.arange(1,len(lines)):
    cur_line=lines[ii]
    Allnames[idx] = cur_line[0]
    Allconds[idx] = (cur_line[1],cur_line[2])
    idx=idx+1

from glob import glob
GameNb=15
Data_file = "Data"
Preproc_file = "Preproc"

my_game_search = '../Preproc/*_1.evts'
paths = glob(my_game_search)
NbPaths = len(paths)
names = [paths[i].split('/')[-1].split('.')[0].split('_')[0] for i in range(NbPaths)]
SubjNb = len(names)
conds=[('','') for j in range(SubjNb)]
for i,nn in enumerate(names):
    for j,aa in enumerate(Allnames):
        if(nn==aa):
            conds[i]=Allconds[j]

#Now deal with autocorrelation measures
Lefts = [[[] for gg in range(GameNb)] for i in range(SubjNb)]
Rights = [[[] for gg in range(GameNb)] for i in range(SubjNb)]
Fires = [[[] for gg in range(GameNb)] for i in range(SubjNb)]


#Looping through all the subjects
numlags = 125 #number of lags 125*16 = 2000 ms
for subj,name in enumerate(names):
    for el,gg in enumerate(range(GameNb)):
        #1) Get the right condition corresponding to the game number
        cur_cond = ''
        if(gg>=5 and gg<10):
            cur_cond = conds[subj][1]
        else:
            cur_cond = conds[subj][0]
        #2) Get the right name corresponding to the no rotations game cycles
        path_cyc = '../Discrete_Game_Cycles/NoRotations/'
        cur_name = names[subj]+"_"+cur_cond+'_Game'+str(gg+1)+'_NoRot*.dists'
        my_game_search2 = path_cyc+cur_name
        cur_paths = glob(my_game_search2)
        Listfiles = [cur_paths[i].split('/')[-1] for i in range(len(cur_paths))]
        if(not(not Listfiles)): #if the returned list is not empty
            list_len = len(Listfiles)
            for cc in np.arange(1,list_len+1): #for each game cycle, append a vector
                SeqFile = path_cyc+names[subj]+'_'+cur_cond+'_Game'+str(gg+1)+'_NoRot'+str(cc)+'.dists'
                if(not (os.stat(SeqFile).st_size == 0)): #Make sure file is not empty
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
        ACF_avg[subj][nn]=np.mean(np.array(All_ACFs[subj][nn]),axis=0) #average across game cycles within games
        per = 0
        amp = 0
        if(len(lag_acf)==len_lag):
            vec = ACF_avg[subj][nn]
            max_all = argrelextrema(vec, np.greater)[0]
            amp_max = np.array([vec[ee] for ee in max_all]) #Extract amplitudes of maximums
            for iii,mm in enumerate(amp_max):
                if(mm>0.02): #Threshold needs to be 0.02!! Extract first peak - amplitude & periodicity
                    amp=mm
                    per=max_all[iii]*16
                    break
        all_pers[subj][nn] = per
        all_amps[subj][nn] = amp

#Now printing the Excel version of the table to help plot results
#1) Periodicity
path = '../'+Output_file+'/'
SeqFile = path+'Periodicity_thresh_'+Name_Output+'_Transfer.txt'
ff_toWrite = open(SeqFile,"w+")
ToWrite = "Subject\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
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
SeqFile = path+'Amplitude_thresh_'+Name_Output+'_Transfer.txt'
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



