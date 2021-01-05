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

#Function for DTS -> ONLY Holds will generate series of 1s (even if the release is outside the DTS matrix)
def Create_DTS(cur_cyc):
    res=16
    timeStart = int(np.floor(int(cur_cyc[0][1])/res)*res)
    timeEnd = int(np.ceil(int(cur_cyc[-1][1])/res)*res)
    lenVec = int((timeEnd-timeStart)/res)+1 #We want to count both timeStart and timeEnd
    DTS = np.zeros((3,lenVec)) #Initialize the DTS vector
    KeyStart = [-5,-5,-5] #Start of series of 1 Left/Right/Fires
    KeyEnd = [-5,-5,-5] #End of series of 1 Left/Right/Fires
    AddSeries = -5 #Boolean turned off
    curPos = 0
    curT = timeStart
    for tup in cur_cyc: #looping through tuples in current cycle
        evt = tup[0]
        evt_time = int(tup[1])
        while(not(evt_time<=curT)):
            curPos = curPos+1
            curT = curT+res
        if(evt=="hold-left"):
            KeyStart[0] = curPos
        elif(evt=="hold-right"):
            KeyStart[1] = curPos
        elif(evt=="hold-fire"):
            KeyStart[2] = curPos
        elif(evt=="release-left"):
            AddSeries = 0
            KeyEnd[AddSeries] = curPos
        elif(evt=="release-right"):
            AddSeries = 1
            KeyEnd[AddSeries] = curPos
        elif(evt=="release-fire"):
            AddSeries = 2
            KeyEnd[AddSeries] = curPos
        if(AddSeries>=0 and KeyStart[AddSeries]>=0): #Add series of 1 in matrix now, NOT if release is alone
            for pos in np.arange(KeyStart[AddSeries],KeyEnd[AddSeries]):
                DTS[AddSeries][pos] = 1
            #Reinitialize everything to -5
            KeyStart[AddSeries],KeyEnd[AddSeries] = -5,-5
            AddSeries = -5
    #End of matrix, need to update numbers for keys with holds BUT no release
    ToAdd = [ii for ii in range(3) if (KeyStart[ii]>=0 and KeyEnd[ii]==-5)]
    for kk in ToAdd:
        for pos in np.arange(KeyStart[kk],lenVec):
            DTS[kk][pos] = 1
    return DTS

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
    path = './Discrete_Game_Cycles/'+Type+'/'
    for k in range(GameNb):
        c_rot_nb = 0
        c_noRot_nb = 0
        times = []
        events = []
        cycles= [] #cycles will be stored in tuples! Make life easier
        name_f = Player_O+"_"+str(k+1)+".holrel"
        f_toOpen = open(name_f,"r") 
        lines = [line.rstrip().split("\t") for line in f_toOpen]
        AddLine = True
        for line in lines:
            cur_t = int(line[0])
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
            game = str(k+1)
            name_file = ''
            if(rotations[ii]==1):
                c_rot_nb = c_rot_nb + 1
                name_file = path+"Rotations/"+name+"_Game"+game+"_Rot"+str(c_rot_nb)+".dists"
            else:
                c_noRot_nb = c_noRot_nb + 1
                name_file = path+"NoRotations/"+name+"_Game"+game+"_NoRot"+str(c_noRot_nb)+".dists"
            #now deal with the cycle itself
            cur_DTS = Create_DTS(cycles[ii])
            Lefts, Rights, Fires = cur_DTS[0], cur_DTS[1], cur_DTS[2]           
            ff_toWrite = open(name_file,"w+")
            ToWrite = ""
            for eee in range(len(Lefts)):
                ToWrite = ToWrite+str(int(Lefts[eee]))+","
            ToWrite=ToWrite[:-1]+"\n"
            ff_toWrite.write(ToWrite)
            ToWrite = ""
            for eee in range(len(Rights)):
                ToWrite = ToWrite+str(int(Rights[eee]))+","
            ToWrite=ToWrite[:-1]+"\n"
            ff_toWrite.write(ToWrite)
            ToWrite = ""
            for eee in range(len(Fires)):
                ToWrite = ToWrite+str(int(Fires[eee]))+","
            ToWrite=ToWrite[:-1]+"\n"
            ff_toWrite.write(ToWrite)
        f_toOpen.close()

