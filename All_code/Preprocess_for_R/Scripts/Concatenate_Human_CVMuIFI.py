#!/usr/bin/env python
# coding: utf-8


import numpy as np


Type = 'CVIFI'
paths = [
    '/Users/pierregianferrara/Documents/Academic/CMU_PhD/Programming/Auto_Orbit/Transfer_All/All_subjects/Outputs/'+Type+'_fastTransfer_Humans.txt',
    '/Users/pierregianferrara/Documents/Academic/CMU_PhD/Programming/Auto_Orbit/Transfer_All/All_subjects/Outputs/'+Type+'_mediumTransfer_Humans.txt',
    '/Users/pierregianferrara/Documents/Academic/CMU_PhD/Programming/Auto_Orbit/Transfer_All/All_subjects/Outputs/'+Type+'_slowTransfer_Humans.txt'
]


#Store final table in the R way
Finalpath='/Users/pierregianferrara/Documents/Academic/CMU_PhD/Programming/Auto_Orbit/Transfer_All/All_subjects/Outputs/'
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



