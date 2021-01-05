#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import pylab

##### Load prepared Excel data file with scores
GameNb=15
SubjNb = 180
OutputPath='../Human_Inputs/Outputs/'
names=['' for j in range(SubjNb)]
conds=[('','') for j in range(SubjNb)]
scores=[('','','','','','','','','','','','','','','') for j in range(SubjNb)]
avgs = ['' for j in range(SubjNb)]
SeqFile = OutputPath+'/Summary_Scores_ALL.txt'
f_toOpen = open(SeqFile,"r") 
lines = [line.rstrip().split("\t") for line in f_toOpen]

cats = lines[0]

idx=0
for ii in np.arange(1,len(lines)):
    cur_line=lines[ii]
    #print(cur_line)
    names[idx] = cur_line[0]
    conds[idx] = (cur_line[1],cur_line[2])
    idx=idx+1

#Function to identify the subject index of a given suubject name
def FindSubIdx(name):
    for el,nn in enumerate(names):
        if(nn==name):
            return el

#Rewrite output measures files with conditions inserted
FileType = ['Periodicity_thresh_ALL_Humans_avg_Transfer','Amplitude_thresh_ALL_Humans_avg_Transfer','Entropy_ALL_Humans_Transfer']
Output_Files = ['Periodicity_Transfer_Humans','Amplitude_Transfer_Humans','Entropy_Transfer_Humans']
ind=0
for ffile in FileType:
    inputPath = OutputPath+ffile+'.txt'
    outputPath = OutputPath+Output_Files[ind]+'_SORTED.txt'
    ff_toWrite = open(outputPath,"w+")
    ToWrite = "Subject\tcondition1\tcondition2\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
    ff_toWrite.write(ToWrite)
    f_toOpen = open(inputPath,"r") 
    lines = [line.rstrip().split("\t") for line in f_toOpen]
    for cur_line in lines[1:]:
        subj_indx = FindSubIdx(cur_line[0])
        ToWrite = names[subj_indx]+"\t"+conds[subj_indx][0]+"\t"+conds[subj_indx][1]
        for j in np.arange(1,16):
            ToWrite=ToWrite+"\t"+cur_line[j]
        ToWrite=ToWrite+"\n"
        ff_toWrite.write(ToWrite)
    ff_toWrite.close()
    ind=ind+1
