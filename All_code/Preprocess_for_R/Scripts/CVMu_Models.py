#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import pylab
import os
import sys
Argums = sys.argv
#First argument: Speed to preprocess

########################################
Type = Argums[1]
ModelNb = Argums[2] #Model number to add in name at the end of script
########################################


#load data
#Special search file to get all the model names
from glob import glob
GameNb=15
#Specify Evt file here!
Evt_file = Type+'_holds'
######################
path = '../Model_Inputs/'
my_game_search = path+Type+'/'+Evt_file+'/*_1.holds'
paths = glob(my_game_search)
NbPaths = len(paths)
Listnames = [paths[i].split('/')[-1].split('.')[0].split('-')[0] for i in range(NbPaths)]
name_comps = [nn.split('_') for nn in Listnames]
Listnames = []
for nn in name_comps:
    Str_ToAppend = nn[0]+'_'+nn[1]+'_'+nn[2]
    Listnames.append(Str_ToAppend)
SubjNb = len(Listnames)
ints = [int(Listnames[i].split('_')[-1]) for i in range(SubjNb)]
#Sorting by integer
orderInts = np.argsort(np.array(ints))
#names contains all the names of all the model subjects
names = [Listnames[nn] for nn in orderInts]
#names contains all the names of all the model subjects

#Writing the game cycles with and without rotations 
Letters = [[] for s in range(len(names))]
AllIPIs = [[] for s in range(len(names))]
GameNbs = [[] for s in range(len(names))]
for subj,name in enumerate(names):
    Player_O = path+Type+'/'+Evt_file+"/"+name
    for k in range(GameNb):
        c_rot_nb = 0
        c_noRot_nb = 0
        times = []
        events = []
        cycles= [] #cycles will be stored in tuples! Make life easier
        name_f = Player_O+"_"+str(k+1)+".holds"
        f_toOpen = open(name_f,"r")
        lines = [line.rstrip().split("\t") for line in f_toOpen]
        AddLine = True
        for idx,line in enumerate(lines):
            if(line[1]=="fortress-destroyed"):
                AddLine = False
            elif(line[1]=="fortress-respawn"):
                AddLine = True
            if(AddLine==True or line[1]=="fortress-destroyed"):
                times.append(line[0])
                events.append(line[1])
        cur_cyc = []
        rotations = []
        cur_rot = 0
        for idx,ee in enumerate(events):
            if(ee=="fortress-destroyed"):
                cycles.append(cur_cyc)
                rotations.append(cur_rot)
                cur_cyc = [] #reset game cycle and create new list for new cycle
                cur_rot = 0 #reset the rotation marker
            elif(ee=="random-rotation"):
                cur_rot = 1
            else:
                cur_cyc.append((ee,times[idx])) #store information in tuple
        len_cyc = len(cycles) #length of all cycles
        for ii in range(len_cyc): #loop through cycles
            game = str(k+1)
            if(rotations[ii]==0): #Only deal with no rotation cycles
                #now deal with the cycle itself
                prev_time = 0
                Evts = []
                IPIs = []
                #remove the double shots
                Remove_Shot = False
                idx_toRem = len(cycles[ii])-1
                #if(not(ii==len_cyc-1)): #all but the last cycle => apply this only when we need to keep the last cycle
                while(Remove_Shot==False):
                    if(cycles[ii][idx_toRem][0]=="hold-fire"):
                        del cycles[ii][idx_toRem]
                        Remove_Shot=True
                    else:
                        idx_toRem = idx_toRem -1 #decrement until last shot is removed
                for cc,tup in enumerate(cycles[ii]): #1st cycle: remove first element/others: remove respawn
                    evt = tup[0]
                    evt_time = int(tup[1])
                    toAdd = ''
                    if(not(evt=="fortress-respawn")):
                        if(evt=="hold-fire"):
                            toAdd='F'
                        elif(evt=="hold-right" or evt=="hold-left"):
                            continue #do not add to cycle list and go to next event
                        if(not(cc==0)):
                            Evts.append(toAdd)
                            c_IPI = evt_time-prev_time
                            IPIs.append(c_IPI)
                    prev_time=evt_time
                NewLets = []
                NewIPI = []
                NewGames = []
                for eee in range(len(Evts)):
                    NewLets.append(str(Evts[eee]))
                    NewIPI.append(IPIs[eee])
                    NewGames.append(k)
                Letters[subj].append(NewLets)
                AllIPIs[subj].append(NewIPI)
                GameNbs[subj].append(NewGames)
                f_toOpen.close()

