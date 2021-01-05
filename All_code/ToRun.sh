#!/bin/bash
cd Models
./ProcessSpeed.sh SSS
./ProcessSpeed.sh MMM
./ProcessSpeed.sh SMS
./ProcessSpeed.sh MSM
cd ../Humans
./ToRunHumans.sh

