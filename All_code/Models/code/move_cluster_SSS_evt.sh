#!/bin/bash
for d in */;
do
   	mkdir ../SSS_evt/$d
   	cd $d
   	for ff in *.evt;
	do
   		mv $ff ../../SSS_evt/$d/
	done
	cd ../
done
