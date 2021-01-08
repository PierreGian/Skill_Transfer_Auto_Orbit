#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import pylab


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
Preproc_file = "Preproc"

my_game_search = '../'+Data_file+'/*_1.evt'
paths = glob(my_game_search)
NbPaths = len(paths)
names = [paths[i].split('/')[-1].split('.')[0].split('_')[0] for i in range(NbPaths)]
N = len(names)
conds=[('','') for j in range(N)]
print("There are %i human subjects"%N)
for i,nn in enumerate(names):
    for j,aa in enumerate(Allnames):
        if(nn==aa):
            conds[i]=Allconds[j]

def Check_Timing(cur_cyc):
    prev_t = 0
    for ee in cur_cyc:
        if(int(ee[1])<prev_t):
            return False
        prev_t = int(ee[1])
    return True

#Writing the game cycles with and without rotations 
condition=['slow','medium','fast']

#Writing the game cycles with and without rotations 
for subj,name in enumerate(names):
    Player_O = "../"+Preproc_file+"/"+names[subj]
    path = "../Game_Cycles/"    
    for k in range(GameNb):
        c_rot_nb = 0
        c_noRot_nb = 0
        times = []
        events = []
        cycles= [] #cycles will be stored in tuples!
        name_f = Player_O+"_"+str(k+1)+".holds"
        f_toOpen = open(name_f,"r")
        lines = [line.rstrip().split("\t") for line in f_toOpen]
        AddLine = True
        for idx,line in enumerate(lines):
            if(line[2]=="fortress-destroyed"):
                AddLine = False
            elif(line[2]=="fortress-respawn"):
                AddLine = True
            if(AddLine==True or line[2]=="fortress-destroyed"):
                times.append(line[0])
                events.append(line[2])
        cur_cyc = []
        rotations = []
        cur_rot = 0
        for idx,ee in enumerate(events):
            if(ee=="fortress-destroyed"):
                if(not(not cur_cyc)):
                    cycles.append(cur_cyc) #Append cycle
                    rotations.append(cur_rot)
                cur_cyc = [] #reset game cycle and create new list for new cycle
                cur_rot = 0 #reset the rotation marker
            elif(ee=="random-rotation"):
                cur_rot = 1
            else:
                cur_cyc.append((ee,times[idx])) #store information in tuple
                
        #Need to check timing of cycles before printing
        Timings = [True for cc in range(len(cycles))]
        for ii in range(len(cycles)):
            Timings[ii] = Check_Timing(cycles[ii]) #Switch to False if timing for given cycle is wrong
        cycles = [cycles[ii] for ii in range(len(cycles)) if Timings[ii]==True] #Trimming cycles with bad timing
                
        len_cyc = len(cycles) #length of all cycles
        for ii in range(len_cyc): #loop through cycles
            #first deal with the name of the file
            cur_cond = ''
            if(k >=5 and k<10):
                cur_cond = conds[subj][1]
            else:
                cur_cond = conds[subj][0]
            game = str(k+1)
            name_file = ''
            if(rotations[ii]==1):
                c_rot_nb = c_rot_nb + 1
                name_file = path+"Rotations/"+name+"_"+cur_cond+"_Game"+game+"_Rot"+str(c_rot_nb)+".txt"
            else:
                c_noRot_nb = c_noRot_nb + 1
                name_file = path+"NoRotations/"+name+"_"+cur_cond+"_Game"+game+"_NoRot"+str(c_noRot_nb)+".txt"
            #now deal with the cycle itself
            prev_time = 0
            Evts = []
            IPIs = []
            #remove the double shots
            Remove_Shot = False
            idx_toRem = len(cycles[ii])-1
            while(Remove_Shot==False):
                if(cycles[ii][idx_toRem][0]=="hold-fire"):
                    del cycles[ii][idx_toRem]
                    Remove_Shot=True
                else:
                    idx_toRem = idx_toRem -1 #decrement until last shot is removed
            for cc,tup in enumerate(cycles[ii]):
                evt = tup[0]
                evt_time = int(tup[1])
                toAdd = ''
                if(not(evt=="fortress-respawn")):
                    if(evt=="hold-left"):
                        toAdd='L'
                    elif(evt=="hold-right"):
                        toAdd='R'
                    elif(evt=="hold-fire"):
                        toAdd='F'
                    elif(evt=="hold-thrust"):
                        continue
                    if(not(cc==0)): #1st cycle: remove first element/others: would be fortress-respawn 
                        Evts.append(toAdd)
                        c_IPI = evt_time-prev_time
                        IPIs.append(c_IPI)
                prev_time=evt_time
            ff_toWrite = open(name_file,"w+")
            ToWrite = "keypress\tIPI\n"
            ff_toWrite.write(ToWrite)
            for eee in range(len(Evts)):
                ToWrite = str(Evts[eee])+"\t"+str(IPIs[eee])+"\n"
                ff_toWrite.write(ToWrite)
            f_toOpen.close()


