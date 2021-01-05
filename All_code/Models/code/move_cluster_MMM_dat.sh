#!/bin/bash
for d in */;
do
   	mkdir ../MMM_dat/$d
   	cd $d
   	for ff in *.dat;
	do
   		mv $ff ../../MMM_dat/$d/
	done
	cd ../
done
