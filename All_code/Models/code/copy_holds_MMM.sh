#!/bin/bash
for d in */;
do
   	cd MMM_Preproc
   	for ff in *.holds;
	do
   		cp $ff ../MMM_holds
	done
	cd ../
done
