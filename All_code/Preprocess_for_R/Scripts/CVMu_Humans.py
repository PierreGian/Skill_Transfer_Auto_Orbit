#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import pylab

#Function to identify the subject index of a given subject name
def FindSubIdx(name,all_names):
    for el,nn in enumerate(all_names):
        if(nn==name):
            return el

##### Load prepared Excel data file with scores
GameNb=15
SubjNb = 80
HumanPath = '../Human_Inputs/Outputs/'
names1=[j for j in range(SubjNb)]
conds1=[('','') for j in range(SubjNb)]
avgs=np.zeros(SubjNb)
SeqFile=HumanPath+'Transfer_Scores_Humans.txt'
f_toOpen = open(SeqFile,"r") 
lines = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines[0]
idx=0
for ii in np.arange(1,len(lines)):
    cur_line=lines[ii]
    names1[idx] = cur_line[0]
    conds1[idx] = (cur_line[1],cur_line[2])
    avgs[idx] = cur_line[18]
    idx=idx+1

#Writing the game cycles with and without rotations
Letters1 = [[] for s in range(len(names1))]
IPIs_all1 = [[] for s in range(len(names1))]
Conditions_all1 = [[] for s in range(len(names1))]
GameNbs1 = [[] for s in range(len(names1))]
for subj,name in enumerate(names1):
    Player_O = "../Human_Inputs/Holds/"+name
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
            #first deal with the name of the file
            cur_cond = ''
            if(k >=5 and k<10):
                cur_cond = conds1[subj][1]
            else:
                cur_cond = conds1[subj][0]
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
                NewConds = []
                NewGames = []
                for eee in range(len(Evts)):
                    NewLets.append(str(Evts[eee]))
                    NewIPI.append(IPIs[eee])
                    NewConds.append(cur_cond)
                    NewGames.append(k)
                Letters1[subj].append(NewLets)
                IPIs_all1[subj].append(NewIPI)
                Conditions_all1[subj].append(NewConds)
                GameNbs1[subj].append(NewGames)
                f_toOpen.close()

#Merging batch 1/2 & 3
names = names1 
conds = conds1 
Letters = Letters1
IPIs_all = IPIs_all1
Conditions_all = Conditions_all1
GameNbs = GameNbs1



done=0
while(done==0): #make sure all the elements have been deleted
    done = 1
    for i,x in enumerate(Letters):
        for j,ll in enumerate(x):
            for k,el in enumerate(ll):
                if(not(el=='F')):
                    #print(el)
                    #print("problem at subject %d cycle %d element %d"%(i,j,k))
                    del Letters[i][j][k]
                    del IPIs_all[i][j][k]
                    del Conditions_all[i][j][k]
                    del GameNbs[i][j][k]
                    done=0


