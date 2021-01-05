#!/bin/bash
SPEED=$1 #Pass either of MMM, SSS,SMS,MSM
mkdir ${SPEED}
cp -r Data_${SPEED} ${SPEED}
mkdir ./${SPEED}/${SPEED}_dat
mkdir ./${SPEED}/${SPEED}_evt
mv ./${SPEED}/Data_${SPEED} ./${SPEED}/${SPEED}
cp ./code/move_cluster_${SPEED}_dat.sh ./${SPEED}/${SPEED}
cp ./code/move_cluster_${SPEED}_evt.sh ./${SPEED}/${SPEED}
cp ./code/copy_holds_${SPEED}.sh ./${SPEED}
mkdir ./${SPEED}/${SPEED}_holds
cp ./code/move_cluster_ext_dat.sh ./${SPEED}/${SPEED}_dat
cp ./code/move_cluster_ext_evt.sh ./${SPEED}/${SPEED}_evt
cp ./code/Entropy.py ./code/AutoCorr.py ./code/DTS.py ./code/GameCycles.py ./code/PreprocessEvt.py  ./code/ProcessScores_Cluster_Models.py ./code/ResDefMis.py ./${SPEED}
cd ${SPEED}/${SPEED}
./move_cluster_${SPEED}_dat.sh
./move_cluster_${SPEED}_evt.sh
cd ../${SPEED}_dat
./move_cluster_ext_dat.sh
cd ../${SPEED}_evt
./move_cluster_ext_evt.sh
cd ../
mkdir Outputs
mkdir ${SPEED}_Preproc
echo "Preprocessing files & Scores - Step 1"
python ProcessScores_Cluster_Models.py $SPEED
python PreprocessEvt.py $SPEED
mkdir Game_Cycles
mkdir Game_Cycles/${SPEED}
mkdir Game_Cycles/${SPEED}/Rotations
mkdir Game_Cycles/${SPEED}/NoRotations
./copy_holds_${SPEED}.sh
echo "Creating Game Cycles - Step 2"
python GameCycles.py $SPEED
mkdir Discrete_Game_Cycles
mkdir Discrete_Game_Cycles/${SPEED}
mkdir Discrete_Game_Cycles/${SPEED}/Rotations
mkdir Discrete_Game_Cycles/${SPEED}/NoRotations
echo "Creating Discrete Game Cycles - Step 3"
python DTS.py $SPEED
echo "Processing Entropy measures - Step 4"
python Entropy.py $SPEED
echo "Processing ACF measures - Step 5"
python AutoCorr.py $SPEED
echo "Computing Resets/Deflations/Misses - Step 6"
python ResDefMis.py $SPEED
