# Skill_Transfer_Auto_Orbit

﻿This "Gianferrara_SkillTransfer_AutoOrbit_Readme.md" file was generated on 2021-01-08 by Pierre Gianferrara

GENERAL INFORMATION

1. Title of Dataset: Skill Transfer Auto Orbit

2. Author Information
	A. Principal Investigator Contact Information
		Name: John. R. Anderson
		Institution: Carnegie Mellon University
		Address: Baker Hall 3rd floor, 4909 Frew St, Pittsburgh, PA 15213
		Email: ja0s@andrew.cmu.edu

	B. First Author Contact Information
		Name: Pierre Gianferrara
		Institution: Carnegie Mellon University
		Address: Baker Hall 3rd floor, 4909 Frew St, Pittsburgh, PA 15213
		Email: pgianfer@andrew.cmu.edu

	C. Contact for ACT-R related questions
		Name: Dan Bothell
		Institution: Carnegie Mellon University
		Address: Baker Hall 3rd floor, 4909 Frew St, Pittsburgh, PA 15213
		Email: db30@andrew.cmu.edu
		
3. Time of human data collection: START: 2019-01-14, END: 2020-02-18

4. Platform where human data was collected: Amazon mechanical Turk
   Platform where model data was generated: Anderson Lab cluster through "act-r-sf" (code for Space Fortress related ACT-R model runs) - ask Dan Bothell (db30@andrew.cmu.edu) for more information

5. Information about funding sources that supported the collection of the data: 
Office   of   Naval Research   Grant   N00014-15-1-2151 and AFOSR/AFRL award  FA9550-18-1-0251.

SHARING/ACCESS INFORMATION

1. Licenses/restrictions placed on the data:
Users have the right to download and use this code, but are required to cite Gianferrara, Betts & Anderson (2021) when doing so.

2. Links to other publicly accessible locations of the data: 
<Kilthub link>

3. Was data derived from another source? No

4. Recommended citation for this dataset: 
Gianferrara, Betts & Anderson (2021)

DATA & FILE OVERVIEW

1. ACT-R - Folder containing the 3 different ACT-R models (*.lisp) that were used to generate the paper data using act-r-sf on the lab cluster

2. "Transfer_Scores_Humans.txt" - Summary of 80 human subjects' scores across conditions

3. All_code - Folder containing all the relevant scripts that were used to a] generate measure files from raw event files (time series with relevant game events based on log files), b] generate R table for statistical analyses, c] run statistical analyses in R
Please check out "Code_Instructions.md" under the "All_code" folder for further information on how to run preprocessing analyses
