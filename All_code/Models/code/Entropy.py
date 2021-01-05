#!/usr/bin/env python
# coding: utf-8

import numpy as np

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
ToWrite_path = Type
Evt_file = Type+'_Preproc'
Final_Folder = 'Outputs'
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


from glob import glob
Letters = [[[] for gg in range(GameNb)] for i in range(SubjNb)]
IPI = [[[] for gg in range(GameNb)] for i in range(SubjNb)]

for subj,name in enumerate(names):
    path_cyc = './Game_Cycles/'+Type+'/NoRotations/'+name
    for gg in range(GameNb):
        my_game_search2 = path_cyc+'_Game'+str(gg+1)+'_NoRot*.txt'
        cur_paths = glob(my_game_search2)
        Listfiles = [cur_paths[i].split('/')[-1] for i in range(len(cur_paths))]
        if(not(not Listfiles)): #if the returned list is not empty
            list_len = len(Listfiles)
            cur_arrLets = []
            cur_arrIPIs = []
            cur_arrgames = -1
            for cc in np.arange(1,list_len+1):
                SeqFile = path_cyc+"_Game"+str(gg+1)+'_NoRot'+str(cc)+'.txt'
                f_toOpen = open(SeqFile,"r") 
                lines = [line.rstrip().split("\t") for line in f_toOpen]
                cur_Letters = []
                cur_IPIs = []
                for ii in np.arange(1,len(lines)): #append letters and IPIs starting at index 1
                    cur_Letters.append(lines[ii][0])
                    cur_IPIs.append(lines[ii][1])
                cur_arrLets.append(''.join(cur_Letters))
                cur_arrIPIs.append(cur_IPIs)
            Letters[subj][gg]=cur_arrLets
            IPI[subj][gg].append(cur_arrIPIs)



#Step 2: Entropy results
def Entropy(perc):
    e=np.sum(-perc*np.log2(perc))
    return e


Letters3 = [a+b+c for a in 'LRF' for b in 'LRF' for c in 'LRF']
ns_pairs = np.ones((SubjNb,GameNb,len(Letters3))) #Initialize vector of fires with all ones
probs_pairs = np.ones((SubjNb,GameNb,len(Letters3))) #make sure the frequency is never 0 (Laplace smoothing)
ent_games = np.ones((SubjNb,GameNb))
for sub in range(SubjNb): #subjects
    for gg in range(GameNb): #games
        for seq in Letters[sub][gg]: 
            ns_pairs[sub][gg] = np.add(ns_pairs[sub][gg],np.array([seq.count(ll) for ll in Letters3],dtype=float))
        probs_pairs[sub][gg] = ns_pairs[sub][gg]/np.sum(ns_pairs[sub][gg]) #Vector divided by the sum of the probabilities
        ent_games[sub][gg] = Entropy(probs_pairs[sub][gg]) #Calculate Entropy next


#1) Entropy
SeqFile = './'+Final_Folder+'/'+'Entropy_'+Type+'_Transfer.txt'
ff_toWrite = open(SeqFile,"w+")
ToWrite = "Subject\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\n"
ff_toWrite.write(ToWrite)
for subj in range(SubjNb):
    ToWrite = names[subj]
    for nn in range(GameNb):
        cGame = str(nn+1)
        Per = str(ent_games[subj][nn])
        ToWrite=ToWrite+'\t'+Per
    ToWrite=ToWrite+"\n"
    ff_toWrite.write(ToWrite)
ff_toWrite.close()








