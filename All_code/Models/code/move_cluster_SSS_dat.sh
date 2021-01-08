#!/bin/bash
for d in */;
do
   	mkdir ../SSS_dat/$d
   	cd $d
   	for ff in *.dat;
	do
   		mv $ff ../../SSS_dat/$d/
	done
	cd ../
done
