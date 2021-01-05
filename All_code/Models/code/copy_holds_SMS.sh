#!/bin/bash
for d in */;
do
   	cd SMS_Preproc
   	for ff in *.holds;
	do
   		cp $ff ../SMS_holds
	done
	cd ../
done
