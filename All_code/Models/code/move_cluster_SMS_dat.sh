#!/bin/bash
for d in */;
do
   	mkdir ../SMS_dat/$d
   	cd $d
   	for ff in *.dat;
	do
   		mv $ff ../../SMS_dat/$d/
	done
	cd ../
done
