#!/usr/bin/env python
# coding: utf-8

import numpy as np
#Special search file to get all the model names
from glob import glob
GameNb=15

import sys
Argums = sys.argv
########################################
#Variable to update before starting running the script
Type = Argums[1] #'FFF', 'MMM'
########################################

#Specify Evt file here!
FileNm = Type+'_evt'
FilePreproc = Type+'_Preproc'
Path='./'+FileNm
Path_ToWrite = './'+FilePreproc
######################
my_game_search = Path+'/*-1.evt'
paths = glob(my_game_search)
NbPaths = len(paths)
Listnames = [paths[i].split('/')[-1].split('.')[0].split('-')[0] for i in range(NbPaths)]
N = len(Listnames)
ints = [int(Listnames[i].split('_')[-1]) for i in range(N)]
#Sorting by integer
orderInts = np.argsort(np.array(ints))
names = [Listnames[nn] for nn in orderInts]

#Create .evts files
for subj in range(N): 
    currPlayer = names[subj] 
    currPath = Path+'/'+currPlayer
    PathWri = Path_ToWrite+'/'+currPlayer
    for k in range(GameNb):
        name1 = currPath+"-1-"+str(k+1)+".evt"
        name2 = PathWri+"_"+str(k+1)+".evts"
        f_toOpen = open(name1,"r") 
        lines = [line.rstrip().split(" ") for line in f_toOpen] 
        ff_toWrite = open(name2,"w+")
        for line in lines:
            if(len(line)>2): #If the 3rd column exists
                toPrint_baseline = line[0]
                evts = line[2].split(",")
                for evt in evts:
                    toPrint = toPrint_baseline+"\t"+evt+"\n"
                    ff_toWrite.write(toPrint)
        ff_toWrite.close()
        f_toOpen.close() #close the file
        
#Write holds and holdrel files
for subj in range(N): 
    currPlayer = names[subj] 
    Player_T = Path_ToWrite+'/'+currPlayer
    for k in range(GameNb):
        name_Evt = Player_T+"_"+str(k+1)+".evts"
        name1 = Player_T+"_"+str(k+1)+".holds"
        name2 = Player_T+"_"+str(k+1)+".holrel"
        f_toOpen = open(name_Evt,"r") 
        lines = [line.rstrip().split("\t") for line in f_toOpen] 
        ff_toWrite = open(name1,"w+")
        for line in lines:
            if(line[1][:4]=="hold" or line[1]=="fortress-destroyed" or line[1]=="fortress-respawn" or line[1]=="random-rotation"):
                ToWrite = line[0]+"\t"+line[1]+"\n"
                ff_toWrite.write(ToWrite)
        ff_toWrite.close()
        f_toOpen.close() #close the file
        f_toOpen = open(name_Evt,"r") 
        lines = [line.rstrip().split("\t") for line in f_toOpen] 
        ff_toWrite = open(name2,"w+")
        for line in lines:
            if(line[1][:4]=="hold" or line[1][:7]=="release" or line[1]=="fortress-destroyed" or line[1]=="fortress-respawn" or line[1]=="random-rotation"):
                ToWrite = line[0]+"\t"+line[1]+"\n"
                ff_toWrite.write(ToWrite)
        ff_toWrite.close()
        f_toOpen.close() #close the file


