#!/bin/bash
MODEL="Model1" #Change the name of the model here!

cd Preprocess_for_R
echo "Copy/Pasting output to R preprocessing folder"
./GetInputs.sh
echo "Preprocessing R Table"
./Preprocess_R.sh $MODEL
mv R_HumanModel_${MODEL}.txt ../
echo "Done"

