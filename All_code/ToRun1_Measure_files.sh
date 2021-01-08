#!/bin/bash
cd Models
echo "Dealing with SSS"
./ProcessSpeed.sh SSS
echo "Dealing with MMM"
./ProcessSpeed.sh MMM
echo "Dealing with SMS"
./ProcessSpeed.sh SMS
echo "Dealing with MSM"
./ProcessSpeed.sh MSM
cd ../Humans
echo "Dealing with Humans"
./ToRunHumans.sh
echo "Done"
