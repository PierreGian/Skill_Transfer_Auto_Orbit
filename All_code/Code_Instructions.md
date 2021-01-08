# Skill_Transfer_Auto_Orbit

Code for Cognitive & Motor Skill Transfer paper on Auto Orbit video game

GENERAL INFORMATION

This secondary README file provides instructions on how to preprocess and analyze the data based on the game event files. You can also find information about the different files and folders at the bottom.

IMPORTANT

Before you follow the instructions, we encourage you to check the dependencies for R and Python to make sure that you have the right packages and libraries to run the code. If you miss one of these packages, you may run into unexpected errors when running the code.

INSTRUCTIONS

1. Download repository from Kilt Hub

2. Open a terminal and cd into Skill_Transfer_Auto_Orbit/All_code

3. Execute the following command: "./ToRun1_Measure_files.sh" to generate measure files for humans (in "Humans" folder) and ACT-R models (in "Models" folder)

4. Execute the following command: "./ToRun2_R_Table.sh" to generate the R table that you would typically use for R analyses. You can change the name of the model by editing the script and changing the name of the model where indicated.

5. You should see a file named "R_HumanModel_<MODEL_NAME>.txt"

6. To check the analyses in R with the paper human & model data (stored under "R_Analyses/ToInput"), open the folder "R_Analyses" and load any python notebook you may be interested in

DATA & FILE OVERVIEW

	ToRun1_Measure_files.sh - Run this Bash script first on the terminal to compute measure files from event files

	ToRun2_R_Table.sh - Run this Bash script second on the terminal to obtain an R-like table that would be input for statistical analyses

	HUMANS - folder with preprocessing scripts and data pertaining to human games
	  '--- DATA - folder with 1200 event files (80 humans * 15 games)
	  '--- ToRunHumans.sh - Bash script to preprocess human data in order
	  '--- Scripts - folder containing all the scripts that need to be run to preprocess the event files
	  	  '--- Preprocess.py - preprocess event files by extracting the relevant events and extract hold events
	  	  '--- GameCycles.py - Creates "no rotation" & "rotation" game cycles with keypress ('L' - left; 'R' - right; 'F' - fire) and inter-press interval (IPI)
	  	  '--- DTS.py - Creates "no rotation" & "rotation" discrete time series for each game cycle (1st row: lefts, 2nd row: rights, 3rd row: shots/fires)
	  	  '--- Entropy.py - Loads no rotation game cycles and computes entropy scores within games
	  	  '--- ACF.py - Loads no rotation discrete time series and computes periodicity and regularity scores based on the averaged autocorrelation function within games
	  	  '--- ResDefMis.py - Loads event files and computes resets, deflations and misses within games
	  	  '--- Transfer_Scores_Humans.txt - Summary of 80 human subjects' scores across conditions

	MODELS - folder with preprocessing scripts and model data
	  '--- ProcessSpeed.sh - Bash script that takes the condition as an argument (MMM/MSM/SMS/SSS) and preprocesses model runs from that condition
	  '--- MODEL_DATA - folder with model data data from example model runs (2 per conditions)
	  	  '--- Data_MMM - folder with data from 2 model runs in the MMM condition
	  	  '--- Data_MSM - folder with data from 2 model runs in the MSM condition
	  	  '--- Data_SMS - folder with data from 2 model runs in the SMS condition
	  	  '--- Data_SSS - folder with data from 2 model runs in the SSS condition
	  '--- code - folder containing all the scripts that need to be run to preprocess the event files
	 	  '--- PreprocessEvt.py - preprocess event files by extracting the relevant events and extract hold events
	  	  '--- GameCycles.py - Creates "no rotation" & "rotation" game cycles with keypress ('L' - left; 'R' - right; 'F' - fire) and inter-press interval (IPI)
	  	  '--- DTS.py - Creates "no rotation" & "rotation" discrete time series for each game cycle (1st row: lefts, 2nd row: rights, 3rd row: shots/fires)
	  	  '--- Entropy.py - Loads no rotation game cycles and computes entropy scores within games
	  	  '--- AutoCorr.py - Loads no rotation discrete time series and computes periodicity and regularity scores based on the averaged autocorrelation function within games
	  	  '--- ResDefMis.py - Loads event files and computes resets, deflations and misses within games
	  	  '--- ProcessScores_Cluster_Models.py - Load *.dat files and extracts scores for each model run
	  	  '--- copy_holds_*.sh - Extracts *.holds preprocessed files and copies them to a separate folder (useful for computation of Coefficient of variation measures)
	  	  '--- move_cluster_ext_*.sh - Puts all *.dat or *.evt model files in one folder
	  	  '--- move_cluster_*_evt.sh - Move *.evt model files to a separate folder
	  	  '--- move_cluster_*_dat.sh - Move *.dat model files to a separate folder
	  	  
	PREPROCESS_FOR_R - folder with code to obtain R input table for statistical analyses
	  '--- GetInputs.sh - First Bash script that copy-pastes the output measure files and stores them in a more organized manner
	  '--- Preprocess_R.sh - Second Bash script that uses the output measure files to extract all the relevant information required for R analyses and concatenates everything together
	  '--- Scripts - folder with scripts that are executed for preprocessing
	  	  '--- CVMu_Models.py - Computes model coefficient of variation measures (along with mean & STD of the inter-shot intervals)
	  	  '--- CVMu_Humans.py - Computes human coefficient of variation measures (along with mean & STD of the inter-shot intervals)
	  	  '--- Reformat_Measures.py - adds condition information to output human measure files
	  	  '--- R_Human_Preprocess.py - preprocesses human measure files to create R table
	  	  '--- R_Model_Preprocess.py - preprocesses model measure files to create R table
	  	  '--- Concatenate_R_files.py - concatenates everything together to create final combined R table


	R_ANALYSES
	  '--- Figures - stores the generated figures
	  '--- ToInput - folder with R tables
	  	  '--- R_HumanMod_MS17.txt - data from MS17 model (1 vs. 2 trackers)
	  	  '--- R_HumanMod_Temperature_MS17.txt - data from MS17 model (2 trackers with vs. without temperature)
	  '--- R_scripts - folder with R scripts (python notebook with R kernel)
	  	  '--- Line_Graph_Script.ipynb: Script that generates Figure 4 and Figure 5
	  	  '--- Temperature_Line_Graphs_Script.ipynb: Script that generates line graphs with vs. without temperature
	  	  '--- BIC_Model_Comparison.ipynb: Script that generates BICs for models with 1 vs. 2 trackers (Tables 3 & 4)
	  	  '--- BIC_Temperature_Model_Compare.ipynb: Script that generates BICs for models with vs. without temperature (Tables 3 & 4)
	  	  '--- Transfer_Bootstrap.ipynb: Script that generates Figure 6
	  	  '--- Phase_Compare_Humans.ipynb: Script that generates Figure 7 (Human phase comparisons)
	  	  '--- Phase_Compare_Models.ipynb: Script that generates Supplemental Figure S4 (Model phase comparisons)
	  	  '--- Phase_Compare_Wilcox.ipynb: Script that executes wilcoxon tests (Table 5)
	  	  '--- Analyses_Skill_Levels.ipynb: Script that generates Figure 8, S5 and Table 6


