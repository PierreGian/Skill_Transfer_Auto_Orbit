#!/usr/bin/env python
# coding: utf-8

import numpy as np
import os
import sys
Argums = sys.argv
#First argument: Speed to preprocess

########################################
Model = Argums[1] #Name of the model
########################################
paths = [
    '../Human_Inputs/Outputs/R_Humans.txt',
    '../Model_Inputs/MMM/Outputs/R_'+Model+'_MMM.txt',
    '../Model_Inputs/MSM/Outputs/R_'+Model+'_MSM.txt',
    '../Model_Inputs/SSS/Outputs/R_'+Model+'_SSS.txt',
    '../Model_Inputs/SMS/Outputs/R_'+Model+'_SMS.txt'
]

#Store final table in the R way
Finalpath='../'
SeqFile = Finalpath+'R_HumanModel_'+Model+'.txt'
ff_toWrite = open(SeqFile,"w+")
ToWrite = "Agent\tSubject\tcondition1\tcondition2\tGameNb\tPoints\tEntropy\tPeriodicity\tAmplitude\tMuIFI\tStdIFI\tCV\tResets\tDeflations\tMisses\tGameSpeed\n"
ff_toWrite.write(ToWrite)

#Store data from each file
for pp in paths:
    SeqFile = pp
    try:
        f_toOpen = open(SeqFile,"r") 
        lines = [line.rstrip() for line in f_toOpen]
        for i,line in enumerate(lines):
            if(i>0):
                lineSplit = line.split("\t")
                ToAdd=''
                if(lineSplit[2]=='slow' and lineSplit[3]=='slow'):
                    ToAdd='SSS'
                    ToWrite=line+"\t"+ToAdd+"\n"
                    ff_toWrite.write(ToWrite)
                elif(lineSplit[2]=='slow' and lineSplit[3]=='medium'):
                    ToAdd='SMS'
                    ToWrite=line+"\t"+ToAdd+"\n"
                    ff_toWrite.write(ToWrite)
                elif(lineSplit[2]=='medium' and lineSplit[3]=='slow'):
                    ToAdd='MSM'
                    ToWrite=line+"\t"+ToAdd+"\n"
                    ff_toWrite.write(ToWrite)
                elif(lineSplit[2]=='medium' and lineSplit[3]=='medium'):
                    ToAdd='MMM'
                    ToWrite=line+"\t"+ToAdd+"\n"
                    ff_toWrite.write(ToWrite)
    except (FileNotFoundError, IOError):
    	print("%s does not exist"%SeqFile)
ff_toWrite.close()
