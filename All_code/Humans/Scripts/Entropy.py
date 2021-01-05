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

#Special search file to get all the human names
from glob import glob
GameNb=15
N = 180
Data_file = 'Data'
Preproc_file = 'Preproc'
Output_file = 'Outputs'
Name_Output = 'ALL_Humans'
######################

Allnames=[j for j in range(N)]
Allconds=[('','') for j in range(N)]
SeqFile = '../Scripts/Summary_Scores_ALL.txt'
f_toOpen = open(SeqFile,"r") 
lines = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines[0]
idx=0
for ii in np.arange(1,len(lines)):
    cur_line=lines[ii]
    Allnames[idx] = cur_line[0]
    Allconds[idx] = (cur_line[1],cur_line[2])
    idx=idx+1

#Special search file to get all the human names and the conditions they were assigned to
from glob import glob
GameNb=15
Data_file = "Data"
Preproc_file = "Preproc"

my_game_search = '../'+Preproc_file+'/*_1.evts'
paths = glob(my_game_search)
NbPaths = len(paths)
names = [paths[i].split('/')[-1].split('.')[0].split('_')[0] for i in range(NbPaths)]
SubjNb = len(names)
conds=[('','') for j in range(SubjNb)]
for i,nn in enumerate(names):
    for j,aa in enumerate(Allnames):
        if(nn==aa):
            conds[i]=Allconds[j]

from glob import glob
Letters = [[[] for gg in range(GameNb)] for i in range(SubjNb)]
IPI = [[[] for gg in range(GameNb)] for i in range(SubjNb)]


for subj,name in enumerate(names):
    path_cyc = '../Game_Cycles/NoRotations/'
    for gg in range(GameNb):
        #1) Get the right condition corresponding to the game number
        cur_cond = ''
        if(gg>=5 and gg<10):
            cur_cond = conds[subj][1]
        else:
            cur_cond = conds[subj][0]
        #2) Get the right name corresponding to the no rotations game cycles
        cur_name = names[subj]+"_"+cur_cond+'_Game'+str(gg+1)+'_NoRot*.txt'
        my_game_search2 = path_cyc+cur_name
        cur_paths = glob(my_game_search2)
        Listfiles = [cur_paths[i].split('/')[-1] for i in range(len(cur_paths))]
        if(not(not Listfiles)): #if the returned list is not empty
            list_len = len(Listfiles)
            cur_arrLets = []
            cur_arrIPIs = []
            cur_arrgames = -1
            for cc in np.arange(1,list_len+1):
                SeqFile = path_cyc+names[subj]+'_'+cur_cond+'_Game'+str(gg+1)+'_NoRot'+str(cc)+'.txt'
                f_toOpen = open(SeqFile,"r") 
                lines = [line.rstrip().split("\t") for line in f_toOpen]
                cur_Letters = []
                cur_IPIs = []
                for ii in np.arange(1,len(lines)): #append letters and IPIs starting at index 1
                    cur_Letters.append(lines[ii][0])
                    cur_IPIs.append(lines[ii][1])
                cur_arrLets.append(''.join(cur_Letters))
                cur_arrIPIs.append(cur_IPIs)
            Letters[subj][gg]=cur_arrLets
            IPI[subj][gg].append(cur_arrIPIs)

#Step 2: Entropy results
def Entropy(perc):
    e=np.sum(-perc*np.log2(perc))
    return e


Letters3 = [a+b+c for a in 'LRF' for b in 'LRF' for c in 'LRF']
ns_pairs = np.ones((SubjNb,GameNb,len(Letters3))) #Initialize vector of fires with all ones
probs_pairs = np.ones((SubjNb,GameNb,len(Letters3))) #make sure the frequency is never 0 (Laplace smoothing)
ent_games = np.ones((SubjNb,GameNb))
for sub in range(SubjNb): #subjects
    for gg in range(GameNb): #games
        for seq in Letters[sub][gg]: 
            ns_pairs[sub][gg] = np.add(ns_pairs[sub][gg],np.array([seq.count(ll) for ll in Letters3],dtype=float))
        probs_pairs[sub][gg] = ns_pairs[sub][gg]/np.sum(ns_pairs[sub][gg]) #Vector divided by the sum of the probabilities
        ent_games[sub][gg] = Entropy(probs_pairs[sub][gg]) #Calculate Entropy next


#Print Entropy scores
path = '../'+Output_file+'/'
SeqFile = path+'Entropy_'+Name_Output+'_Transfer.txt'
ff_toWrite = open(SeqFile,"w+")
ToWrite = "Subject\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
ff_toWrite.write(ToWrite)
for subj in range(SubjNb):
    ToWrite = names[subj]
    for nn in range(GameNb):
        cGame = str(nn+1)
        Per = str(ent_games[subj][nn])
        ToWrite=ToWrite+'\t'+Per
    ToWrite=ToWrite+"\n"
    ff_toWrite.write(ToWrite)
ff_toWrite.close()


