
Combination of python, bash scripts, and topas files to perform multi-scale simulations of in-vitro irradiation experiments of cells with nanoparticles.

DIRECTORY STRUCTURE
	- simulationFiles: Contains the templates for the main topas simulation txt files that are used in the 3 phase/scale simulations.
	- supportFiles: Contains topas-command files which will be included in the main topas simulation files.
	- TsExtensions: Special topas extensions needed for the simulations.
	- bashscripts: shell scripts to distribute and execute the simulations on a local computer (sequential) or on a cluster (parallel).
	- pythonscripts: Set of python classes and scripts that generate the simulation input files, sample the nanoparticles positions, process result files, ...
	- runFiles: target directory where the simulation input files generated by the python scripts are located.
	- work: directory where the different simulations will be executed. 


IMPORTANT FILES DESCRIPTION

- SimulationConfigFile.txt
[Simulation]
simulatePhase1 = True 							# Phase1 simulation. Generates a phasespace from a primary source
simulatePhase2 = True 							# Phase2 simulation. Cell with nanoparticles. Scores dose and electron phasespace to nucleus
simulatePhase3 = True 							# Phase3 simulation. TOPAS-nBio simulations of electrons in nucleus.
BeamSource = SARRP 								# Name of the TOPAS radiation source: SARRP, TrueBeam, I125
HasSourcePHSP = True                            # If True, will copy the sourcePHSPFiles dir to the execution dir
NPsInMedium = True 								# Presence of NPs in medium. If "False", medium is considered water.
NPsInCell = True  								# Presence of NPs in cell cytoplasm. 
CellType = A549 								# Name of the cell model: A549, ... 
NPType = AuNP15									# Types: AGuIX, AuNP, water, AGuIXBi, ...
NPConcInMedium = 1.0 							# mg of NPs in ml of water. Determines the number of NPs to be explicitely simulated in the detailed region of the medium above the cell,
NPNumberInCell = 5000 							# Number of NPs in the cytoplasm.
NPNumberInMedium = 2000 						# number of NPs to be sampled in the detailed region of the medium above the cell. Overridden by NPConcInMedium.
sortNPPositions = True 							# If true, the positions of NPs are resampled in each job to simulate different cells.
simScriptFile = run_local_script.sh 			# specify the script from the bashscripts directory that will distribute and run the simulations.
njobs = 20 					 					# number of jobs to be executed
nhistories = 1000000 							# number of histories to be simulated per job. Doesn't apply to PhaseSpace sources.
runDirectoryName = RunDir    			    # The name of the directory that will be created in work/ directory, where the simulations will be executed.


The BeamSource, NPType, and CellType parameters determine the name of their corresponding TOPAS files:
Phase1 simulation file name: Phase1_{BeamSource}.txt
Parameters files: cell_parameters_{CellType}.txt, np_parameters_{NPType}.txt, source_parameters_{BeamSource}.txt


- main_run_simulation.sh
Creates the execution directory ($RUNDIR), inside the work directory, where the different jobs will be executed.
Executes the run_simulation python script that creates the topas simulation input files in the $RUNDIR.
Finally, calls the submit_script.sh, which contains the commands to execute the simulations locally or on a cluster.
The name of the $RUNDIR is given as an input of the run_simulation.sh script.

- ./submit_script.sh
Shell script that is created by simulation_manager.py from the simScriptFile specified in the SimulationConfigFile.txt (located in bashscripts directory).
It is initially placed at runFiles directory and then copyed to ./work/$RUNDIR. 

- bashscripts files
These are the scripts that distribute the simulations in jobs with a specific directory configuration.
Depending on your cluster configuration you may need to modify the "run_cluster_script.sh".
The "run_local_script" will execute the jobs in your local computer sequentially.
All these scripts must follow the following structure:
1. Create a run# folder for each job to be executed.
2. Copy the files in the root directory ($RUNDIR) to each run subdirectory.
3. For each run folder:
	- Generate initial seeds for the random number generator and change it in the simulation files.
	- Execute python script (optional).
	- Execute topas simulations.
The value of the variables INFILE#, PYFILE will be modified by the run_simulation.py script according to the information specified in the SimulationConfigFile.txt file

- merge_results.sh
Bash script that calls python scripts to merge the dose results from the different runs. Place the result files in runDirectoryName/results.
		./merge_results.sh SimulationConfigFile.txt

INSTRUCTIONS
Steps to execute a simulation:

1. Edit the SimulationConfigFile.txt file to specify the parameters for your simulation.
2. run the main_run_simulation.sh script as:
         ./main_run_simulation.sh SimulationConfigFile.txt
		 
This will create a "{runDirectoryName}" directory inside the "work" directory where the simulation in the n jobs will be executed.

