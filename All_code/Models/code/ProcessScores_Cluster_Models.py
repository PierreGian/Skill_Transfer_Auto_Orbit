#!/usr/bin/env python
# coding: utf-8

import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab
#Looking for all folders and sorting by number run in cluster
from glob import glob
GameNb=15
Argums = sys.argv
Type = Argums[1] #Need to pass the condition ('FFF', 'MFM' etc.) as argument here
FileNm = Type+'_dat'
Path='./'+FileNm

my_game_search = Path+'/*.dat'
paths = glob(my_game_search)
NbPaths = len(paths)
Listnames = [paths[i].split('/')[-1].split('.')[0].split('-')[0] for i in range(NbPaths)]
Listnames = list(set(Listnames))
N = len(Listnames)
ints = [int(Listnames[i].split('_')[-1]) for i in range(N)]
orderInts = np.argsort(np.array(ints))
names = [Listnames[nn] for nn in orderInts]

#Open the '.dat' files and extract the total score
AllScores = np.zeros((N,GameNb))
for subj,name in enumerate(names):
    Player_O = Path+"/"+name
    for k in range(GameNb):
        name_f = Player_O+"-1-"+str(k+1)+".dat"
        f_toOpen = open(name_f,"r")
        lines = [line.rstrip().split(" ") for line in f_toOpen]
        for line in lines:
            if(len(line)==4):
                if(line[1]=='total' and line[2]=='score'):
                    AllScores[subj,k] = int(line[3])
                    
#Excel version of models
ScoresFile = "./AllScores_"+Type+".txt"
ff_toWrite = open(ScoresFile,"w+")
gameStrNbs = "SubjectNb"
for ii in range(GameNb):
    gameStrNbs = gameStrNbs+"\t"+str(ii+1)
gameStrNbs=gameStrNbs+"\n"
ToWrite = gameStrNbs
ff_toWrite.write(ToWrite)
for subj in range(N):
    sub_nb=subj+1
    ToWrite=names[subj]
    for k in range(GameNb):
        ToWrite=ToWrite+'\t'+str(int(AllScores[subj,k]))
    ToWrite=ToWrite+'\n'
    ff_toWrite.write(ToWrite)
ff_toWrite.close()

