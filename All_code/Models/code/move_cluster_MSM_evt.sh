#!/bin/bash
for d in */;
do
   	mkdir ../MSM_evt/$d
   	cd $d
   	for ff in *.evt;
	do
   		mv $ff ../../MSM_evt/$d/
	done
	cd ../
done
