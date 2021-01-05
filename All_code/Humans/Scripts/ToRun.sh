#!/bin/bash
#SCORES is the file with all the subject names & conditions
SCORES="Summary_Scores_ALL.txt"
#OUTPUT is the desired output prefix for the output files
OUTPUT="Humans_Final"

mkdir Game_Cycles
mkdir Discrete_Game_Cycles
mkdir Outputs
mkdir Preproc
cd Game_Cycles
mkdir NoRotations
mkdir Rotations
cd ../Discrete_Game_Cycles
mkdir NoRotations
mkdir Rotations
cd ../Scripts
echo "Preprocessing event files 1/5"
python Preprocess.py
echo "Creating Game Cycles 2/5"
python GameCycles.py $SCORES
echo "Creating Discrete game cycles 3/5"
python DTS2.py $SCORES
echo "Computing Entropy 4/5"
python Entropy.py $SCORES  $OUTPUT
echo "Computing Autocorr measures 5/5"
python AutoCorr_v2.py $SCORES $OUTPUT
echo "DONE"
