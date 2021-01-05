#!/bin/bash
for d in */;
do
   	cd SSS_Preproc
   	for ff in *.holds;
	do
   		cp $ff ../SSS_holds
	done
	cd ../
done
