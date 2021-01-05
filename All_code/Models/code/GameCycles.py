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

def Check_Timing(cur_cyc):
    prev_t = 0
    for ee in cur_cyc:
        if(int(ee[1])<prev_t):
            return False
        prev_t = int(ee[1])
    return True


#Writing the game cycles with and without rotations 
for subj,name in enumerate(names):
    Player_O = './'+Evt_file+'/'+name
    path = './Game_Cycles/'+Type+'/'
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
                
        #Need to check timing of cycles before printing
        Timings = [True for cc in range(len(cycles))]
        for ii in range(len(cycles)):
            Timings[ii] = Check_Timing(cycles[ii]) #Switch to False if timing for given cycle is wrong
        cycles = [cycles[ii] for ii in range(len(cycles)) if Timings[ii]==True] #Trimming cycles with bad timing
                
        len_cyc = len(cycles) #length of all cycles
        for ii in range(len_cyc): #loop through cycles
            game = str(k+1)
            name_file = ''
            if(rotations[ii]==1):
                c_rot_nb = c_rot_nb + 1
                name_file = path+"Rotations/"+name+"_Game"+game+"_Rot"+str(c_rot_nb)+".txt"
            else:
                c_noRot_nb = c_noRot_nb + 1
                name_file = path+"NoRotations/"+name+"_Game"+game+"_NoRot"+str(c_noRot_nb)+".txt"
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
            for cc,tup in enumerate(cycles[ii]): #1st cycle: remove first element/others: remove respawn
                evt = tup[0]
                evt_time = int(tup[1])
                #go through the 6 cases now
                toAdd = ''
                if(not(evt=="fortress-respawn")):
                    if(evt=="hold-left"):
                        toAdd='L'
                    elif(evt=="hold-right"):
                        toAdd='R'
                    elif(evt=="hold-fire"):
                        toAdd='F'
                    if(not(cc==0)):
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

