#!/usr/bin/env python
# coding: utf-8

import numpy as np

##### Load prepared Excel data file with scores
GameNb=15
SubjNb = 80
Allnames=[j for j in range(SubjNb)]
Allconds=[('','') for j in range(SubjNb)]
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

#Special search to get all the humans' names and identify the conditions they were assigned to
from glob import glob
GameNb=15
Data_file = "Data"
Output_file = "Outputs"
Preproc_file = "Preproc"

my_game_search = '../'+Data_file+'/*_1.evt'
paths = glob(my_game_search)
NbPaths = len(paths)
names = [paths[i].split('/')[-1].split('.')[0].split('_')[0] for i in range(NbPaths)]
N = len(names)
conds=[('','') for j in range(N)]
for i,nn in enumerate(names):
    for j,aa in enumerate(Allnames):
        if(nn==aa):
            conds[i]=Allconds[j]

#Reset number computation (capped at 100!!)
currPath = '../'+Preproc_file+'/'
outputPath = '../'+Output_file+'/AllResets.txt'
ff_toWrite = open(outputPath,"w+")
ToWrite = "Subject\tCondition1\tCondition2\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
ff_toWrite.write(ToWrite)
for subj in range(N):
    currPlayer = currPath+names[subj]
    resets = np.zeros(GameNb)
    for k in range(GameNb):
        resets[k]=0
        name1 = currPlayer+"_"+str(k+1)+".evts"
        f_toOpen = open(name1,"r") 
        lines = [line.rstrip().split("\t") for line in f_toOpen]
        for line in lines:
            if(line[2]=="vlner-reset"):
                resets[k]=resets[k]+1 #Count number of reset events
        f_toOpen.close()
    ToWrite = names[subj]+"\t"+conds[subj][0]+"\t"+conds[subj][1]
    for k in range(GameNb):
        R_write = np.amin([100,resets[k]])
        ToWrite=ToWrite+"\t"+str(R_write)
    ToWrite=ToWrite+"\n"
    ff_toWrite.write(ToWrite)
ff_toWrite.close()

#Deflations number computation (capped at 100!!)
currPath = '../'+Preproc_file+'/'
outputPath = '../'+Output_file+'/AllDeflations.txt'
ff_toWrite = open(outputPath,"w+")
ToWrite = "Subject\tCondition1\tCondition2\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
ff_toWrite.write(ToWrite)
for subj in range(N):
    currPlayer = currPath+names[subj]
    deflates = np.zeros(GameNb)
    for k in range(GameNb):
        deflates[k]=0
        name1 = currPlayer+"_"+str(k+1)+".evts"
        f_toOpen = open(name1,"r") 
        lines = [line.rstrip().split("\t") for line in f_toOpen]
        for line in lines:
            if(line[2]=="start-deflating"):
                deflates[k]=deflates[k]+1 #count number of deflation events
        f_toOpen.close()
    ToWrite = names[subj]+"\t"+conds[subj][0]+"\t"+conds[subj][1]
    for k in range(GameNb):
        D_write = np.amin([100,deflates[k]])
        ToWrite=ToWrite+"\t"+str(D_write)
    ToWrite=ToWrite+"\n"
    ff_toWrite.write(ToWrite)
ff_toWrite.close()

#Misses number computation (capped at 200!!)
currPath = '../'+Preproc_file+'/'
outputPath = '../'+Output_file+'/AllMisses.txt'
ff_toWrite = open(outputPath,"w+")
ToWrite = "Subject\tCondition1\tCondition2\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
ff_toWrite.write(ToWrite)
for subj in range(N):
    currPlayer = currPath+names[subj]
    misses = np.zeros(GameNb)
    hits = np.zeros(GameNb)
    fires = np.zeros(GameNb)
    for k in range(GameNb):
        misses[k]=0
        hits[k]=0
        fires[k]=0
        name1 = currPlayer+"_"+str(k+1)+".evts"
        f_toOpen = open(name1,"r") 
        lines = [line.rstrip().split("\t") for line in f_toOpen]
        for line in lines:
            if(line[2]=="hit-fortress"):
                hits[k]=hits[k]+1
            elif(line[2]=="missile-fired"):
                fires[k]=fires[k]+1
        misses[k]=fires[k]-hits[k] #Get number of missile-fired and subtract number of hits from that
        f_toOpen.close()
    ToWrite = names[subj]+"\t"+conds[subj][0]+"\t"+conds[subj][1]
    for k in range(GameNb):
        M_write = np.amin([200,misses[k]])
        ToWrite=ToWrite+"\t"+str(M_write)
    ToWrite=ToWrite+"\n"
    ff_toWrite.write(ToWrite)
ff_toWrite.close()

