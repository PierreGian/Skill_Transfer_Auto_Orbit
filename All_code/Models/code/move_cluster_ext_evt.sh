#!/bin/bash
EXT=evt
for d in */;
do
   	cd $d
   	for ff in *.${EXT};
	do
   		mv $ff ../
	done
	cd ../
	rm -r $d
done
