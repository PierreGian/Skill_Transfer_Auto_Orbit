#!/bin/bash
for d in */;
do
   	cd MSM_Preproc
   	for ff in *.holds;
	do
   		cp $ff ../MSM_holds
	done
	cd ../
done
