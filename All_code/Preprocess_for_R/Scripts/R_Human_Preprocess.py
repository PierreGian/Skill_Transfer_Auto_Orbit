#!/usr/bin/env python
# coding: utf-8

import numpy as np

#Function to identify the subject index of a given subject name
def FindSubIdx(name,all_names):
    for el,nn in enumerate(all_names):
        if(nn==name):
            return el

#Prepare Human Data
GameNb=15
SubjNb = 80
path = '../Human_Inputs/Outputs/'
names=[j for j in range(SubjNb)]
conds=[('','') for j in range(SubjNb)]
Points = [['' for gg in range(GameNb)] for ss in range(SubjNb)]
avgs=np.zeros(SubjNb)
SeqFile = path+'Transfer_Scores_Humans.txt'
f_toOpen = open(SeqFile,"r") 
lines = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines[0]

idx=0
for ii in np.arange(1,len(lines)):
    cur_line=lines[ii]
    names[idx] = cur_line[0]
    conds[idx] = (cur_line[1],cur_line[2])
    for gg in np.arange(3,18):
        Points[idx][gg-3] = cur_line[gg]
    avgs[idx] = cur_line[18]
    idx=idx+1

Entropy = np.zeros((SubjNb,GameNb))
Amplitude = np.zeros((SubjNb,GameNb))
Periodicity = np.zeros((SubjNb,GameNb))
MuIFI = np.zeros((SubjNb,GameNb))
StdIFI = np.zeros((SubjNb,GameNb))
CVIFI = np.zeros((SubjNb,GameNb))
Resets = np.zeros((SubjNb,GameNb))
Deflations = np.zeros((SubjNb,GameNb))
Misses = np.zeros((SubjNb,GameNb))


#Loading Entropy
SeqFile = path+'Entropy_Transfer_Humans_SORTED.txt'
f_toOpen = open(SeqFile,"r") 
lines_Entropy = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines_Entropy[0]

for i,line in enumerate(lines_Entropy):
    if(i>0):
        cur_name = line[0]
        idx = FindSubIdx(cur_name,names)
        for gg in range(GameNb):
            curG = gg+3
            Entropy[idx][gg] = line[curG]

#Loading Amplitude
SeqFile = path+'Amplitude_Transfer_Humans_SORTED.txt'
f_toOpen = open(SeqFile,"r") 
lines_Amplitude = [line.rstrip().split("\t") for line in f_toOpen]
for i,line in enumerate(lines_Amplitude):
    if(i>0):
        cur_name = line[0]
        idx = FindSubIdx(cur_name,names)
        for gg in range(GameNb):
            curG = gg+3
            Amplitude[idx][gg] = line[curG]

#Loading Periodicity
SeqFile = path+'Periodicity_Transfer_Humans_SORTED.txt'
f_toOpen = open(SeqFile,"r") 
lines_Periodicity = [line.rstrip().split("\t") for line in f_toOpen]
for i,line in enumerate(lines_Periodicity):
    if(i>0):
        cur_name = line[0]
        idx = FindSubIdx(cur_name,names)
        for gg in range(GameNb):
            curG = gg+3
            Periodicity[idx][gg] = line[curG]
            
#Loading Mu IFI
SeqFile = path+'MeanIFI_Transfer_Humans.txt'
f_toOpen = open(SeqFile,"r") 
lines_MuIFI = [line.rstrip().split("\t") for line in f_toOpen]
for i,line in enumerate(lines_MuIFI):
    if(i>0):
        cur_name = line[0]
        idx = FindSubIdx(cur_name,names)
        for gg in range(GameNb):
            curG = gg+3
            MuIFI[idx][gg] = line[curG]
            
#Loading Std IFI
SeqFile = path+'StdIFI_Transfer_Humans.txt'
f_toOpen = open(SeqFile,"r") 
lines_StdIFI = [line.rstrip().split("\t") for line in f_toOpen]
for i,line in enumerate(lines_StdIFI):
    if(i>0):
        cur_name = line[0]
        idx = FindSubIdx(cur_name,names)
        for gg in range(GameNb):
            curG = gg+3
            StdIFI[idx][gg] = line[curG]

#Loading CV IFI
SeqFile = path+'CVIFI_Transfer_Humans.txt'
f_toOpen = open(SeqFile,"r") 
lines_CVIFI = [line.rstrip().split("\t") for line in f_toOpen]
for i,line in enumerate(lines_CVIFI):
    if(i>0):
        cur_name = line[0]
        idx = FindSubIdx(cur_name,names)
        for gg in range(GameNb):
            curG = gg+3
            CVIFI[idx][gg] = line[curG]
            
#Loading Resets
SeqFile = path+'AllResets.txt'
f_toOpen = open(SeqFile,"r") 
lines_Resets = [line.rstrip().split("\t") for line in f_toOpen]
for i,line in enumerate(lines_Resets):
    if(i>0):
        cur_name = line[0]
        idx = FindSubIdx(cur_name,names)
        for gg in range(GameNb):
            curG = gg+3
            Resets[idx][gg] = line[curG]
            
#Loading Deflations
SeqFile = path+'AllDeflations.txt'
f_toOpen = open(SeqFile,"r") 
lines_Deflations = [line.rstrip().split("\t") for line in f_toOpen]
for i,line in enumerate(lines_Deflations):
    if(i>0):
        cur_name = line[0]
        idx = FindSubIdx(cur_name,names)
        for gg in range(GameNb):
            curG = gg+3
            Deflations[idx][gg] = line[curG]
            
#Loading Misses
SeqFile = path+'AllMisses.txt'
f_toOpen = open(SeqFile,"r") 
lines_Misses = [line.rstrip().split("\t") for line in f_toOpen]
for i,line in enumerate(lines_Misses):
    if(i>0):
        cur_name = line[0]
        idx = FindSubIdx(cur_name,names)
        for gg in range(GameNb):
            curG = gg+3
            Misses[idx][gg] = line[curG]

#Store final table in the R way
SeqFile = path+'R_Humans.txt'
ff_toWrite = open(SeqFile,"w+")
ToWrite = "Agent\tSubject\tcondition1\tcondition2\tGameNb\tPoints\tEntropy\tPeriodicity\tAmplitude\tMuIFI\tStdIFI\tCV\tResets\tDeflations\tMisses\n"
ff_toWrite.write(ToWrite)

#Printing all humans
for subj in range(SubjNb):
    ToWriteBase = "Human\t"+names[subj]+"\t"+conds[subj][0]+"\t"+conds[subj][1]
    for gg in range(GameNb):
        ToWrite = ToWriteBase+"\t"+str(gg+1)+"\t"+str(Points[subj][gg])+"\t"+str(Entropy[subj][gg])+"\t"+str(Periodicity[subj][gg])+"\t"+str(Amplitude[subj][gg])+"\t"+str(MuIFI[subj][gg])+"\t"+str(StdIFI[subj][gg])+"\t"+str(CVIFI[subj][gg])+"\t"+str(Resets[subj][gg])+"\t"+str(Deflations[subj][gg])+"\t"+str(Misses[subj][gg])+"\n"
        ff_toWrite.write(ToWrite)
ff_toWrite.close()

