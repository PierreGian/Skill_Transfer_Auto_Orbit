#!/usr/bin/env python
# coding: utf-8

import numpy as np
from glob import glob
GameNb=15
Data_file = "Data"
Preproc_file = "Preproc"

my_game_search = '../'+Data_file+'/*_1.evt'
paths = glob(my_game_search)
NbPaths = len(paths)
#print(paths)
names = [paths[i].split('/')[-1].split('.')[0].split('_')[0] for i in range(NbPaths)]
SubjNb = len(names)
#names contains all the names of all the subjects


#This cell is creating *.evts, *.holds and *.holrel files, we are only keeping the events of interest for each file type
for subj in range(SubjNb):
    currPlayer = "../Data/"+names[subj] 
    Player_T = "../Preproc/"+names[subj] 
    for k in range(GameNb):
        name1 = currPlayer+"_"+str(k+1)+".evt"
        name2 = Player_T+"_"+str(k+1)+".evts"
        name3 = Player_T+"_"+str(k+1)+".holds"
        name4 = Player_T+"_"+str(k+1)+".holrel"
        f_toOpen = open(name1,"r") 
        lines = [line.rstrip().split("\t") for line in f_toOpen] 
        ff_toWrite = open(name2,"w+")
        for line in lines:
            toPrint_baseline = line[1]+"\t"+line[2]
            if(not line[3]=='[]'):
                #print(line[3])
                evts = line[3][1:-1].rstrip().split(",")
                for evt in evts:
                    toPrint = toPrint_baseline+"\t"+evt.replace("\"","").replace(" ","")+"\n"
                    ff_toWrite.write(toPrint)
        ff_toWrite.close()
        f_toOpen.close() #close the file
        f_toOpen = open(name2,"r") 
        lines = [line.rstrip().split("\t") for line in f_toOpen] 
        ff_toWrite = open(name3,"w+")
        for line in lines:
            if(line[2][:4]=="hold" or line[2]=="fortress-destroyed" or line[2]=="fortress-respawn" or line[2]=="random-rotation"):
                ToWrite = line[0]+"\t"+line[1]+"\t"+line[2]+"\n"
                ff_toWrite.write(ToWrite)
        ff_toWrite.close()
        f_toOpen.close() #close the file
        f_toOpen = open(name2,"r") 
        lines = [line.rstrip().split("\t") for line in f_toOpen] 
        ff_toWrite = open(name4,"w+")
        for line in lines:
            if(line[2][:4]=="hold" or line[2][:7]=="release" or line[2]=="fortress-destroyed" or line[2]=="fortress-respawn" or line[2]=="random-rotation"):
                ToWrite = line[0]+"\t"+line[1]+"\t"+line[2]+"\n"
                ff_toWrite.write(ToWrite)
        ff_toWrite.close()
        f_toOpen.close() #close the file
