#!/bin/bash
for d in */;
do
   	mkdir ../MSM_dat/$d
   	cd $d
   	for ff in *.dat;
	do
   		mv $ff ../../MSM_dat/$d/
	done
	cd ../
done
