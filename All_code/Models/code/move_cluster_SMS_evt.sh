#!/bin/bash
for d in */;
do
   	mkdir ../SMS_evt/$d
   	cd $d
   	for ff in *.evt;
	do
   		mv $ff ../../SMS_evt/$d/
	done
	cd ../
done
