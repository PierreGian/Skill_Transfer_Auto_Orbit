#!/bin/bash
MNAME=$1 #Pass name of model, need a name!
SPEED=MMM
if [ -d "./Model_Inputs/$SPEED" ]
then
	echo "Dealing with $SPEED"
	cd Scripts
	python CVMu_Models.py $SPEED $MNAME
	cd ../
fi
SPEED=MSM
if [ -d "./Model_Inputs/$SPEED" ]
then
	echo "Dealing with $SPEED"
	cd Scripts
	python CVMu_Models.py $SPEED $MNAME
	cd ../
fi
SPEED=SMS
if [ -d "./Model_Inputs/$SPEED" ]
then
	echo "Dealing with $SPEED"
	cd Scripts
	python CVMu_Models.py $SPEED $MNAME
	cd ../
fi
SPEED=SSS
if [ -d "./Model_Inputs/$SPEED" ]
then
	echo "Dealing with $SPEED"
	cd Scripts
	python CVMu_Models.py $SPEED $MNAME
	cd ../
fi
cd Scripts
python CVMu_Humans.py
python Reformat_Measures.py
cd ../Human_Inputs
mkdir Outputs/old
cd Outputs
mv CVIFI_mediumTransfer_Humans.txt CVIFI_slowTransfer_Humans.txt ./old/
mv StdIFI_mediumTransfer_Humans.txt StdIFI_slowTransfer_Humans.txt ./old/
mv MeanIFI_mediumTransfer_Humans.txt MeanIFI_slowTransfer_Humans.txt ./old/
mv Amplitude_thresh_ALL_Humans_avg_Transfer.txt ./old/
mv Entropy_ALL_Humans_Transfer.txt ./old/
mv Periodicity_thresh_ALL_Humans_avg_Transfer.txt ./old/
cd ../../Scripts
python R_Human_Preprocess.py
cd ../
SPEED=MMM
if [ -d "./Model_Inputs/$SPEED" ]
then
	cd Scripts
	python R_Model_Preprocess.py $SPEED $MNAME
	cd ../
fi
SPEED=MSM
if [ -d "./Model_Inputs/$SPEED" ]
then
	cd Scripts
	python R_Model_Preprocess.py $SPEED $MNAME
	cd ../
fi
SPEED=SMS
if [ -d "./Model_Inputs/$SPEED" ]
then
	cd Scripts
	python R_Model_Preprocess.py $SPEED $MNAME
	cd ../
fi
SPEED=SSS
if [ -d "./Model_Inputs/$SPEED" ]
then
	cd Scripts
	python R_Model_Preprocess.py $SPEED $MNAME
	cd ../
fi
cd Scripts
python Concatenate_R_files.py $MNAME

