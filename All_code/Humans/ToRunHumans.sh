#!/bin/bash

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
echo "Preprocessing event files 1/6"
python Preprocess.py
echo "Creating Game Cycles 2/6"
python GameCycles.py
echo "Creating Discrete game cycles 3/6"
python DTS.py
echo "Computing Entropy 4/6"
python Entropy.py
echo "Computing Autocorrelation measures 5/6"
python ACF.py
echo "Computing Resets, Deflations & Misses 6/6"
python ResDefMis.py
echo "DONE"
