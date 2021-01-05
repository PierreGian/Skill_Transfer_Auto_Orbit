#!/usr/bin/env python
# coding: utf-8


import numpy as np
import matplotlib.pyplot as plt
import pylab

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
Evt_file = Type+'_Preproc'
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


#Reset number computation
currPath = './'+Evt_file+'/'
outputPath = './Outputs/'+Type+'_Resets.txt'
ff_toWrite = open(outputPath,"w+")
ToWrite = "Subject\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
ff_toWrite.write(ToWrite)
for subj in range(len(names)):
    currPlayer = currPath+names[subj]
    resets = np.zeros(GameNb)
    for k in range(GameNb):
        resets[k]=0
        name1 = currPlayer+"_"+str(k+1)+".evts"
        f_toOpen = open(name1,"r") 
        lines = [line.rstrip().split("\t") for line in f_toOpen]
        for line in lines:
            if(line[1]=="vlner-reset"):
                resets[k]=resets[k]+1
        f_toOpen.close()
    ToWrite = names[subj]
    for k in range(GameNb):
        R_write = np.amin([100,resets[k]])
        ToWrite=ToWrite+"\t"+str(R_write)
    ToWrite=ToWrite+"\n"
    ff_toWrite.write(ToWrite)
ff_toWrite.close()


#Deflations number computation
currPath = './'+Evt_file+'/'
outputPath = './Outputs/'+Type+'_Deflations.txt'
ff_toWrite = open(outputPath,"w+")
ToWrite = "Subject\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
ff_toWrite.write(ToWrite)
for subj in range(len(names)):
    currPlayer = currPath+names[subj]
    deflates = np.zeros(GameNb)
    for k in range(GameNb):
        deflates[k]=0
        name1 = currPlayer+"_"+str(k+1)+".evts"
        f_toOpen = open(name1,"r") 
        lines = [line.rstrip().split("\t") for line in f_toOpen]
        for line in lines:
            if(line[1]=="start-deflating"):
                deflates[k]=deflates[k]+1
        f_toOpen.close()
    ToWrite = names[subj]
    for k in range(GameNb):
        D_write = np.amin([100,deflates[k]])
        ToWrite=ToWrite+"\t"+str(D_write)
    ToWrite=ToWrite+"\n"
    ff_toWrite.write(ToWrite)
ff_toWrite.close()


#Misses number computation
currPath = './'+Evt_file+'/'
outputPath = './Outputs/'+Type+'_Misses.txt'
ff_toWrite = open(outputPath,"w+")
ToWrite = "Subject\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
ff_toWrite.write(ToWrite)
for subj in range(len(names)):
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
            if(line[1]=="hit-fortress"):
                hits[k]=hits[k]+1
            elif(line[1]=="missile-fired"):
                fires[k]=fires[k]+1
        misses[k]=fires[k]-hits[k]
        f_toOpen.close()
    ToWrite = names[subj]
    for k in range(GameNb):
        M_write = np.amin([200,misses[k]])
        ToWrite=ToWrite+"\t"+str(M_write)
    ToWrite=ToWrite+"\n"
    ff_toWrite.write(ToWrite)
ff_toWrite.close()