# # Within-subject analyses
AllSpeeds = ['slow','medium']
for CurSpeed in AllSpeeds:
 MediumCombo=[CurSpeed,'medium']
 SlowCombo=[CurSpeed,'slow']

 #Initialization
 SlowIFI = [[[] for k in range(GameNb)] for s in range(len(names))] #1) Subject, 2) GameNb, 3) IFIs
 MediumIFI = [[[] for k in range(GameNb)] for s in range(len(names))]
 NbNames = int(len(names)/4)
 SlowNames = ['' for i in range(NbNames)]
 MediumNames = ['' for i in range(NbNames)]

 inds = [0,0]
 #Append date to arrays
 for i,S in enumerate(IPIs_all):
     if(conds[i][0]==MediumCombo[0] and conds[i][1]==MediumCombo[1]): #medium condition
         MediumNames[inds[1]] = names[i]
         inds[1] = inds[1] + 1
         for j,cyc in enumerate(S):
             for k,el in enumerate(cyc):
                        MediumIFI[i][GameNbs[i][j][k]].append(el)
     elif(conds[i][0]==SlowCombo[0] and conds[i][1]==SlowCombo[1]): #slow condition
         SlowNames[inds[0]] = names[i]
         inds[0] = inds[0] + 1
         for j,cyc in enumerate(S):
             for k,el in enumerate(cyc):
                        SlowIFI[i][GameNbs[i][j][k]].append(el)


 #CoefV
 nbGroup = int(len(names)/4)
 Slow_CV = np.zeros((GameNb,nbGroup))
 Medium_CV = np.zeros((GameNb,nbGroup))
 MuSlow_CV = np.zeros(GameNb)
 MuMedium_CV = np.zeros(GameNb)
 ISImuSlow = np.zeros((GameNb,nbGroup))
 ISImuMedium = np.zeros((GameNb,nbGroup))
 ISIstdSlow = np.zeros((GameNb,nbGroup))
 ISIstdMedium = np.zeros((GameNb,nbGroup))
 MusISI = np.zeros((2,GameNb)) #Slow, medium
 StdISI = np.zeros((2,GameNb))

 sub_inds = [0,0] #indices for each game speed
 for subj,ctup in enumerate(conds): 
     if(ctup[0]==MediumCombo[0] and ctup[1]==MediumCombo[1]): #medium condition
         for gg in range(GameNb):
             cur_IFI = np.array(MediumIFI[subj][gg])
             if(not(cur_IFI.size == 0)):
                 ISImuMedium[gg][sub_inds[0]] = np.mean(cur_IFI)
                 ISIstdMedium[gg][sub_inds[0]] = np.std(cur_IFI)
                 Medium_CV[gg][sub_inds[0]] = np.std(cur_IFI)/np.mean(cur_IFI) 
             else:
                 ISImuMedium[gg][sub_inds[0]] = 0
                 ISIstdMedium[gg][sub_inds[0]] = 0
                 Medium_CV[gg][sub_inds[0]] = 0
         sub_inds[0] = sub_inds[0] + 1
     elif(ctup[0]==SlowCombo[0] and ctup[1]==SlowCombo[1]): #slow condition
         for gg in range(GameNb):
             cur_IFI = np.array(SlowIFI[subj][gg])
             if(not(cur_IFI.size == 0)):
                 ISImuSlow[gg][sub_inds[1]] = np.mean(cur_IFI)
                 ISIstdSlow[gg][sub_inds[1]] = np.std(cur_IFI)
                 Slow_CV[gg][sub_inds[1]] = np.std(cur_IFI)/np.mean(cur_IFI) 
             else:
                 ISImuSlow[gg][sub_inds[1]] = 0
                 ISIstdSlow[gg][sub_inds[1]] = 0
                 Slow_CV[gg][sub_inds[1]] = 0
         sub_inds[1] = sub_inds[1] + 1

 for gg in range(GameNb):
     MuSlow_CV[gg] = np.mean(Slow_CV[gg])
     MuMedium_CV[gg] = np.mean(Medium_CV[gg])
     MusISI[0,gg] = np.mean(ISImuSlow[gg])
     MusISI[1,gg] = np.mean(ISImuMedium[gg])
     StdISI[0,gg] = np.mean(ISIstdSlow[gg])
     StdISI[1,gg] = np.mean(ISIstdMedium[gg])


 #Now printing the Excel version of the table to help plot results
 #1) Mu ISI
 path = HumanPath
 SeqFile = path+'MeanIFI_'+CurSpeed+'Transfer_Humans.txt'
 ff_toWrite = open(SeqFile,"w+")
 ToWrite = "Subject\tcondition1\tcondition2\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
 ff_toWrite.write(ToWrite)
 #Printing Medium
 for subj in range(NbNames):
     cName = MediumNames[subj]+'\t'+MediumCombo[0]+'\t'+MediumCombo[1]
     ToWrite = cName
     for gg in range(GameNb):
         ToWrite=ToWrite+'\t'+str(ISImuMedium[gg][subj])
     ToWrite=ToWrite+"\n"
     ff_toWrite.write(ToWrite)
 #Printing Slow
 for subj in range(NbNames):
     cName = SlowNames[subj]+'\t'+SlowCombo[0]+'\t'+SlowCombo[1]
     ToWrite = cName
     for gg in range(GameNb):
         ToWrite=ToWrite+'\t'+str(ISImuSlow[gg][subj])
     ToWrite=ToWrite+"\n"
     ff_toWrite.write(ToWrite)
 ff_toWrite.close()

 #2) std ISI
 SeqFile = path+'StdIFI_'+CurSpeed+'Transfer_Humans.txt'
 ff_toWrite = open(SeqFile,"w+")
 ToWrite = "Subject\tcondition1\tcondition2\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
 ff_toWrite.write(ToWrite)
 #Printing Medium
 for subj in range(NbNames):
     cName = MediumNames[subj]+'\t'+MediumCombo[0]+'\t'+MediumCombo[1]
     ToWrite = cName
     for gg in range(GameNb):
         ToWrite=ToWrite+'\t'+str(ISIstdMedium[gg][subj])
     ToWrite=ToWrite+"\n"
     ff_toWrite.write(ToWrite)
 #Printing Slow
 for subj in range(NbNames):
     cName = SlowNames[subj]+'\t'+SlowCombo[0]+'\t'+SlowCombo[1]
     ToWrite = cName
     for gg in range(GameNb):
         ToWrite=ToWrite+'\t'+str(ISIstdSlow[gg][subj])
     ToWrite=ToWrite+"\n"
     ff_toWrite.write(ToWrite)
 ff_toWrite.close()

 #3) CV ISI
 SeqFile = path+'CVIFI_'+CurSpeed+'Transfer_Humans.txt'
 ff_toWrite = open(SeqFile,"w+")
 ToWrite = "Subject\tcondition1\tcondition2\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
 ff_toWrite.write(ToWrite)
 #Printing Medium
 for subj in range(NbNames):
     cName = MediumNames[subj]+'\t'+MediumCombo[0]+'\t'+MediumCombo[1]
     ToWrite = cName
     for gg in range(GameNb):
         ToWrite=ToWrite+'\t'+str(Medium_CV[gg][subj])
     ToWrite=ToWrite+"\n"
     ff_toWrite.write(ToWrite)
 #Printing Slow
 for subj in range(NbNames):
     cName = SlowNames[subj]+'\t'+SlowCombo[0]+'\t'+SlowCombo[1]
     ToWrite = cName
     for gg in range(GameNb):
         ToWrite=ToWrite+'\t'+str(Slow_CV[gg][subj])
     ToWrite=ToWrite+"\n"
     ff_toWrite.write(ToWrite)
 ff_toWrite.close()

#Concatenating all files
Types = ['CVIFI','MeanIFI','StdIFI']
for Type in Types:
 paths = [
     path+Type+'_mediumTransfer_Humans.txt',
     path+Type+'_slowTransfer_Humans.txt'
 ]


 #Store final table in the R way
 Finalpath=path
 SeqFile = Finalpath+Type+'_Transfer_Humans.txt'
 ff_toWrite = open(SeqFile,"w+")

 #Store data from each file
 PrintFirst=True
 for ii,pp in enumerate(paths):
     if(ii>0):
         PrintFirst=False
     SeqFile = pp
     f_toOpen = open(SeqFile,"r") 
     lines = [line.rstrip() for line in f_toOpen]
     for i,line in enumerate(lines):
         ToWrite = line+'\n'
         if(not(PrintFirst==False and i==0)):
             ff_toWrite.write(ToWrite)

