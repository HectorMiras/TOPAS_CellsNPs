import json
import numpy as np
import sys
import shutil
import os
from pathlib import Path
import configparser
import re
from get_NP_positions import get_positions
from cell import Cell_class
from nanoparticles import NP_class
from files_and_directory_manager import get_outputfile_paths

class Simulation_manager:

    def __init__(self, workingDir, config_file):

        #with open(config_file, 'r') as file:
            #json_data = json.load(file)
        
        self.workingDir = workingDir
        self.supportFilesDir = os.path.join(workingDir,"supportFiles")
        self.bashScriptsDir = os.path.join(workingDir, "bashscripts")
        self.simulationFilesDir = os.path.join(workingDir, "simulationFiles")
        self.pythonScripts = os.path.join(workingDir, "pythonscripts")
        self.sourcePHSPFiles = os.path.join(workingDir, "sourcePHSPFiles")

        self.read_pyconfig(workingDir, config_file)

        self.read_support_files()

        print("Simulation manager parameters:")
        for attr_name, attr_value in self.__dict__.items():
            print(f"{attr_name}: {attr_value}")
        print("")
        print("Cell parameters:")
        for attr_name, attr_value in self.cell.__dict__.items():
            print(f"{attr_name}: {attr_value}")
        print("")
        print("Nanoparticles parameters:")
        for attr_name, attr_value in self.np.__dict__.items():
            print(f"{attr_name}: {attr_value}")

    def read_pyconfig(self, workingDir, config_file):
        self.ConfigFile = config_file
        config = configparser.ConfigParser(allow_no_value=True)
        with open(os.path.join(workingDir, config_file), 'r') as file:
            config_string = '[simulation]\n' + file.read()

        # Remove inline comments
        config_string = re.sub(r'\s*#.*', '', config_string)

        config.read_string(config_string)

        simulation = config['Simulation']

        self.simulatePhase1 = simulation.getboolean('simulatePhase1')
        self.simulatePhase2 = simulation.getboolean('simulatePhase2')
        self.simulatePhase3 = simulation.getboolean('simulatePhase3')
        self.BeamSource = simulation["BeamSource"]
        self.HasSourcePHSP = simulation.getboolean("HasSourcePHSP")
        self.NPsInMedium = simulation.getboolean("NPsInMedium")
        self.NPsInCell = simulation.getboolean("NPsInCell")
        self.NPType = simulation["NPType"]
        self.CellType = simulation["CellType"]
        self.NPConcInMedium = simulation.getfloat("NPConcInMedium")
        self.NPConcInCell = simulation.getfloat("NPConcInCell")
        self.UpTakeVar = simulation.getfloat("UpTakeVar")/100.0
        if self.NPsInCell:
            self.NPNumberInCell = simulation.getint("NPNumberInCell")
        else:
            self.NPNumberInCell = 1
        if self.NPsInMedium:
            self.NPNumberInMedium = simulation.getint("NPNumberInMedium")
        else:
            self.NPNumberInMedium = 1
        self.sortNPPositions = simulation.getboolean("sortNPPositions")
        self.simScriptFile = simulation["simScriptFile"]
        self.njobs = simulation.getint("njobs")
        self.startingJob = simulation.getint("startingJob", fallback=1)
        self.simSplit = simulation.getint("simSplit", fallback=0)
        self.nhistories = simulation.getint("nhistories")
        self.phsp2Recycle = simulation.getint("phsp2Recycle", fallback=1)
        self.runDirectoryName = simulation["runDirectoryName"]

        # Generates file and directory names from previous parameters
        self.Phase1File = f'Phase1_{self.BeamSource}.txt'
        self.Phase2File = "Phase2_Cell.txt"
        self.Phase3File = "Phase3_dnaDamage.txt"
        self.PHSP1Name = self.BeamSource + "_PHSP"
        self.NPParametersFile = "np_parameters_" + self.NPType + ".txt"
        self.cellParametersFile = f"cell_parameters_{self.CellType}.txt"
        self.SourceParametersFile = "source_parameters_" + self.BeamSource + ".txt"
        #conc_str = str(self.NPConcInMedium)
        #conc_str = conc_str.replace(".", "p")
        #self.runDirectoryName = f"work/{self.BeamSource}_{self.CellType}_{conc_str}_{self.NPNumberInCell}_{self.NPType}_{self.runDirectoryName}"
        #self.runDirectoryName = os.path.join(workingDir, self.runDirectoryName)
        self.runDirectoryName = os.path.join(workingDir,"work", self.runDirectoryName)

        med_conc_str = str(self.NPConcInMedium)
        med_conc_str = med_conc_str.replace(".", "p")
        cell_conc_str = str(self.NPConcInCell)
        cell_conc_str = cell_conc_str.replace(".", "p")
        self.outputFileNameSufix = f"_medium{med_conc_str}mgml_cell{cell_conc_str}mgml_{self.NPType}"


    def read_support_files(self):
        self.cell = Cell_class()
        self.cell.read_file_parameters(os.path.join(self.supportFilesDir, self.cellParametersFile))
        self.np = NP_class()
        self.np.read_file_parameters(os.path.join(self.supportFilesDir, self.NPParametersFile))

        if self.NPsInMedium:
            # Get the number of NPs from the concentration
            vol_medium = 3.1415926 * 0.2 * np.power(1.25 * self.cell.rNucl, 2)
            npart = self.np.number_from_conc_volume(self.NPConcInMedium, vol_medium)
            self.NPNumberInMedium = npart
            self.np_positions_in_medium_file = "positions_in_medium_" + \
                                               str(self.NPNumberInMedium) + "_" + self.NPType + ".txt"
        else:
            self.np_positions_in_medium_file = "positions_in_medium_1_NP.txt"
        if self.NPsInCell:
            # Get the number of NPs from the concentration and cytoplasm volume
            npart = self.np.number_from_conc_volume(self.NPConcInCell, self.cell.volume_cytoplasm())
            self.NPNumberInCell = npart
            self.np_positions_in_cell_file = "positions_in_cell_" + \
                                             str(self.NPNumberInCell) + "_" + self.NPType + ".txt"
        else:
            self.np_positions_in_cell_file = "positions_in_cell_1_NP.txt"


    def map_files(self):

        # Create run directory if it does not exist
        os.makedirs(self.runDirectoryName, exist_ok=True)

        # Copy config file to run directory
        source = os.path.join(self.workingDir, self.ConfigFile)
        destination = os.path.join(self.runDirectoryName, self.ConfigFile)
        shutil.copy(source, destination)
        
        # Create supportFiles dir and copy files
        destination_dir = os.path.join(self.runDirectoryName, 'supportFiles')
        os.makedirs(destination_dir, exist_ok=True)
        for file_name in os.listdir(self.supportFilesDir):
            source = os.path.join(self.supportFilesDir, file_name)
            destination = os.path.join(destination_dir, file_name)
            if os.path.isfile(source):
                shutil.copy(source, destination)
        # Copy the python scripts for NP sampling to runDirectoryName/supportFiles
        for file in ["get_NP_positions.py", "sample_positions_in_cell.py", "sample_positions_in_medium.py"]:
            source_file_path = os.path.join(self.pythonScripts, file)
            destination_file_path = os.path.join(self.runDirectoryName, 'supportFiles', file)
            shutil.copyfile(source_file_path, destination_file_path)

        # Map the Phase1File
        if self.simulatePhase1:
            self.map_phase1_file()

        # Map the Phase2File
        if self.simulatePhase2:
            self.map_phase2_file()

        # Map the Phase3File
        if self.simulatePhase3:
            self.map_phase3_file()

        # Process self.simScriptFile
        self.map_simScriptFile()

        # map python scripts for sampling NPs
        self.map_sample_positions_pyscripts()

        # If phase1 is using source phase space, copy phsp files directory
        if self.HasSourcePHSP:
            # Create supportFiles dir and copy files
            destination_dir = os.path.join(self.runDirectoryName, 'sourcePHSPFiles')
            os.makedirs(destination_dir, exist_ok=True)
            for file_name in os.listdir(self.sourcePHSPFiles):
                source = os.path.join(self.sourcePHSPFiles, file_name)
                destination = os.path.join(destination_dir, file_name)
                if os.path.isfile(source):
                    shutil.copy(source, destination)




    def map_sample_positions_pyscripts(self):
        # Map python scripts for generating np positions
        with open(os.path.join(self.pythonScripts, "sample_positions_in_medium.py"), 'r') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            line = lines[i]
            if "positions_file =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'\"{self.np_positions_in_medium_file}\"')
            if "Rmax =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'1.25*{1000 * self.cell.rNucl}')
            if "Rnp =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{self.np.rNP}')
            if "N =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{self.NPNumberInMedium}')


        # write the file
        with open(os.path.join(self.runDirectoryName, "supportFiles", "sample_positions_in_medium.py"), 'w') as file:
            file.writelines(lines)

        with open(os.path.join(self.pythonScripts, "sample_positions_in_cell.py"), 'r') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            line = lines[i]
            if "positions_file =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'\"{self.np_positions_in_cell_file}\"')
            if "Rmax =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{1000 * self.cell.rCell}')
            if "Rmin =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{1000 * self.cell.rNucl}')
            if "H =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{1000 * self.cell.height}')
            if "Rnp =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{self.np.rNP}')
            if "N =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{self.NPNumberInCell}')
            if "sN =" in line:
                old_value = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_value, f'{int(self.NPNumberInCell*self.UpTakeVar)}')

        # write the file
        with open(os.path.join(self.runDirectoryName, "supportFiles", "sample_positions_in_cell.py"), 'w') as file:
            file.writelines(lines)

    def map_phase1_file(self):
        # read the file Phase1 File
        with open(os.path.join(self.simulationFilesDir, self.Phase1File), 'r') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            line = lines[i]
            # check if the line contains the keywords
            if "NumberOfHistoriesInRun" in line:
                old_file_name = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_file_name, f'{self.nhistories}')
            if "includeFile" in line and "cell_parameters" in line:
                # get the old file name
                old_file_name = line.split("/")[-1].strip()
                lines[i] = line.replace(old_file_name, self.cellParametersFile)
            if "includeFile" in line and "source_parameters_" in line:
                old_file_name = line.split("/")[-1].strip()
                lines[i] = line.replace(old_file_name, self.SourceParametersFile)
            if "includeFile" in line and "np_parameters_" in line:
                old_file_name = line.split("/")[-1].strip()
                lines[i] = line.replace(old_file_name, self.NPParametersFile)
            if "s:Ge/CellPHSPName" in line:
                old_file_name = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_file_name, f'\"{self.PHSP1Name}\"')
            if "s:Sc/DoseCell/OutputFile" in line:
                old_file_name = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_file_name, f"\"DoseToCell_{self.BeamSource}\"")
            if "s:Ge/MediumVol/Material" in line:
                if not self.NPsInMedium:
                    old_values = line.split("= ")[-1].strip()
                    lines[i] = line.replace(old_values, f"\"G4_WATER\"")

            # update medium composition and density values from NPs concentration
            w_water, w_np, dens_tot = self.np.get_relweights_and_dens_from_conc(self.NPConcInMedium)
            if "Ma/MediumMaterial/Fractions" in line:
                old_values = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_values, f"2 {w_water} {w_np}")
            if "Ma/MediumMaterial/Density" in line:
                old_values = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_values, f"{dens_tot} g/cm3")

        # write the file
        with open(os.path.join(self.runDirectoryName, self.Phase1File), 'w') as file:
            file.writelines(lines)

    def map_phase2_file(self):
        # read the file Phase2 File
        with open(os.path.join(self.simulationFilesDir, self.Phase2File), 'r') as file:
            lines = file.readlines()

        conc_str = str(self.NPConcInMedium)
        conc_str = conc_str.replace(".", "p")

        for i in range(len(lines)):
            line = lines[i]
            # check if the line contains the keywords
            if "includeFile" in line and "cell_parameters" in line:
                # get the old file name
                old_file_name = line.split("/")[-1].strip()
                lines[i] = line.replace(old_file_name, self.cellParametersFile)
            if "includeFile" in line and "source_parameters_" in line:
                # get the old file name
                old_file_name = line.split("/")[-1].strip()
                # replace the old file name with the new one
                lines[i] = line.replace(old_file_name, self.SourceParametersFile)
            if "includeFile" in line and "np_parameters_" in line:
                old_file_name = line.split("/")[-1].strip()
                lines[i] = line.replace(old_file_name, self.NPParametersFile)
            if "s:Ge/CellPHSPName" in line:
                old_file_name = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_file_name, f"\"{self.PHSP1Name}\"")
            if "s:Sc/NucleusPHSP/OutputFile" in line:
                old_file_name = line.split("= ")[-1].strip()
                new_file_name = f"\"nucleus_PHSP{self.outputFileNameSufix}_electrons\""
                lines[i] = line.replace(old_file_name, new_file_name)
            if "s:Sc/DoseNucleus_e/OutputFile" in line:
                old_file_name = line.split("= ")[-1].strip()
                new_file_name = f"\"DoseToNucleus{self.outputFileNameSufix}_electrons\""
                lines[i] = line.replace(old_file_name, new_file_name)
            if "s:Sc/DoseNucleus_g/OutputFile" in line:
                old_file_name = line.split("= ")[-1].strip()
                new_file_name = f"\"DoseToNucleus{self.outputFileNameSufix}_gammas\""
                lines[i] = line.replace(old_file_name, new_file_name)
            if "s:Ge/MediumNPPositionsFile" in line:
                old_file_name = line.split("= ")[-1].strip()
                new_file_name = f'\"./supportFiles/{self.np_positions_in_medium_file}\"'
                lines[i] = line.replace(old_file_name, new_file_name)
            if "s:Ge/CellNPPositionsFile" in line:
                old_file_name = line.split("= ")[-1].strip()
                new_file_name = f'\"./supportFiles/{self.np_positions_in_cell_file}\"'
                lines[i] = line.replace(old_file_name, new_file_name)
            if "s:Ge/MediumVol/Material" in line:
                if not self.NPsInMedium:
                    old_file_name = line.split("= ")[-1].strip()
                    lines[i] = line.replace(old_file_name, f"\"G4_WATER\"")
            if "s:Ge/MediumDetailed/ElementMaterial" in line:
                if not self.NPsInMedium:
                    old_values = line.split("= ")[-1].strip()
                    lines[i] = line.replace(old_values, f"\"G4_WATER\"")
            if "s:Ge/Cell/ElementMaterial" in line:
                if not self.NPsInCell:
                    old_values = line.split("= ")[-1].strip()
                    lines[i] = line.replace(old_values, f"\"G4_WATER\"")
            if "Ge/CellLayer/Material" in line:
                if not self.NPsInMedium:
                    old_values = line.split("= ")[-1].strip()
                    lines[i] = line.replace(old_values, f"\"G4_WATER\"")
            if ("i:So/" in line) and ("PhaseSpaceMultipleUse" in line):
                old_values = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_values, f"{str(self.phsp2Recycle)}")

            # update medium composition and density values from NPs concentration
            w_water, w_np, dens_tot = self.np.get_relweights_and_dens_from_conc(self.NPConcInMedium)
            if "Ma/MediumMaterial/Fractions" in line:
                old_values = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_values, f"2 {w_water} {w_np}")
            if "Ma/MediumMaterial/Density" in line:
                old_values = line.split("= ")[-1].strip()
                lines[i] = line.replace(old_values, f"{dens_tot} g/cm3")

        # write the file
        with open(os.path.join(self.runDirectoryName, self.Phase2File), 'w') as file:
            file.writelines(lines)


    def map_phase3_file(self):
        # read the file Phase3 File
        with open(os.path.join(self.simulationFilesDir, self.Phase3File), 'r') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            line = lines[i]
            # check if the line contains the keywords
            if "includeFile" in line and "cell_parameters" in line:
                # get the old file name
                old_file_name = line.split("/")[-1].strip()
                lines[i] = line.replace(old_file_name, self.cellParametersFile)
            if "s:Ge/SourcePHSPName" in line:
                old_file_name = line.split("= ")[-1].strip()
                conc_str = str(self.NPConcInMedium)
                conc_str = conc_str.replace(".", "p")
                new_file_name = f"\"nucleus_PHSP_{conc_str}mgml_{self.NPNumberInCell}_{self.NPType}_electrons\""
                lines[i] = line.replace(old_file_name, new_file_name)

        # write the file
        with open(os.path.join(self.runDirectoryName, self.Phase3File), 'w') as file:
            file.writelines(lines)


    def map_simScriptFile(self):
        with open(os.path.join(self.bashScriptsDir, self.simScriptFile), 'r') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            line = lines[i]

            if line.startswith("ITER="):
                lines[i] = f'ITER={self.njobs} \n'

            if line.startswith("ADDITION="):
                lines[i] = f'ADDITION={self.startingJob - 1} \n'

            if line.startswith("SPLITNUM="):
                lines[i] = f'SPLITNUM={self.simSplit} \n'

            if line.startswith("INFILE1="):
                lines[i] = f'INFILE1=\"{self.Phase1File}\" \n'
            if not self.simulatePhase1:
                if "topas $INFILE1" in line:
                    lines[i] = "#"+line
                if "topas $SIMFILE3" in line:
                    lines[i] = "#"+line
                if "cp $INFILE1 $DIR" in line:
                    lines[i] = "#"+line
                if "sed -i" and "$DIR/$INFILE1" in line:
                    lines[i] = "#"+line

            if line.startswith("INFILE2="):
                lines[i] = f'INFILE2=\"{self.Phase2File}\" \n'
            if not self.simulatePhase2:
                if "topas $INFILE2" in line:
                    lines[i] = "#"+line
                if "topas $SIMFILE3" in line:
                    lines[i] = "#"+line
                if "cp $INFILE2 $DIR" in line:
                    lines[i] = "#"+line
                if "sed -i" and "$DIR/$INFILE2" in line:
                    lines[i] = "#"+line

            if line.startswith("INFILE3="):
                lines[i] = f'INFILE3=\"{self.Phase3File}\" \n'
            if not self.simulatePhase3:
                if "topas $INFILE3" in line:
                    lines[i] = "#"+line
                if "topas $SIMFILE3" in line:
                    lines[i] = "#"+line
                if "cp $INFILE3 $DIR" in line:
                    lines[i] = "#"+line
                if "sed -i" and "$DIR/$INFILE3" in line:
                    lines[i] = "#"+line

            if line.startswith("DELFILE="):
                old_file_name = line.split("=")[-1].strip()
                new_file_name = f'\"{self.PHSP1Name}.phsp\"'
                lines[i] = line.replace(old_file_name, new_file_name)

            if self.sortNPPositions:
                if "DOSAMPLE=" in line:
                    lines[i] = "DOSAMPLE=true"
            else:
                if "DOSAMPLE=" in line:
                    lines[i] = "DOSAMPLE=false"

        # write the bash file
        with open(os.path.join(self.runDirectoryName, "submit_script.sh"), 'w') as file:
            file.writelines(lines)


    def collect_np_number(self):
        folder_path = self.runDirectoryName

        file_pattern = f"np_number"
        output_path = os.path.join(folder_path, "results")
        os.makedirs(output_path, exist_ok=True)

        output_file_paths = get_outputfile_paths(folder_path, file_pattern, 'txt')

        lines_list = []
        for file_path in output_file_paths:
            path = os.path.dirname(file_path)
            run_number = path.split('run')[-1].split('/')[0]

            with open(file_path, 'r') as f:
                nlines = int(f.readlines()[0])
                lines_list.append(f'{run_number} {nlines}')

        # Write a results file with all the results from each job
        lines_list.sort(key=lambda x: int(x.split()[0]))
        with open(os.path.join(output_path, f'AllJobs_np_number.csv'), "w") as f:
            f.write(f'#  Run#  NP#\n')
            for line in lines_list:
                f.write(f'{line}\n')



    def merge_DoseToNucleus_results(self):

        folder_path = self.runDirectoryName

        filenames = [f"DoseToNucleus{self.outputFileNameSufix}_electrons",
                     f"DoseToNucleus{self.outputFileNameSufix}_gammas"]
        output_path = os.path.join(folder_path, "results")
        os.makedirs(output_path, exist_ok=True)

        for filename in filenames:
            # Merge EnergyDeposit or DoseToMedium files from different runs
            combined_sum = 0
            combined_count_in_bin = 0
            combined_second_moment = 0
            combined_histories_with_scorer_active = 0
            output_file_paths = get_outputfile_paths(folder_path, filename, 'csv')
            cont = 0
            var = 0.0
            lines_list = []
            for file_path in output_file_paths:
                # subfolder_name = f'run{run_number}'

                # Read EnergyDepositToNucleus.csv file
                # file_path = Path(f'{folder_path}/{subfolder_name}/{filename}').absolute()
                path = os.path.dirname(file_path)
                run_number = path.split('run')[-1]

                with open(file_path, 'r') as f:
                    lines = f.readlines()

                # Extract the data from the last line
                if len(lines) > 0:
                    data_line = lines[-1]
                    lines_list.append(f'{run_number} {data_line}')
                    data_values = [float(value) for value in data_line.split(', ')]

                    sum_dose, mean_dose, count_in_bin, second_moment, variance, std_dev, histories_with_scorer_active = data_values

                    # Combine the output values
                    combined_sum += sum_dose
                    combined_count_in_bin += count_in_bin
                    combined_second_moment += second_moment
                    combined_histories_with_scorer_active += histories_with_scorer_active
                    var = var + sum_dose * sum_dose
                    cont = cont + 1
            # Calculate the combined mean, variance, and standard deviation
            combined_mean = combined_sum / combined_histories_with_scorer_active
            combined_variance = combined_second_moment / combined_histories_with_scorer_active - combined_mean ** 2
            combined_std_dev = np.sqrt(combined_variance)
            var = np.sqrt(var / cont - combined_sum * combined_sum / (cont * cont))

            # Write the combined results to a new output file
            with open(os.path.join(output_path, f'combined_{filename}.csv'), "w") as f:
                for line in lines[:-1]:
                    f.write(line)

                f.write(f"{combined_sum}, {combined_mean}, {combined_count_in_bin}, {combined_second_moment}, "
                        f"{combined_variance}, {combined_std_dev}, {combined_histories_with_scorer_active}\n")

            # Write a results file with all the results from each job
            lines_list.sort(key=lambda x: int(x.split()[0]))
            with open(os.path.join(output_path, f'AllJobs_{filename}.csv'), "w") as f:
                for line in lines[:-1]:
                    f.write(line)
                for line in lines_list:
                    f.write(line)

            unc_2sigma = combined_std_dev / np.sqrt(combined_histories_with_scorer_active)
            print('')
            print(f'File {filename:}')
            print(f'Number of results merged: {cont} out of {len(output_file_paths)}')
            print(f'Dose (Gy/hist): {combined_mean} +/- {unc_2sigma}')
            print(f'Sum Dose = {combined_sum / cont} +/- {var}')
            print('')
