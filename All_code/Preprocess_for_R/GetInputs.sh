#!/bin/bash
MODEL=Models
mkdir Model_Inputs
mkdir Human_Inputs
mkdir Human_Inputs/Holds
cd ../$MODEL/
SPEED=MMM
if [ -d "./$SPEED" ]
then
	echo "Dealing with $SPEED"
	cd ${SPEED}
	cp AllScores_${SPEED}.txt Outputs
	cd ../ 
	mkdir ../Preprocess_for_R/Model_Inputs/${SPEED} #will need to change this line later!!
	cp -R ${SPEED}/${SPEED}_holds ../Preprocess_for_R/Model_Inputs/${SPEED}
	cp -R ${SPEED}/Outputs ../Preprocess_for_R/Model_Inputs/${SPEED}
fi
SPEED=MSM
if [ -d "./$SPEED" ]
then
	echo "Dealing with $SPEED"
	cd ${SPEED}
	cp AllScores_${SPEED}.txt Outputs
	cd ../ 
	mkdir ../Preprocess_for_R/Model_Inputs/${SPEED} #will need to change this line later!!
	cp -R ${SPEED}/${SPEED}_holds ../Preprocess_for_R/Model_Inputs/${SPEED}
	cp -R ${SPEED}/Outputs ../Preprocess_for_R/Model_Inputs/${SPEED}
fi
SPEED=SMS
if [ -d "./$SPEED" ]
then
	echo "Dealing with $SPEED"
	cd ${SPEED}
	cp AllScores_${SPEED}.txt Outputs
	cd ../ 
	mkdir ../Preprocess_for_R/Model_Inputs/${SPEED} #will need to change this line later!!
	cp -R ${SPEED}/${SPEED}_holds ../Preprocess_for_R/Model_Inputs/${SPEED}
	cp -R ${SPEED}/Outputs ../Preprocess_for_R/Model_Inputs/${SPEED}
fi
SPEED=SSS
if [ -d "./$SPEED" ]
then
	echo "Dealing with $SPEED"
	cd ${SPEED}
	cp AllScores_${SPEED}.txt Outputs
	cd ../ 
	mkdir ../Preprocess_for_R/Model_Inputs/${SPEED} #will need to change this line later!!
	cp -R ${SPEED}/${SPEED}_holds ../Preprocess_for_R/Model_Inputs/${SPEED}
	cp -R ${SPEED}/Outputs ../Preprocess_for_R/Model_Inputs/${SPEED}
fi
cd ../
echo "Dealing with Humans"
cp Humans/Scripts/Transfer_Scores_Humans.txt Humans/Outputs
cp -R Humans/Outputs ./Preprocess_for_R/Human_Inputs/
cp Humans/Preproc/*.holds ./Preprocess_for_R/Human_Inputs/Holds