done=0
while(done==0): #make sure all the elements have been deleted
    done = 1
    for i,x in enumerate(Letters):
        for j,ll in enumerate(x):
            for k,el in enumerate(ll):
                if(not(el=='F')):
                    #print("problem at subject %d cycle %d element %d"%(i,j,k))
                    del Letters[i][j][k]
                    del AllIPIs[i][j][k]
                    del GameNbs[i][j][k]
                    done=0

#Initialization
IFI = [[[] for k in range(GameNb)] for s in range(len(names))] #1) Subject, 2) GameNb, 3) IFIs

#Append date to arrays - Fast
for i,S in enumerate(AllIPIs):
    for j,cyc in enumerate(S):
        for k,el in enumerate(cyc):
            IFI[i][GameNbs[i][j][k]].append(el)


#CoefV
All_CV = np.zeros((GameNb,len(names)))
MuAll_CV = np.zeros(GameNb)
ISImu = np.zeros((GameNb,len(names)))
ISIstd = np.zeros((GameNb,len(names)))

for gg in range(GameNb):
    for subj in range(len(names)):
        cur_IFI = np.array(IFI[subj][gg])
        if(not(cur_IFI.size == 0)):
            ISImu[gg][subj] = np.mean(cur_IFI)
            ISIstd[gg][subj] = np.std(cur_IFI)
            All_CV[gg][subj] = np.std(cur_IFI)/np.mean(cur_IFI)
        else:
            ISImu[gg][subj] = 0
            ISIstd[gg][subj] = 0
            All_CV[gg][subj] = 0

for gg in range(GameNb):
    MuAll_CV[gg] = np.mean(All_CV[gg])


#Now printing R file
#Points are PointsFast/PointsMedium/PointsSlow
#Now printing the Excel version of the table to help plot results
#1) Mu ISI
path = '../Model_Inputs/'
path2 = path+Type+'/Outputs/'
SeqFile = path2+'MeanIFI_'+Type+'_'+ModelNb+'.txt'
ff_toWrite = open(SeqFile,"w+")
ToWrite = "Subject\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
ff_toWrite.write(ToWrite)
#Printing Fast
for subj in range(len(names)):
    cName = names[subj]
    ToWrite = cName
    for gg in range(GameNb):
        ToWrite=ToWrite+'\t'+str(ISImu[gg][subj])
    ToWrite=ToWrite+"\n"
    ff_toWrite.write(ToWrite)


#2) std ISI
SeqFile = path2+'StdIFI_'+Type+'_'+ModelNb+'.txt'
ff_toWrite = open(SeqFile,"w+")
ToWrite = "Subject\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
ff_toWrite.write(ToWrite)
#Printing Fast
for subj in range(len(names)):
    cName = names[subj]
    ToWrite = cName
    for gg in range(GameNb):
        ToWrite=ToWrite+'\t'+str(ISIstd[gg][subj])
    ToWrite=ToWrite+"\n"
    ff_toWrite.write(ToWrite)


#3) CV ISI
SeqFile = path2+'CVIFI_'+Type+'_'+ModelNb+'.txt'
ff_toWrite = open(SeqFile,"w+")
ToWrite = "Subject\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
ff_toWrite.write(ToWrite)
#Printing Fast
for subj in range(len(names)):
    cName = names[subj]
    ToWrite = cName
    for gg in range(GameNb):
        ToWrite=ToWrite+'\t'+str(All_CV[gg][subj])
    ToWrite=ToWrite+"\n"
    ff_toWrite.write(ToWrite)
ff_toWrite.close()

