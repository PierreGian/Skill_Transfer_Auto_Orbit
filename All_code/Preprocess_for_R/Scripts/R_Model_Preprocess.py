#!/usr/bin/env python
# coding: utf-8

import numpy as np

GameNb=15
SubjNb=100
import os
import sys
Argums = sys.argv
#First argument: Speed to preprocess

########################################
Type = Argums[1]
ModelNb = Argums[2]
########################################

path = '../Model_Inputs/'+Type+'/Outputs'
cond_map = {'SSS':('slow','slow'),'SMS':('slow','medium'),'MSM':('medium','slow'),'MMM':('medium','medium')}
cond1 = cond_map[Type][0]
cond2 = cond_map[Type][1]

SeqFile = path+'/AllScores_'+Type+'.txt'
f_toOpen = open(SeqFile,"r") 
lines_Perf = [line.rstrip().split("\t") for line in f_toOpen]
SubjNb=int(lines_Perf[-1][0].split("_")[-1])
#print(SubjNb)

Perf = np.zeros((SubjNb,GameNb))
Entropy = np.zeros((SubjNb,GameNb))
Amplitude = np.zeros((SubjNb,GameNb))
Periodicity = np.zeros((SubjNb,GameNb))
MuIFI = np.zeros((SubjNb,GameNb))
StdIFI = np.zeros((SubjNb,GameNb))
CVIFI = np.zeros((SubjNb,GameNb))
Resets = np.zeros((SubjNb,GameNb))
Deflations = np.zeros((SubjNb,GameNb))
Misses = np.zeros((SubjNb,GameNb))
names = ['' for ss in range(SubjNb)]


#Loading Performance
for i,line in enumerate(lines_Perf):
    if(i>0):
        cur_name = line[0]
        idx=i-1
        names[idx] = cur_name
        for gg in range(GameNb):
            curG = gg+1
            Perf[idx][gg] = int(line[curG])
            
#Loading Entropy
SeqFile = path+'/Entropy_'+Type+'_Transfer.txt'
f_toOpen = open(SeqFile,"r") 
lines_Entropy = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines_Entropy[0]
for i,line in enumerate(lines_Entropy):
    if(i>0):
        cur_name = line[0]
        idx=i-1
        for gg in range(GameNb):
            curG = gg+1
            Entropy[idx][gg] = float(line[curG])
            
#Loading Amplitude
SeqFile = path+'/Amplitude_'+Type+'_Transfer.txt'
f_toOpen = open(SeqFile,"r") 
lines_Amplitude = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines_Amplitude[0]
for i,line in enumerate(lines_Amplitude):
    if(i>0):
        cur_name = line[0]
        idx=i-1
        for gg in range(GameNb):
            curG = gg+1
            Amplitude[idx][gg] = float(line[curG])

#Loading Periodicity
SeqFile = path+'/Periodicity_'+Type+'_Transfer.txt'
f_toOpen = open(SeqFile,"r") 
lines_Periodicity = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines_Periodicity[0]
for i,line in enumerate(lines_Periodicity):
    if(i>0):
        cur_name = line[0]
        idx=i-1
        for gg in range(GameNb):
            curG = gg+1
            Periodicity[idx][gg] = float(line[curG])
            
#Loading Mu IFI
SeqFile = path+'/MeanIFI_'+Type+'_'+ModelNb+'.txt'
f_toOpen = open(SeqFile,"r") 
lines_MuIFI = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines_MuIFI[0]
for i,line in enumerate(lines_MuIFI):
    if(i>0):
        cur_name = line[0]
        idx=i-1
        for gg in range(GameNb):
            curG = gg+1
            MuIFI[idx][gg] = float(line[curG])

#Loading Std IFI
SeqFile = path+'/StdIFI_'+Type+'_'+ModelNb+'.txt'
f_toOpen = open(SeqFile,"r") 
lines_StdIFI = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines_StdIFI[0]
for i,line in enumerate(lines_StdIFI):
    if(i>0):
        cur_name = line[0]
        idx=i-1
        for gg in range(GameNb):
            curG = gg+1
            StdIFI[idx][gg] = float(line[curG])

#Loading CV
SeqFile = path+'/CVIFI_'+Type+'_'+ModelNb+'.txt'
f_toOpen = open(SeqFile,"r") 
lines_CVIFI = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines_CVIFI[0]
for i,line in enumerate(lines_CVIFI):
    if(i>0):
        cur_name = line[0]
        idx=i-1
        for gg in range(GameNb):
            curG = gg+1
            CVIFI[idx][gg] = float(line[curG])
            
#Loading Resets
SeqFile = path+'/'+Type+'_Resets.txt'
f_toOpen = open(SeqFile,"r") 
lines_Resets = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines_Resets[0]
for i,line in enumerate(lines_Resets):
    if(i>0):
        cur_name = line[0]
        idx=i-1
        for gg in range(GameNb):
            curG = gg+1
            Resets[idx][gg] = float(line[curG])
            
#Loading Deflations
SeqFile = path+'/'+Type+'_Deflations.txt'
f_toOpen = open(SeqFile,"r") 
lines_Deflations = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines_Deflations[0]
for i,line in enumerate(lines_Deflations):
    if(i>0):
        cur_name = line[0]
        idx=i-1
        for gg in range(GameNb):
            curG = gg+1
            Deflations[idx][gg] = float(line[curG])
            
#Loading Misses
SeqFile = path+'/'+Type+'_Misses.txt'
f_toOpen = open(SeqFile,"r") 
lines_Misses = [line.rstrip().split("\t") for line in f_toOpen]
cats = lines_Misses[0]
for i,line in enumerate(lines_Misses):
    if(i>0):
        cur_name = line[0]
        idx=i-1
        for gg in range(GameNb):
            curG = gg+1
            Misses[idx][gg] = float(line[curG])


#Store final table in the R way
SeqFile = path+'/R_'+ModelNb+'_'+Type+'.txt'
ff_toWrite = open(SeqFile,"w+")
ToWrite = "Agent\tSubject\tcondition1\tcondition2\tGameNb\tPoints\tEntropy\tPeriodicity\tAmplitude\tMuIFI\tStdIFI\tCV\tResets\tDeflations\tMisses\n"
ff_toWrite.write(ToWrite)

for subj in range(SubjNb):
    ToWriteBase = "Model\t"+names[subj]+"\t"+cond1+"\t"+cond2
    for gg in range(GameNb):
        ToWrite = ToWriteBase+"\t"+str(gg+1)+"\t"+str(Perf[subj][gg])+"\t"+str(Entropy[subj][gg])+"\t"+str(Periodicity[subj][gg])+"\t"+str(Amplitude[subj][gg])+"\t"+str(MuIFI[subj][gg])+"\t"+str(StdIFI[subj][gg])+"\t"+str(CVIFI[subj][gg])+"\t"+str(Resets[subj][gg])+"\t"+str(Deflations[subj][gg])+"\t"+str(Misses[subj][gg])+"\n"
        ff_toWrite.write(ToWrite)
ff_toWrite.close()

