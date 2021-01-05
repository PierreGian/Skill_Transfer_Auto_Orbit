#!/bin/bash
for d in */;
do
   	mkdir ../MMM_evt/$d
   	cd $d
   	for ff in *.evt;
	do
   		mv $ff ../../MMM_evt/$d/
	done
	cd ../
done
